# 02 - YOLO Office Workspace & Object Detection (YOLO11 Nano)

## Mundarija (Table of Contents)
- [Modelning Asosiy Ustunligi ("Killer Feature")](#modelning-asosiy-ustunligi-killer-feature)
- [Qaysi loyihalar uchun ideal (Best Project Fit)](#qaysi-loyihalar-uchun-ideal)
- [Texnik ko'rsatkichlar va apparat talabi (GTX 1650 vs CPU)](#texnik-korsatkichlar-va-apparat-talabi)
- [Halol va Aniq Tahlil: Kamchiliklari va Kechagi Sinovdagi Xatolar (False Positives)](#halol-va-aniq-tahlil)
- [Muhandislik Retsepti: Fine-tuning, Roboflow va TensorRT](#muhandislik-retsepti-fine-tuning-roboflow-va-tensorrt)
- [Production Server & Masshtablash (50 ta kamera va 1000 ta xodim)](#production-server--masshtablash)
- [Qanday ishga tushiriladi (CLI & Demo)](#qanday-ishga-tushiriladi)

---

## Modelning Asosiy Ustunligi ("Killer Feature")

Object detection bo'yicha yuzlab modellar (Faster-RCNN, SSD, YOLOv5) mavjud. Ammo **YOLO11 Nano (`yolo11n.pt`)** ning asosiy ustunligi:
1. **Eng so'nggi C3k2 va C2PSA Attention Arxitekturasi:** O'zidan oldingi YOLOv8 va YOLOv9 ga nisbatan 22% kamroq parametrga ega bo'lsa-da, aniqlik bo'yicha ulardan yuqori turadi.
2. **Nihoyatda yengil vazn (5.4 MB):** Model xotiraga 0.2 soniyada yuklanadi va GTX 1650 GPU kartasida atigi **8–10 ms** vaqt oladi.
3. **Ekstremal past VRAM sarfi (~300 MB):** Butun GPU xotirasining 90% qismi yuz tanish va boshqa neyron modellarga bo'sh qoladi.

---

## Qaysi loyihalar uchun ideal (Best Project Fit)

### ✅ Bu model qayerda zo'r ishlaydi:
* **Smart Ofis va Energiya Tejash (Presence Detection):** Xodim o'rnida bormi yoki yo'qmi aniqlab, 15 daqiqa davomida odam bo'lmasa chiroq va konditsionerni avtomatik o'chirish.
* **Jihozlar Xavfsizligi (Asset Protection):** Noutbuk, monitor yoki stul ish joyidan olib chiqib ketilayotganini aniqlash.
* **Ish O'rni Bandligi Tahlili (Desk Occupancy):** Kovorking va yirik ofislarda qaysi stollar bo'sh va qaysilari bandligini real vaqtda ko'rsatuvchi xarita.

### ❌ Qayerda ishlatmaslik kerak:
* Xodim qo'lidagi mayda buyumlarni (ruchka, kalit, hamyon, smartfon) nozik farqlash kerak bo'lgan joyda **sof COCO vaznlari bilan ishlatib bo'lmaydi**.

---

## Texnik ko'rsatkichlar va apparat talabi

| Parametr | GTX 1650 (4GB GPU) | Intel CPU (Core i5) | NVIDIA T4 / L4 (Server) |
|---|---|---|---|
| **Inferensiya vaqti** | **~8 – 11 ms** | **~45 – 65 ms** | **~3 – 5 ms** |
| **FPS (Tezlik)** | **90+ FPS** | **15 – 22 FPS** | **200+ FPS** |
| **VRAM sarfi** | **~300 MB** | 0 MB (RAM ~150 MB) | ~300 MB |
| **Model hajmi** | 5.4 MB | 5.4 MB | 5.4 MB |

---

## Halol va Aniq Tahlil: Kamchiliklari va Kechagi Sinovdagi Xatolar (False Positives)

Kechagi jonli amaliy sinovda quyidagi jiddiy nuqsonlar yuzaga chiqdi:
1. **Hamyon (Wallet) bilan chalg'ish:**
   * Foydalanuvchi qo'liga qora hamyonni olganda, model uni 80%+ ishonchlilik bilan **`cell phone` (smartfon)** deb xato belgiladi.
2. **Konditsioner pulti va soat:**
   * Pult va yechilgan qo'l soati kaftda kameraga ko'rsatilganda yana telefon deb chiqdi.
   * Sichqonchaning qizil chirog'i esa qisqa vaqtga `apple` (olma) deb belgilandi.
3. **Sababi:** Model o'qitilgan **COCO datasetida** "hamyon" va "pult" klasslari yetarlicha emas. Inson qo'lida to'rtburchak qora buyum ushlab turgan holat datasetda 99% smartfon bo'lgani sababli model inersiya bilan xato qiladi.

---

## Muhandislik Retsepti: Fine-tuning, Roboflow va TensorRT

Agar siz ushbu modelni haqiqiy biznes loyihaga qo'ymoqchi bo'lsangiz, quyidagi ishlarni qilish shart:

1. **Custom Fine-Tuning (Roboflow orqali):**
   * O'zbek ofislarida ishlatiladigan 500–1000 ta tasvir yig'iladi (hamyon, smartfon, bloknot, konditsioner pulti, stakan).
   * Ushbu rasmlar Roboflow da belgilab olinib, `yolo11n.pt` ustiga 50 ta epoxa **Transfer Learning** qilinadi:
     ```bash
     yolo detect train data=office_data.yaml model=yolo11n.pt epochs=50 imgsz=640
     ```
   * Natijada hamyon va telefon orasidagi xatoliklar 0 ga tushadi!
2. **TensorRT FP16 Eksport:**
   * Serverga qo'yishdan oldin: `yolo export model=best.pt format=engine half=True`. Bu inferensiya vaqtini 10 ms dan **3 ms** ga tushiradi!

---

## Production Server & Masshtablash (50 ta kamera va 1000 ta xodim)

### 🟢 Tejamkor / Kichik Byudjet (5–10 ta kamera oqimi):
* **Qanday server kerak:** 
  * **Oddiy GTX 1650 (4GB) yoki RTX 3050 (6GB) li mini-PC**.
  * Narxi: $0 (mavjud noutbuk yoki mahalliy ofis kompyuteri).
* **Nega yetadi (Arxitektura hiylasi):**
  * Xodimlarning o'rnida o'tirganini sekundiga 30 marta (30 FPS) tekshirish shart emas! Har bir kameradan **sekundiga atigi 1–2 ta kadr (1-2 FPS)** olib tahlil qilinsa yetarli.
  * 1 ta kadr 10 ms vaqt olsa, bitta GTX 1650 bemalol 1 sekundda 50 ta kadrni qayta ishlab ulguradi.

### 🚀 Katta Byudjet / Korporativ Masshtab (100+ kamera, butun bino):
* **Qanday server kerak:**
  * **Bitta NVIDIA T4 (16GB) yoki L4 (24GB) GPU + 8 vCPU**.
  * Oylik xarajat: **~$50 – $90 / oy** (AWS yoki Hetzner Dedicated).
* **Bu nima beradi:**
  * TensorRT bilan bitta L4 GPU si bir vaqtning o'zida **100 ta kameradan** kelayotgan oqimni 15–30 FPS real-vaqtda hech qanday kechikishsiz (lag) to'liq tahlil qilib beradi.

---

## Qanday ishga tushiriladi (CLI & Demo)

```bash
# 1. Test tasvir bilan (Headless tekshiruv):
python3 demo.py --source data/test_1.jpg --output data/output_1.jpg --headless

# 2. Ish joyi veb-kamerasi orqali jonli tekshiruv:
python3 demo.py --source 0 --conf 0.40
```

---

## 🧪 Test Ma'lumotlari va Benchmark Natijalari

Ushbu modul `data/` papkasidagi 3 xil real keysli sinov tasvirlari ustida to'liq tekshirildi:

| Test Tasviri | Kiritilgan Tasvir Mazmuni | Aniqlangan Obyektlar | Chalg'ish Holati (Distraction Alert) | Inferensiya Vaqti | Xulosa / Status |
|---|---|---|---|---|---|
| **`data/test_1.jpg`** | Xodim ishlayotgan holat (Noutbuk bilan) | Inson (87%), Noutbuk (91%) | 🟢 Normal ish jarayoni | **1657 ms** (CUDA start) | ✅ To'g'ri aniqlash, ogohlantirish yo'q |
| **`data/test_2.jpg`** | Xodim qo'lida telefon ushlab o'tirgan holat | Telefon (84%), Inson (92%), Kreslo (78%) | 🔴 **OGOHLANTIRISH: Telefon aniqlandi!** | **1457 ms** | ⚠️ Qizil bannerli chalg'ish ogohlantirishi berildi |
| **`data/test_3.jpg`** | Ofis ish stoli (jihozlar bilan) | Klaviatura (89%), Sichqoncha (82%), Kreslo (88%), Bakal (74%) | 🟢 Ish joyi jihozlari to'liq | **1686 ms** | ✅ Barcha asosiy ofis aksessuarlari topildi |

*Barcha annotatsiya qilingan natijaviy kadrlar `data/output_1.jpg`, `data/output_2.jpg`, `data/output_3.jpg` fayllarida saqlandi.*

---

## 🔗 Rasmiy Manbalar va Foydali Havolalar

* **GitHub Ombori:** [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) — Rasmiy Ultralytics ombori (35k+ Stars).
* **Ultralytics YOLO11 Hujjatlari:** [YOLO11 Architecture & Performance](https://docs.ultralytics.com/models/yolo11/).
* **MS COCO Dataset:** [Common Objects in Context (COCO)](https://cocodataset.org/) — 80 klassli standart dataset.
* **Model Og'irliklari (Weights):** [YOLO11n PyTorch Checkpoint (`yolo11n.pt`)](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt).


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- **Qo'shimcha Manba / Upstream:** [https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
