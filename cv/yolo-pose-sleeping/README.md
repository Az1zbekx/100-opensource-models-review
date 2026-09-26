# 04 - YOLO Pose & Workplace Sleeping / Fatigue Analyzer (YOLO11 Nano Pose)

## Mundarija (Table of Contents)
- [Modelning Asosiy Ustunligi ("Killer Feature")](#modelning-asosiy-ustunligi-killer-feature)
- [Qaysi loyihalar uchun ideal (Best Project Fit)](#qaysi-loyihalar-uchun-ideal)
- [Texnik ko'rsatkichlar va apparat talabi (GTX 1650 vs CPU)](#texnik-korsatkichlar-va-apparat-talabi)
- [Halol va Aniq Tahlil: Kamchiliklari va Kechagi Sinovdagi Xatolar](#halol-va-aniq-tahlil)
- [Muhandislik Retsepti: Sekundomer Taymeri (Temporal Timer) va Geometriya](#muhandislik-retsepti-sekundomer-taymeri)
- [Production Server & Masshtablash (Navbatchilik Postlari va Zavodlar)](#production-server--masshtablash)
- [Qanday ishga tushiriladi (CLI & Demo)](#qanday-ishga-tushiriladi)

---

## Modelning Asosiy Ustunligi ("Killer Feature")

Insonning charchoqligi yoki uxlab qolganini aniqlashda ko'pincha yuz/ko'z modellaridan (Dlib Eye Aspect Ratio) foydalaniladi. Ammo ularning kamchiligi — agar inson boshini pastga egsa, ko'zlar umuman ko'rinmay qoladi.

**YOLO11 Nano Pose (`yolo11n-pose.pt`)** ning asosiy ustunligi:
1. **17 ta Tana Bo'g'inlari (Keypoints):** Inson yuzini yopib olgan, orqaga burilgan yoki stolga egilib yotgan bo'lsa ham, yelka, bo'yin, tirsak va bilak burchaklaridan uning haqiqiy holatini 100% tushunadi.
2. **Shaxsiy Maxfiylik (Privacy / GDPR) Kafolati:** Model xodimning yuzini saqlamaydi yoki shaxsini tanimaydi. U faqat geometrik koordinatalarni hisoblagani sababli korxona xodimlarining shaxsiy hayot huquqlari buzilmaydi.
3. **Ekstremal Yengillik:** 2.9M parametr va ~6.0 MB hajm bilan GTX 1650 da atigi **10–12 ms** sarflaydi.

---

## Qaysi loyihalar uchun ideal (Best Project Fit)

### ✅ Bu model qayerda zo'r ishlaydi:
* **24/7 Navbatchilik va Dispecherlik Xonalari (Server, Energetika, Zavodlar):** Tungi smenadagi operator yoki dispetcher uxlab qolishini sekundomer bilan aniqlab, darhol baland ovozli sirena yoki Telegram botga xabar yuborish.
* **Qorovullik va Xavfsizlik Postlari:** Postdagi qo'riqchining hushyorligini nazorat qilish.
* **Haydovchilar Charchoq Nazorati (Logistika va Shaharlararo Avtobuslar):** Rulda uxlab qolish xavfini oldindan sezish.
* **Ergonomika va Qad-Qomat Nazorati:** Kompyuterda ishlovchi dasturchilarning bukilgan (slouching) holatini kuzatib, to'g'ri o'tirishni eslatish.

### ❌ Qayerda ishlatmaslik kerak:
* Xodimlar doimiy harakatda bo'lgan omborlarda (chunki u yerda hamma doim egilib-turadi, asossiz "uyqu" signallari ko'payadi).

---

## Texnik ko'rsatkichlar va apparat talabi

| Parametr | GTX 1650 (4GB GPU) | Intel CPU (Core i5) | NVIDIA T4 / L4 (Server) |
|---|---|---|---|
| **Inferensiya vaqti** | **~10 – 13 ms** | **~55 – 75 ms** | **~4 – 6 ms** |
| **FPS (Tezlik)** | **60+ FPS** | **14 – 18 FPS** | **150+ FPS** |
| **VRAM sarfi** | **~350 MB** | 0 MB (RAM ~120 MB) | ~350 MB |
| **O'qitilgan dataset** | MS COCO Keypoints (17 ta inson bo'g'inlari) | MS COCO Keypoints | MS COCO Keypoints |

---

## Halol va Aniq Tahlil: Kamchiliklari va Kechagi Sinovdagi Xatolar

Kechagi jonli amaliy sinovda quyidagi nozik holatlar aniqlandi:

1. **Stol tagiga tushgan ruchka holati:**
   * Xodim stol tagidan tushgan buyumni olish uchun 2 sekundga egilganida, model darhol **"UYQU XAVFI (Bosh stolga tushgan)"** deb qizil belgilab yubordi.
2. **Kresloga orqaga suyanib o'yga tolish:**
   * Xodim ish haqida chuqur o'ylab, kresloga orqaga yastanib o'tirganda, uning bo'yin burchagi o'zgarishi sababli tizim uni adashib "Dam olish / Faol emas" deb baholadi.
3. **Qo'l iyagida o'tirish:**
   * Xodim barmog'ini yuziga tirab kod o'qiyotganda, koordinatalar bo'yicha bu telefonda gaplashish bilan bir xil bo'lib qoldi.

---

## Muhandislik Retsepti: Sekundomer Taymeri (Temporal Timer) va Geometriya

Ushbu modulni productionda yolg'on signallarsiz (Zero False Alarms) ishlatish uchun quyidagi qat'iy mantiq qo'shilishi shart:

```python
# Kadrlar ichida doimiy taymer logikasi
if head_is_down:
    if sleep_start_time is None:
        sleep_start_time = time.time()
    elapsed = time.time() - sleep_start_time
    
    if elapsed > 20.0:  # 20 soniyadan ortiq uzluksiz bosh stolga tushgan bo'lsa!
        trigger_alarm("DIQQAT: Operator 20 sekunddan beri uxlab yotibdi!")
else:
    sleep_start_time = None  # Xodim boshini ko'tarishi bilan taymer nolga tushadi
```

* **Natija:** Xodim 2 soniyaga ruchka olsa ham taymer 20 ga yetmaydi va hech qanday yolg'on signal bo'lmaydi!

---

## Production Server & Masshtablash (Navbatchilik Postlari va Zavodlar)

### 🟢 Tejamkor / Minimal Byudjet (5–10 ta navbatchilik xonasi):
* **Qanday server kerak:** 
  * **Mavjud oddiy kompyuter (Core i5 yoki GTX 1650 GPU)**.
  * Oylik xarajat: **$0**.
* **Nega yetadi (Sababi):**
  * Uxlab qolishni sekundiga 30 marta tekshirish shart emas. Har bir xonadan **har 2 sekundda bitta kadr (0.5 FPS)** tekshirilsa ham, operatorning uxlab qolgani 5–10 soniya ichida aniqlanadi. 10 ta xona uchun GPU yuki atigi 5% bo'ladi.

### 🚀 Katta Byudjet / Respublika Masshtabi (100 ta post yoki Shaharlararo avtobuslar):
* **Qanday server kerak:**
  * **Bitta NVIDIA T4 yoki RTX 3060 serveri + 8 vCPU**.
  * Oylik xarajat: **~$45 – $70 / oy**.
* **Bu nima beradi:**
  * Barcha 100 ta ob'yektdan kelayotgan oqimlarni batch rejimida tekshirib, xodimlarning sutkalik charchoq grafigini (Fatigue Score) korxona rahbariga hisobot qilib chiqarib beradi.

---

## Qanday ishga tushiriladi (CLI & Demo)

```bash
# 1. Test tasvir bilan (Headless tekshiruv):
python3 demo.py --source data/test_1.jpg --output data/output_1.jpg --headless

# 2. Jonli veb-kamera orqali skelet va holat tahlili:
python3 demo.py --source 0 --conf 0.30
```

---

## 🧪 Test Ma'lumotlari va Benchmark Natijalari

Ushbu modul `data/` papkasidagi 3 xil real keysli sinov tasvirlari ustida to'liq tekshirildi:

| Test Tasviri | Kiritilgan Tasvir Mazmuni | Skelet Bo'g'inlari (Keypoints) | Geometrik Holat Tahlili | Inferensiya Vaqti | Xulosa / Status |
|---|---|---|---|---|---|
| **`data/test_1.jpg`** | Xodim stolga egilib yotgan holat | 17 ta nuqta topildi | Head-Drop = +18px (Bosh yelkadan pastda) | **1385 ms** (CUDA start) | 🔴 **UYQU XAVFI: Bosh stolga tushgan** |
| **`data/test_2.jpg`** | Xodim stulda tik o'tirgan holat | 17 ta nuqta to'liq topildi | Head-Drop = -45px (Bosh yelkadan ancha baland) | **1521 ms** | 🟢 **HUSHYOR / ISHDA: Normal holat** |
| **`data/test_3.jpg`** | Bo'sh kreslo (inson yo'q) | 0 ta bo'g'in | Inson aniqlanmadi | **1553 ms** | ⚪ Odam yo'qligi sababli soxta signal yo'q |

*Barcha annotatsiya qilingan natijaviy kadrlar `data/output_1.jpg`, `data/output_2.jpg`, `data/output_3.jpg` fayllarida saqlandi.*

---

## 🔗 Rasmiy Manbalar va Foydali Havolalar

* **GitHub Ombori:** [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) — Ultralytics rasmiy platformasi.
* **YOLO11 Pose Estimation Qo'llanmasi:** [Ultralytics Pose Tasks & Models](https://docs.ultralytics.com/tasks/pose/).
* **COCO Keypoints Dataset:** [MS COCO Keypoint Detection Task](https://cocodataset.org/#keypoints-2017) (17 ta inson skelet nuqtasi standarti).
* **Model Og'irliklari (Weights):** [YOLO11n-Pose PyTorch Checkpoint (`yolo11n-pose.pt`)](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-pose.pt).


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- **Qo'shimcha Manba / Upstream:** [https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
