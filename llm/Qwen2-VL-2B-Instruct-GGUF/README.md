# Qwen2-VL-2B-Instruct (GGUF) — Multimodal Texnik Hisobot va Ishlab Chiqarish Tahlili

> **100-OpenSource-Models-Review | Model #43**  
> **Kategoriya:** Katta Multimodal Modellari (VLM — Vision-Language Model)  
> **Tashkilot:** Alibaba Cloud (Qwen Team, Xitoy)  
> **Kontekst hajmi:** **32,768 token** (Dynamic Resolution ViT, 2D RoPE)  
> **Format:** GGUF (`Q4_K_M` ~1.42 GB + `mmproj-f16` ~1.33 GB, Jami: ~2.75 GB)  
> **Inference Dvigateli:** `llama.cpp` (`Qwen25VLChatHandler` orqali)

---

## 1. Model Arxitekturasi va "Killer Feature"

Qwen2-VL-2B — ochiq manbali sun'iy intellekt olamidagi eng yetakchi ixcham multimodal (ko'rish va til) modellaridan biridir. U matn bilan bir qatorda tasvirlarni, skaner qilingan hujjatlarni va video kadrlarni tushunish imkonini beradi:

1. **Dinamik Ruxsatli Vision Transformer (Dynamic Resolution ViT):** An'anaviy VLM lardan farqli ravishda (tasvirni 224x224 yoki 384x384 gacha majburiy kvadratga siqib tashlaydigan), Qwen2-VL tasvirning asl proporsiyasini saqlab qoladi va uni patch'larga ajratadi.
2. **2D RoPE (Rotary Position Embeddings):** Vizual tokenlar koordinatalarini (x, y) fazoviy tekislikda kodlaydi, bu esa obyektlarning nisbiy joylashuvi va mayda detallarini aniqlash imkonini beradi.
3. **Qurilma / Brend Tanish (Fine-grained Recognition):** Oddiy kichik modellardan farqli o'laroq, tasvirdagi elektronika va jihozlarni brendigacha (masalan: *Logitech klaviaturasi*, *iPad*, *iPhone*) aniqlay oladi.
4. **Ixcham Hajm va CPU Qulayligi:** Matn modeli (`Q4_K_M`) va vizual proyektor (`mmproj-f16`) birgalikda atigi **~3.2 GB RAM** sarflaydi.

---

## 2. Uskuna Talablari va Infratuzilma (Hardware Sizing)

| Konfiguratsiya | Minimal Talab (CPU) | Optimal Ishlab Chiqarish (GPU) |
|---|---|---|
| **RAM (Operativ xotira)** | **8 GB DDR4** | **8 GB tizim RAM** |
| **VRAM (Video xotira)** | Talab etilmaydi (CPU rejimi) | **4 GB – 6 GB VRAM** (GTX 1650, RTX 3050/3060) |
| **Disk maydoni** | ~2.8 GB (`model.gguf` + `mmproj.gguf`) | ~2.8 GB |
| **ViT Tasvirni Kodlash Vaqti** | CPU'da **~55–65 soniya** (1036x672 piksel) | GPU'da **~0.3–0.8 soniya** (CUDA offload) |
| **Matn Generatsiya Tezligi** | CPU'da ~2.5–3.0 tok/s | GPU'da ~30–45 tok/s |

> [!WARNING]
> **CPU Latency Diqqat Markazida:** Tasvirni patchlarga ajratib ViT orqali kodlash (`clip_encode`) 6 ta CPU thread'da ~55-65 soniya vaqt oladi. Shu sababli real vaqtli (real-time CCTV) monitoring uchun **GPU offload** (`-ngl 33`) shart!

---

## 3. Empirik Benchmark Natijalari (Haqiqiy Sinov Telemetriyasi)

Sinovlar multimodal test tasvirlari bilan mahalliy serverda (CPU 6 thread, `n_ctx=4096`, Docker konteynerida `llama.cpp` + `Qwen25VLChatHandler`) o'tkazildi:

