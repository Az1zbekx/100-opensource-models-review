# Moondream2 (GGUF) — Ultra-Ixcham Chekka VLM Texnik Hisobot va Ishlab Chiqarish Tahlili

> **100-OpenSource-Models-Review | Model #44**  
> **Kategoriya:** Ultra-Ixcham Vision-Language Modeli (Tiny Edge VLM)  
> **Muallif:** Vikhyat Korrapati / Moondream  
> **Parametrlar soni:** **1.86B** (SigLIP Vision Encoder + Phi-1.5/2 Backbone)  
> **Format:** GGUF (`moondream2-text-model-f16` ~1.0 GB + `moondream2-mmproj-f16` ~880 MB)  
> **Inference Dvigateli:** `llama.cpp` (`MoondreamChatHandler` orqali)

---

## 1. Model Arxitekturasi va "Killer Feature"

Moondream2 — chekka qurilmalar (Edge devices, Raspberry Pi 4/5, mini-kompyuterlar, smartfonlar va dronlar) uchun noldan maxsus optimallashtirilgan dunyodagi eng tezkor va ixcham multimodal sun'iy intellekt modelidir.

1. **SigLIP Kvadrat Tasvir Enkoderi (378x378):** Og'ir dinamik rezolyutsiyali ViT modellardan (masalan, Qwen2-VL) farqli o'laroq, Moondream2 tasvirni 378x378 pikselli qat'iy SigLIP enkoderi orqali qayta ishlaydi. Natijada tasvirni kodlash CPU'da **bor-yo'g'i 3.6 soniya** oladi (Qwen2-VL da 58.7 soniya!).
2. **16x Yuqori CPU Tezligi:** Katta VLM lardan 16 barobar tezroq kadr tahlili amalga oshiriladi, bu esa zaif CPU protsessorlarida ham real monitoring imkonini beradi.
3. **Ekstremal Kichik Xotira:** Model va proyektor birgalikda operativ xotiradan (RAM) atigi **~1.8 – 2.2 GB** joy egallaydi.
4. **Aniq Detallashtirish va "Ha/Yo'q" Savollari:** Tasvirda monitor, stul, avtomobillar rangi va odamlar bor-yo'qligini tezkor tasdiqlash uchun ayni muddao.

---

## 2. Uskuna Talablari va Infratuzilma (Hardware Sizing)

