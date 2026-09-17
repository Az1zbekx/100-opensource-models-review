# YOLOv8 orqali real-time odam (person) detection

## 📋 Tezkor xulosa (PM uchun)

| Savol | Javob |
|---|---|
| Qaysi project ehtiyoji uchun mos | Kamera orqali kuzatuv, hozirlik/yo'qlik aniqlash, obyekt sanash, xavfsizlik monitoring |
| GPU kerakmi | **Yo'q** — CPU'da real-time ishlaydi |
| Oylik server xarajati | **$0 qo'shimcha** (mavjud serverning resursidan foydalanadi) |
| Joriy backend bilan bitta serverda ishlay oladimi | ✅ Ha, muammosiz (bitta kamera oqimi uchun) |
| Ko'p kamera (5-10+) kerak bo'lsa | GPU zarur bo'ladi — pastdagi "GPU moslik" bo'limiga qarang |

---

Bu loyihada Ultralytics tomonidan chiqarilgan **YOLOv8n** (nano versiya) ochiq manbali (open-source) modeli sinovdan o'tkazildi. Model laptop kamerasidan olingan real-time video oqimida odam borligi/yo'qligini aniqlash uchun ishlatildi, va shu asosda oddiy presence-detection (hozirlik aniqlash) mantig'i qurildi.

**Repo tarkibi:** `demo.py` (asosiy skript, `--headless` bayrog'ini qo'llab-quvvatlaydi), `requirements.txt`, `Dockerfile` va `docker-compose.yml` (Docker orqali ishga tushirish uchun).

---

## 1. Model haqida umumiy ma'lumot

**YOLO** (*You Only Look Once*) — real-time object detection uchun mo'ljallangan neural network arxitekturalar oilasi. Klassik ikki bosqichli detektorlardan (masalan R-CNN) farqli o'laroq, YOLO butun rasmni **bitta forward pass**da qayta ishlab, bir vaqtning o'zida ham obyekt qayerdaligini (bounding box), ham u nima ekanligini (klass) aniqlaydi. Bu uni sezilarli darajada tezroq qiladi, shuning uchun real-time video uchun mos.

| Xususiyat | Qiymat |
|---|---|
| Model | YOLOv8n (nano) |
| Ishlab chiqargan | Ultralytics |
| Vazifa | Object detection |
| O'qitilgan dataset | COCO (80 klass: odam, mashina, hayvon va h.k.) |
| Og'irligi | ~6 MB |
| Litsenziya | AGPL-3.0 (Ultralytics) |
| Manba | [Ultralytics GitHub](https://github.com/ultralytics/ultralytics), [Hugging Face](https://huggingface.co/Ultralytics) |

> **Muhim izoh:** Bu loyihada model **hech qanday o'qitilmadi (training qilinmadi)** va COCO dataseti o'zimiz tomonidan yuklanmadi/ko'rilmadi. Ultralytics kompaniyasi modelni oldindan COCO'da o'qitib, tayyor og'irliklar (`yolov8n.pt`) sifatida chiqargan. Biz faqat shu tayyor modelni yuklab, **inference** (tayyor modeldan real-time natija olish) uchun ishlatdik. Yuqoridagi COCO haqidagi ma'lumot faqat shaffoflik uchun — model qaysi 80 ta obyektni tanishga "o'rgatilganini" ko'rsatish uchun keltirilgan.

**Nima uchun "nano" versiya tanlandi:** YOLOv8 bir nechta o'lchamda keladi — `n` (nano), `s` (small), `m` (medium), `l` (large), `x` (xlarge). Katta o'lchamlar aniqroq, lekin sekinroq va ko'proq resurs talab qiladi. Bizga faqat bitta klass (`person`) va CPU'da real-time ishlash kerak bo'lgani uchun eng yengil `nano` versiya yetarli va optimal tanlov bo'ldi.

---

## 2. Bu loyihada nima qilindi (qisqacha)

- Laptop kamerasidan `OpenCV` orqali real-time video oqimi olindi.
- Har bir frame YOLOv8n orqali qayta ishlanib, faqat `person` (odam) klassi filtrlandi (`classes=[0]`, `conf=0.5`).
- Aniqlangan odam atrofiga ko'k rangli bounding box chizildi (vizual tasdiqlash uchun).
- Kadrda odam bor/yo'qligiga qarab oddiy holat mashinasi (state machine) qurildi: `PRESENT` (bor) → `ABSENT` (yo'q) → belgilangan vaqtdan ko'p yo'q bo'lsa `ALERTED`.
- **Muhim texnik muammo va yechimi:** model har bir frame'ni mustaqil baholaganligi sababli, odam kadr chegarasidan kirib-chiqayotganda (qisman ko'ringanda) natija bir necha frame davomida beqaror bo'lib qoldi ("flickering" — bir soniyada bir necha marta "bor/yo'q" almashinishi). Bu **debounce** texnikasi bilan hal qilindi: holat faqat ketma-ket N ta frame bir xil natija bergandan keyingina o'zgartiriladi. Bu — signal ishonchsiz bo'lganda barqaror qaror qabul qilishning standart usuli.