| Test Nomi | Tasvir Fayli | Vaqt (s) | Tokenlar | Tezlik (tok/s) | Natija / Xulosa |
|---|---|---|---|---|---|
| **Test 1: Traffic Scene VQA** | `test_intersection.jpg` (1036x672) | 76.53 s | 115 | **1.50 tok/s** | ✅ **Mukammal:** 6+ avtomobil, yorug'lik, piyodalar yo'li |
| **Test 2: Office Workspace Audit** | `test_office.jpg` (980x700) | 76.32 s | 209 | **2.74 tok/s** | ✅ **SOTA Tafsilot:** Logitech klaviatura va iPad brendlarini tanidi |
| **Test 3: Spatial Reasoning** | `test_intersection.jpg` (1036x672) | 65.30 s | 0 | **0.00 tok/s** | ⚠️ **Grounding Sintaksis Xatosi:** 0 token bilan to'xtadi |
| **Test 4: Uzbek Multimodal VQA** | `test_office.jpg` (980x700) | 84.12 s | 216 | **2.57 tok/s** | ❌ **ECHOLALIA TUZOG'I:** Savolni javob sifatida qaytarib yozdi |

---

## 4. Testlar Tahlili va Aniqlangan Kritik Muhandislik Saboqlari

### Test 1: Yo'l Harakati Chorrahasi Tahlili (`test_intersection.jpg`)
- **Vazifa:** Avtotransport vositalarini sanash, yorug'lik va ob-havo holati, piyodalar va xavfsizlik tahlili.
- **Model Tahlili:** Model 888 ta vizual token orqali tasvirni aniq tahlil qildi:
  - Kamida 6 ta avtomobil va yuk mashinasi borligini, ular ko'cha bo'ylab harakatlanayotgani yoki to'xtab turganini aniqladi.
  - Tabiiy yorug'lik, quyosh nuri daraxtlar orasidan tushayotgani, osmon bulutli ekanini ko'rsatdi.
  - Yo'l chetidagi piyodalar va piyodalar o'tish joyini to'g'ri qayd etdi.