| Konfiguratsiya | Minimal Chekka Qurilma (Raspberry Pi 4/5) | Oddiy Noutbuk / Server (CPU) |
|---|---|---|
| **RAM (Operativ xotira)** | **4 GB RAM** (Bo'sh joy: 2.2 GB) | **8 GB tizim RAM** |
| **VRAM (Video xotira)** | Talab etilmaydi (Faqat CPU) | Talab etilmaydi (ixtiyoriy 2 GB VRAM) |
| **Disk maydoni** | ~1.9 GB (Ikkala GGUF fayl) | ~1.9 GB |
| **ViT Tasvirni Kodlash Vaqti** | ~7–10 soniya (ARM Cortex) | **~3.6 soniya** (Intel/AMD x86 CPU) |
| **Inference Tezligi** | ~5–8 tok/s | ~15–25 tok/s |

---

## 3. Empirik Benchmark Natijalari (Haqiqiy Sinov Telemetriyasi)

Sinovlar mahalliy serverda (AMD/Intel CPU, 6 thread, `n_ctx=2048`, Docker konteynerida `llama.cpp` + `MoondreamChatHandler`) o'tkazildi:

| Test Nomi | Tasvir Fayli | Vaqt (s) | Tokenlar | Tezlik (tok/s) | Natija / Xulosa |
|---|---|---|---|---|---|
| **Test 1: Quick Scene Caption** | `test_intersection.jpg` (1036x672) | 14.57 s | 16 | **1.10 tok/s** | ✅ **Mukammal:** Bitta lo'nda jumla bilan holatni aniq tavsifladi |
| **Test 2: Vehicle Color QA** | `test_intersection.jpg` (1036x672) | 12.68 s | 3 | **0.24 tok/s** | ✅ **Aniq va qisqa:** *"White and black"* ranglarini to'g'ri aytdi |
| **Test 3: Office Presence Audit** | `test_office.jpg` (980x700) | 16.21 s | 36 | **2.22 tok/s** | ✅ **SOTA Farqlash:** Monitor yo'qligini, planshet/klaviatura borligini bildi |
| **Test 4: Uzbek Edge VQA** | `test_office.jpg` (980x700) | 13.24 s | 1 | **0.08 tok/s** | ❌ **KO'R NUQTA (Blind Spot):** O'zbekcha savolga faqat *"Yes"* deb javob berdi |

---

## 4. Testlar Tahlili va Kritik Muhandislik Saboqlari

### Test 1: Tezkor Sahna Tavsifi (`test_intersection.jpg`)
- **Vazifa:** Bir jumla bilan asosiy voqeani xulosa qilish.
- **Model Natijasi (14.5s):**
  > *"A crosswalk with a stop sign and a sign that says do not enter."*
- **Muhandislik Xulosasi:** Model keraksiz so'zlarsiz chorrahadagi piyodalar yo'lagi (crosswalk) va belgilarini bitta aniq jumlada ifodaladi. Kadrni tahlil qilish va javob berish atigi 14 soniya oldi.

### Test 2: Avtomobillar Rangi Bo'yicha Savol-Javob
- **Vazifa:** Old plandagi mashinalar rangini aniqlash.
- **Model Natijasi (12.6s):** *"White and black"* (3 token).
- **Muhandislik Xulosasi:** Model to'g'ridan-to'g'ri faktni aytdi (oq va qora avtomobillar).

### Test 3: Ish Joyi Inventari — Monitor va Stul Tekshiruvi (`test_office.jpg`)
- **Vazifa:** Stol ustida monitor va stul bormi?
- **Model Natijasi (16.2s):**
  > *"No, there is no office chair and monitor visible on the desk. The person is sitting at a desk with a tablet and a smartphone, and they are also holding a keyboard."*
- **Ajoyib Farqlash:** Ko'pgina modellar iPad'ni ko'rib uni "monitor" deb adashadi. Moondream2 esa uning alohida monitor emas, planshet (tablet) ekanini, foydalanuvchi klaviatura va smartfon bilan ishlayotganini aniq ajrata oldi!

### Test 4: O'zbek Tili Sinovi — "Faqat Ingliz Tili" Cheklovi (Blind Spot)
- **Vazifa:** *"Ushbu tasvirda nimalar bor? Stol ustida qanday narsalar ko'rinib turibdi? Qisqa va lo'nda javob bering."*
- **Model Natijasi (13.2s):** *"Yes"* (1 token).
- **Sababi:**
  - Moondream2 modelining matn o'zagi (backbone) juda kichik (~1.4B Phi-1.5) bo'lib, u faqat ingliz tilidagi tasvir tavsiflari (captioning) va inglizcha VQA korpuslarida o'qitilgan.
  - Model o'zbek tili lug'atini (vocabulary) tushunmaydi. Natijada har qanday notanish tildagi so'rovga shunchaki generatsiyani 1-token bilan to'xtatuvchi standart so'zni (`Yes`) qaytaradi.

---

## 5. Qwen2-VL-2B va Moondream2 Taqqoslama Matritsasi

| Mezon | Qwen2-VL-2B-Instruct | Moondream2 | Qaysi biri qachon tanlanadi? |
|---|---|---|---|
| **Tasvirni kodlash (ViT Latency CPU)** | ~58.7 soniya (Sekin) | **~3.6 soniya (16x Tezkor!)** | **Tezlik kerak bo'lsa: Moondream2** |
| **RAM sarfi** | ~3.0 – 3.2 GB | **~1.8 – 2.0 GB** | **Raspberry Pi / Edge: Moondream2** |
| **Tasvir Ruxsati (Resolution)** | Dinamik (Yuqori sifat, OCR) | 378x378 kvadrat (Siqilgan) | **Kichik matn/Hujjat: Qwen2-VL** |
| **Brend va Matnlarni O'qish** | Yuqori (Logitech, iPad brendlari) | O'rtacha (Umumiy toifalar) | **Chuqur audit: Qwen2-VL** |
| **Ko'p tilli qo'llab-quvvatlash** | Xitoy, Ingliz, Rus tillari | **Faqat Ingliz tili** | **Ko'p tillilik: Qwen2-VL** |

---

## 6. Ishlab Chiqarish Qarorlar Matritsasi (Team Lead uchun)

```
                            ┌──────────────────────────────────────────────┐
                            │    VLM Ishga Tushiriladigan Qurilma Qanday?   │
                            └──────────────────────┬───────────────────────┘
                                                   │
                     ┌─────────────────────────────┴─────────────────────────────┐
                     ▼                                                           ▼
       [ Kuchli Server / GPU Mavjud ]                               [ Chekka Qurilma / Zaif CPU / IoT ]
                     │                                                           │
        ┌────────────┴────────────┐                                 ┌────────────┴────────────┐
        ▼                         ▼                                 ▼                         ▼
 [ Mayda Hujjat / OCR ]   [ Inglizcha VQA ]                 [ Inglizcha Tezkor VQA ]   [ O'zbek Tili Kerak ]
        │                         │                                 │                         │
        ▼                         ▼                                 ▼                         ▼
 ✅ QWEN2-VL-2B           ✅ QWEN2-VL-2B                    ✅ MOONDREAM2 IDEAL        🛑 MOONDREAM2 ISHLAMAYDI!
 (Dinamik ruxsat)         (Maksimal tafsilot)               (Atigi 3.6s, 1.8GB RAM)   (Faqat "Yes" deb qaytaradi)
```

### Qachon Ishlatish Kerak (Ideal Cases):
1. **Dronlar va Robototexnika:** Real vaqtda yo'ldagi to'siqlarni, eshiklar ochiq/yopiqligini, xonada odam bor-yo'qligini tekshirish.
2. **Smart Home va Xavfsizlik Kameralari (Edge):** Raspberry Pi yoki mini-kompyuterda serverga ulanmasdan turib: *"Avtomobil turibdimi?"*, *"Eshik oldida posilka bormi?"* kabi savollarga bir zumda javob olish.
3. **Cheklangan Xotira (RAM < 3 GB):** Katta VLM larni ko'tara olmaydigan yengil mikrotizimlar.

### Qachon Ishlatish Mumkin Emas:
1. **O'zbek Tilidagi Loyihalar:** Model o'zbek tilidagi so'rovlarga javob bera olmaydi (faqat inglizcha ishlaydi).
2. **Mayda Matnli Hujjatlar / Cheklar (OCR):** Tasvir 378x378 ga siqilgani sababli, kichik raqamlar va matnlar o'qilmaydi.

---

## 7. Modelni Ishga Tushirish

### Bitta tasvir bilan savol berish:
```bash
docker compose run --rm moondream2_gguf python3 demo.py \
  --image data/test_intersection.jpg \
  --prompt "What colors of vehicles are visible in the foreground?"
```

### Interaktiv VLM sessiyasi:
```bash
docker compose run --rm moondream2_gguf python3 demo.py --chat
```

### Benchmarklarni qayta ishga tushirish:
```bash
docker compose run --rm moondream2_gguf python3 run_benchmarks.py
```


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://huggingface.co/vikhyatk/moondream2](https://huggingface.co/vikhyatk/moondream2)
- **Qo'shimcha Manba / Upstream:** [https://github.com/vikhyat/moondream](https://github.com/vikhyat/moondream)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