---

## 3. Model yana nimalarga qodir

YOLOv8n loyihada faqat `person` klassi uchun ishlatildi, lekin modelning imkoniyatlari ancha kengroq:

- **80 xil obyekt klassini** bir vaqtda aniqlay oladi (COCO dataset klasslari: mashina, velosiped, it, mushuk, telefon, stul va h.k.) — `classes=[0]` filtrini olib tashlasa bo'ldi.
- Ultralytics oilasida shu arxitekturaning boshqa vazifalar uchun versiyalari ham bor:
  - **YOLOv8-seg** — instance segmentation (obyektning aniq shaklini piksel darajasida ajratish)
  - **YOLOv8-pose** — inson tanasi tayanch nuqtalarini (skelet, pose estimation) aniqlash
  - **YOLOv8-obb** — burchak bilan aylantirilgan (oriented) bounding box, masalan aerofoto rasmlar uchun
- **Custom fine-tuning**: agar loyiha COCO'da yo'q maxsus obyektni (masalan ma'lum bir mahsulot, xavfsizlik kaskasi) aniqlashi kerak bo'lsa, model o'z datasetingda qayta o'qitilishi (fine-tune) mumkin.
- **Kattaroq versiyalar (`s`/`m`/`l`/`x`)**: agar aniqlik nano versiyadan yetarli bo'lmasa, xuddi shu kodni deyarli o'zgartirmasdan (`YOLO("yolov8s.pt")` kabi) kattaroq modelga o'tish mumkin — tezlik hisobiga aniqlik oshadi.

---

## 4. Model qanday ishlaydi (texnik mexanizm)

YOLOv8 arxitekturasi uch qismdan iborat:

- **Backbone** — konvolyutsion qatlamlar kirish rasmidan xususiyat (feature) ajratadi: erta qatlamlar oddiy naqshlarni (chekka, burchak), chuqur qatlamlar murakkab shakllarni (tana, yuz konturi) aniqlaydi.
- **Neck** (FPN/PANet tipidagi struktura) — turli chuqurlikdagi qatlamlar xususiyatlarini birlashtiradi, shu orqali model kichik va katta obyektlarni bir vaqtda yaxshi aniqlaydi.
- **Head** — anchor-free: har bir grid katakchasi uchun to'g'ridan-to'g'ri bounding box koordinatalari va klass ehtimolliklarini chiqaradi (eski YOLO versiyalaridagi oldindan belgilangan "anchor box" o'lchamlariga tayanmaydi).

**Parametrlar** — training paytida sozlangan konvolyutsion filtr og'irliklari. YOLOv8n'da **~3.2 million** parametr bor (eng kichik versiya):

| Versiya | Parametrlar | Nisbiy tezlik (CPU) | Nisbiy aniqlik (mAP) |
|---|---|---|---|
| YOLOv8n | 3.2M | eng tez | eng past |
| YOLOv8s | 11.2M | tez | o'rtacha |
| YOLOv8m | 25.9M | o'rtacha | yaxshi |
| YOLOv8l | 43.7M | sekin | yuqori |
| YOLOv8x | 68.2M | eng sekin | eng yuqori |

Ko'proq parametr = ko'proq "sig'im" (murakkab naqshlarni farqlash qobiliyati), lekin shunga mos ravishda ko'proq hisoblash resursi talab qiladi — bu klassik aniqlik/tezlik trade-off.

---

## 5. Resurs talabi (bu loyihada aniq nima ishlatildi)

| Resurs | Bu loyihada ishlatilgan/yetarli bo'lgan |
|---|---|
| Protsessor | Oddiy zamonaviy laptop CPU'si (GPU'siz) |
| RAM | 2–4 GB |
| Disk | ~6 MB (model og'irligi) |
| GPU | Kerak bo'lmadi — CPU'da real-time ishladi |
| Internet | Faqat birinchi ishga tushirishda (model yuklab olish uchun) |

**Kattaroq ko'lamda (real production loyiha) resurs qanday o'zgaradi:**
- Bitta kameradan CPU'da YOLOv8n — muammosiz. 5-10+ kamerani bir vaqtda parallel qayta ishlash kerak bo'lsa — GPU zarur bo'ladi (masalan NVIDIA RTX 3060 darajasidagi kartochka).
- **Fine-tuning/training** qilish (o'z datasetingda modelni qayta o'qitish) — bu inference'dan butunlay boshqa yuk: kamida 8 GB VRAM'li GPU va soatlab vaqt talab qiladi. Bu loyihada training qilinmadi (yuqorida aytilganidek, faqat tayyor model ishlatildi).

---

## 6. GPU moslik va bulutli xarajat (agar production'da ishlatilsa)

### Qaysi GPU'larda ishlaydi

YOLOv8'ga CUDA orqali tezlashtirish uchun **compute capability 6.0 va undan yuqori** bo'lgan istalgan NVIDIA GPU mos keladi, chunki YOLOv8 CUDA orqali GPU tezlashtirishga tayanadi, shuning uchun compute capability 6.0 yoki undan yuqori bo'lgan NVIDIA GPU kerak bo'ladi — bu 2016 yildan keyin chiqqan deyarli barcha NVIDIA kartalarni qamrab oladi (GTX 10-seriyadan boshlab).

YOLOv8n juda yengil model bo'lgani uchun GPU talabi minimal: bitta kameradan real-time uchun istalgan GPU yetarli — RTX 3050 kabi kichik kartochka ham YOLOv8n bilan 640×640 o'lchamda 400+ FPS beradi; 4-8 ta kamera oqimini parallel ishlatish uchun esa RTX 4060 + YOLOv8s tavsiya etiladi.

**Muhim farq — inference vs training:** training/fine-tuning uchun kamida RTX 3090 darajasidagi GPU kerak, chunki training inference'dan 3-5 baravar ko'proq VRAM talab qiladi.

| Stsenariy | Tavsiya etilgan GPU |
|---|---|
| Bitta kamera, real-time (bizning loyiha) | GPU shart emas, CPU yetarli |
| Bitta kamera, GPU bilan tezroq | Deyarli har qanday GPU (RTX 3050+) |
| 4-8 kamera parallel | RTX 4060 / RTX A5000 darajasida |
| Fine-tuning (o'z datasetingda qayta o'qitish) | RTX 3090 yoki undan yuqori (24 GB VRAM) |

### Bulutda ishlatilsa, oyiga qancha turadi

Agar model shaxsiy kompyuterda emas, bulutli GPU serverida 24/7 ishlatilsa (masalan ko'p kamerali production loyihada), taxminiy narxlar (RunPod, 2026-yil avgust holatiga ko'ra, soatlik ijaraga asoslangan, 730 soat/oy hisobida):

| GPU | Narx/soat | Taxminiy oylik narx (24/7) |
|---|---|---|
| RTX A5000 | $0.27/soat | ~$197 |
| L4 | $0.39/soat | ~$285 |
| A40 | $0.44/soat | ~$321 |
| RTX 3090 | $0.46/soat | ~$336 |
| RTX 4090 | $0.69/soat | ~$504 |
| A100 PCIe 80GB | $1.39/soat | ~$1,015 |
| H100 PCIe 80GB | $2.89/soat | ~$2,110 |

> **Bizning loyiha uchun xulosa:** yuqoridagi jadval **kerak emas** — bitta kamera, CPU'da real-time ishlagani uchun qo'shimcha xarajat **$0**. Bulutli GPU narxi faqat loyiha ko'p kamerali, yuqori aniqlik talab qiladigan yoki fine-tuning kerak bo'ladigan production tizimiga aylansa dolzarb bo'ladi.
>
> Narxlar bozorga qarab tez o'zgaradi (oxirgi 90 kunda RTX 4090 narxi ~13% pasaygan) — production rejalashtirishdan oldin provayder (RunPod, Lambda Labs, Vast.ai) saytidan joriy narxni tekshirish tavsiya etiladi.

---

## 7. Real loyihalarda qanday ishlatiladi (bizning kod darajasidan farqi)

Bu loyihadagi kod (`while True: cap.read()...`) — faqat **local demo/test** uchun mos, professional production tizimida boshqacha yondashiladi:

- **Model formatini optimallashtirish** — xom `.pt` (PyTorch) fayl o'rniga, tezlik uchun **ONNX** (turli platformalarga universal) yoki **TensorRT** (NVIDIA GPU uchun maxsus tezlashtirilgan) formatiga eksport qilinadi (`model.export(format="onnx")`).
- **API sifatida o'rash** — model to'g'ridan-to'g'ri ilova ichiga "ko'milmaydi", odatda alohida servis sifatida (masalan FastAPI orqali) ishga tushiriladi, boshqa qismlar unga HTTP so'rov orqali murojaat qiladi.
- **Konteynerlashtirish** — Docker (GPU kerak bo'lsa `nvidia-docker`) orqali barqaror, ko'chiriladigan muhitda deploy qilinadi.
- **Edge vs Cloud** — kamera joyida (edge, masalan Raspberry Pi + Coral TPU yoki oddiy PC) ishlatish tezkor javob beradi va internetga bog'liq emas; markaziy serverda (cloud) ishlatish esa ko'p kameradan kelgan oqimni kuchli GPU bilan parallel qayta ishlashga imkon beradi, lekin tarmoq kechikishi paydo bo'ladi.

**Real dunyoda YOLOv8 (person detection) qo'llaniladigan sohalar:** xavfsizlik/kuzatuv tizimlari, chakana savdo do'konlarida mijozlar oqimini tahlil qilish, ombor/fabrikada xavfsizlik qoidalariga rioya qilishni kuzatish (kaska, jilet borligini tekshirish — fine-tuning bilan), avtonom transport va robototexnikada obyektlarni aniqlash.

---

## 8. Cheklovlari (kuzatilgan)

- Bitta frame asosida ishonch darajasi past bo'lishi mumkin — real ilovada bir necha frame bo'ylab tasdiqlash (debounce) zarur.
- Kichik yoki uzoq masofadagi obyektlarni yomon aniqlaydi.
- Yorug'lik sharoiti va harakat loyqalanishi (motion blur) aniqlikka sezilarli ta'sir qiladi.
- COCO datasetida yo'q maxsus obyektlarni tanimaydi (fine-tuning talab qiladi).

---

## 8. Ishga tushirish

Loyihani ishga tushirishning **ikki usuli** bor. Ular tasodifiy emas — quyida sababi tushuntirilgan.

> Bu model `100-opensource-models-review` repo'sining `cv/yolov8n/` papkasida joylashgan — clone qilinadigan narsa **bosh repo**, alohida repo emas.

### A) Native (venv) — GUI oynasi bilan, tavsiya etiladigan usul

Bounding box'larni ko'z bilan ko'rish uchun eng oddiy va ishonchli yo'l:

```bash
git clone https://github.com/<username>/100-opensource-models-review.git
cd 100-opensource-models-review/cv/yolov8n

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

python demo.py
```

Chiqish uchun oynada `q` tugmasini bosing.

### B) Docker — headless (oynasiz) rejim

`cv/yolov8n/` papkasida turib (yuqoridagi `cd` bosqichidan keyin):

```bash
docker compose up --build
```

Bu rejimda oyna ochilmaydi, natijalar faqat konsolga (`Odam ketdi` / `Odam qaytdi` / `ALERT!`) yoziladi.

> **Nega Docker'da GUI yo'q:** kamera qurilmasi va ekran chiqishi (`cv2.imshow`) konteyner ichidan operatsion tizimga qarab har xil ishlaydi — Linux'da qo'shimcha sozlash (X11 forwarding) bilan mumkin, lekin Mac va Windows'da bu ancha murakkablashadi va ishonchli ishlamaydi. Shuning uchun Docker versiyasi ataylab **headless** qilib qo'yilgan — bu, "kim bo'lmasin, qaysi operatsion tizimda bo'lmasin, bir xil natija olsin" degan maqsadga eng mos yechim. Vizual (oynali) tekshirish kerak bo'lsa, A) usulidan foydalaning.

**Linux'da kamera qurilmasini tekshirish:** agar `/dev/video0` boshqa nomda bo'lsa (masalan `/dev/video1`), buni `docker-compose.yml` faylidagi `devices` qatorida mos ravishda o'zgartiring.

Ikkala usulda ham model birinchi ishga tushirilganda (`yolov8n.pt`) avtomatik ravishda Ultralytics serverlaridan yuklab olinadi (~6 MB, internet talab qiladi).

---

## 9. Foydalanilgan manbalar

- Ultralytics YOLOv8 rasmiy hujjatlari: https://docs.ultralytics.com
- COCO dataset: https://cocodataset.org
- YOLOv8 GPU/VRAM talablari: https://gigagpu.com/yolov8-vram-requirements/
- Bulutli GPU narxlari (RunPod, 2026): https://www.runpod.io/product/cloud-gpus, https://diyai.io/ai-tools/hosting/runpod-pricing/