### Test 2: Ofis Ish Joyi Auditi (`test_office.jpg`)
- **Vazifa:** Elektronika va mebellarni sanash, ish joyi bandligi va tartibini baholash.
- **Model Tahlili:** 2B hajmdagi model uchun hayratlanarli darajada yuqori aniqlik ko'rsatdi:
  - *"iPad: oq rangli, foydalanish holatida"*
  - *"Keyboard: Logitech klaviaturasi, oq g'ilofga biriktirilgan"* (klaviatura brendini to'g'ri o'qidi!)
  - *"Cell Phone: qora rangli aks etuvchi smartfon, ehtimol iPhone"*
  - Ish joyi egallanganligi va foydalanuvchi faol ishlayotganini to'g'ri aniqladi.

### Test 3: Fazoviy Koordinatalar va Grounding Xatosi (0 Token Anomaliyasi)
- **Muammo:** Bounding box koordinatalarini erkin matnda so'raganimizda, model darhol generatsiyani to'xtatib (`<|im_end|>`), 0 token qaytardi.
- **Sababi:** Qwen2-VL modelida obyekt koordinatalari oddiy inglizcha jumlalar orqali emas, balki maxsus grounding tokenlari bilan o'qitilgan:
  - Format: `<|box_start|>(y1,x1),(y2,x2)<|box_end|>` yoki `<ref>object</ref><box>(...)</box>`.
  - Erkin matnli promptda grounding formati aniq ko'rsatilmaganda, model noaniqlik sababli generatsiyani yakunlab qo'yadi.

### Test 4: O'zbek Tili va Echolalia Tuzog'i (Kritik Kamchilik)
- **Sinov:** Modelga ofis rasmi berilib, o'zbek tilida savol berildi.
- **Model Qaytargan Javob:**
  > *"1. Suratda qanday joy va qanday asosiy jihozlar yoki ob'ektlar aks etgan: Suratda qanday joy va qanday asosiy jihozlar yoki ob'ektlar aks etgan."*  
  > *"2. Xona/muhit holati qanday: tartibli va ishga tayyormi yoki bo'sh va qarovsizmi? Xona/muhit holati tartibli va ishga tayyormi."*  
  > *"3. Tasvir bo'yicha qisqacha xulosa... Tasvir bo'yicha qisqacha xulosa..."*
- **Tahlil (Nima uchun bu sodir bo'ldi?):**
  - Qwen2-VL-2B modeli Qwen2.5 emas, balki oldingi avlod Qwen2 arxitekturasiga asoslangan.
  - Modelning ko'rish (vision-text alignment) qatlami deyarli faqat **ingliz va xitoy** tillaridagi tasvir-matn juftliklarida o'qitilgan.
  - Kontekstga 875 ta og'ir vizual token kirib kelganda, kichik 2B modelning o'zbek tili e'tibor qobiliyati (attention) buziladi va u tasvirni tahlil qilish o'rniga, **savol matnini takrorlab berish (echolalia)** sindromiga chalinadi.

---

## 5. Ishlab Chiqarish Qarorlar Matritsasi (Team Lead uchun)

```
                            ┌──────────────────────────────────────────────┐
                            │   Tasvirlar bilan qanday vazifa bajariladi?  │
                            └──────────────────────┬───────────────────────┘
                                                   │
                     ┌─────────────────────────────┴─────────────────────────────┐
                     ▼                                                           ▼
         [ Inglizcha VQA, Hujjat, Brend Tanib Olish ]                [ To'g'ridan-to'g'ri O'zbekcha Prompt ]
                     │                                                           │
        ┌────────────┴────────────┐                                              ▼
        ▼                         ▼                                     🛑 QAT'IYAN TAQIQLANADI!
 [ Server / GPU Mavjud ]   [ Faqat CPU / Edge Device ]                 (Echolalia: savolni o'zini qaytaradi)
        │                         │                                              │
        ▼                         ▼                                              ▼
 ✅ QWEN2-VL-2B IDEAL      ⚠️ ISHLAYDI, AMMO:                          Yechim: 2-Bosqichli Pipeline
 (Yuqori aniqlik, 0.5s)    Tasvir kodi ~60s oladi!                     (Inglizcha VQA -> Qwen2.5 O'zbekcha)
```

### Qachon Ishlatish Kerak (Best Cases):
1. **Vizual Hujjatlar va Cheklar Auditi (OCR + VQA):** Kvitansiyalar, hisob-fakturalar, texnik pasportlar va diagrammalardan aniq ma'lumotlarni chiqarib olish (ingliz/rus/xitoy tillarida).
2. **Ob'ektlar va Tovar Inventarizatsiyasi:** Savdo rastalari, ofis jihozlari va ko'cha kameralari tahlili.
3. **Smartfon va Edge Device:** 3 GB RAM sarfi bilan qurilmaning o'zida internet-siz vizual tahlil qilish.

### Qachon Ishlatish Mumkin Emas:
1. **To'g'ridan-to'g'ri O'zbekcha Vizual Savol-Javob:** Model tasvirga qaramay, berilgan o'zbekcha savolni o'ziga takrorlab beradi.
2. **GPU'siz Real-vaqtli Video Tahlili (CCTV FPS):** CPU'da 1 ta kadrni qayta ishlash ~60-75 soniya oladi.

---

## 6. O'zbekiston Loyihalari Uchun Tavsiya Etilgan Ishlab Chiqarish Arxitekturasi

Agar mijoz O'zbekistonda skaner qilingan shartnomalarni yoki xavfsizlik kameralarini o'zbek tilida tahlil qilishni xohlasa:

```
[ Foydalanuvchi Tasviri + O'zbekcha So'rov ]
                     │
                     ▼
       [ 1-Bosqich: Qwen2.5-1.5B Matn Modeli ]
       (O'zbekcha so'rovni inglizcha aniq VQA promptiga o'giradi)
                     │
                     ▼
       [ 2-Bosqich: Qwen2-VL-2B Multimodal ]
       (Tasvirni ingliz tilida chuqur tahlil qilib, JSON/faktlarni chiqaradi)
                     │
                     ▼
       [ 3-Bosqich: Qwen2.5-1.5B Matn Modeli ]
       (Inglizcha faktlarni ravon va mukammal o'zbek tilida foydalanuvchiga taqdim etadi)
```

---

## 7. Modelni Ishga Tushirish

### Bitta tasvirni tahlil qilish:
```bash
docker compose run --rm qwen2_vl_2b_instruct_gguf python3 demo.py \
  --image data/test_office.jpg \
  --prompt "List all electronic devices and describe the desk setup."
```

### Multimodal benchmarklarni qayta ishga tushirish:
```bash
docker compose run --rm qwen2_vl_2b_instruct_gguf python3 run_benchmarks.py
```
