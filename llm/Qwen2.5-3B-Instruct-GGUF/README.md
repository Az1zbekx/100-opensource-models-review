# Qwen2.5-3B-Instruct (GGUF) — Texnik Hisobot va Ishlab Chiqarish Tahlili

> **100-OpenSource-Models-Review | Model #49**  
> **Kategoriya:** Katta Til Modellari (LLM) — Ko'p Tillik / "Oltin O'rtaliq" 3B  
> **Tashkilot:** Alibaba Cloud (Qwen Team, Xitoy)  
> **Kontekst hajmi:** **32,768 token** (128k gacha kengaytiriladi)  
> **O'qitilgan ma'lumot hajmi:** **18 Trillion token**  
> **Format:** GGUF (`Q4_K_M`, ~2.10 GB)  
> **Inference Dvigateli:** `llama.cpp` (CPU / GPU offload)

---

## 1. Model Arxitekturasi va "Killer Feature"

Qwen2.5-3B — zamonaviy ochiq LLM ekotizimida eng muvaffaqiyatli "oltin o'rtaliq" (sweet spot) modelidir. 1.5B modellardan farqli ravishda u ancha chuqur mantiqiy xulosalash qobiliyatiga ega, 7B-8B modellarga qaraganda esa 2 barobar kam xotira sarflaydi va 2 barobar tezroq ishlaydi:

1. **18 Trillion Tokenlik Gigant Baza:** Model zamonaviy 70B modellar kabi ulkan ma'lumotlar ustida o'qitilgan. Shu sababli ko'p tillilik, faktik bilim va dasturlash darajasi o'tgan avlod 7B modellaridan ham ustun.
2. **O'zbek Tilidagi Aniq Entitilarni Ajratish (NER & Entity Extraction):** Mijozlarning o'zbek tilidagi erkin matnli buyurtmalaridan tuman, ko'cha, uy raqami, telefon va vaqtni benuqson ajrata oladi.
3. **Mukammal Qat'iy JSON (Zero-Shot Tool Calling):** Tashqi API larni chaqirish yoki ma'lumotlar bazasiga yozish uchun berilgan JSON sxemani 100% buzmasdan qaytaradi.
4. **Resurs Tejamkorligi:** Bor-yo'g'i **~2.4 GB RAM** talab qiladi va oddiy CPU da **~15 tok/s** tezlik bilan generatsiya qiladi.

---

## 2. Uskuna Talablari va Infratuzilma (Hardware Sizing)

| Konfiguratsiya | Minimal Talab (CPU) | Optimal Ishlab Chiqarish (GPU) |
|---|---|---|
| **RAM (Operativ xotira)** | **4 GB DDR4** (Bo'sh joy: 2.5 GB) | **4 GB tizim RAM** |
| **VRAM (Video xotira)** | Talab etilmaydi (CPU rejimi) | **3 GB – 4 GB VRAM** (GTX 1650, RTX 3050) |
| **Model disk hajmi** | ~2.10 GB (`qwen2.5-3b-instruct-q4_k_m.gguf`) | ~2.10 GB |
| **KV Cache hajmi (4k/32k)** | ~210 MB (4k) | ~1.6 GB (32k) |
| **Inference Tezligi** | CPU'da **~14.5 – 15.5 tok/s** | GPU'da **~50 – 70 tok/s** |

---

## 3. Empirik Benchmark Natijalari (Haqiqiy Sinov Telemetriyasi)

Sinovlar mahalliy serverda (AMD/Intel CPU, 6 thread, `n_ctx=4096`, Docker konteynerida `llama.cpp`) o'tkazildi:

| Test Nomi | Fokus / Yo'nalish | Vaqt (s) | Tokenlar | Tezlik (tok/s) | Natija / Xulosa |
|---|---|---|---|---|---|
| **Test 1: Database Internals** | PostgreSQL B-Tree, GIN va BRIN indekslari taqqoslash jadvali | 19.27 s | 290 | **15.05 tok/s** | ✅ **Mukammal:** Aniq va to'liq Markdown jadval |
| **Test 2: Uzbek Business Dilemma** | Toshkent shahridagi tig'iz payt yetkazib berish muammosi | 54.41 s | 800 (max) | **14.70 tok/s** | ⚠️ **Repetition Trap:** Past temperaturada n-gram sikliga tushdi |
| **Test 3: Logic Deduction** | Formal kategorik sillogizm (Barbara mantiqiy xulosasi) | 18.90 s | 274 | **14.50 tok/s** | ✅ **SOTA Mantiq:** Tranzitivlik qoidasi bilan to'g'ri isbotladi |
| **Test 4: Strict JSON Tool Calling** | O'zbekcha buyurtma xabaridan shahar, manzil, telefonni ajratish | 12.16 s | 134 | **11.02 tok/s** | ✅ **JAHON DARAJASI:** 100% toza, benuqson JSON obyekt |

---

## 4. Testlar Tahlili va Kritik Muhandislik Saboqlari

### Test 1: Ma'lumotlar Bazasi Arxitekturasi (PostgreSQL Indekslari)
- **Vazifa:** B-Tree, GIN va BRIN indekslarining farqi va qo'llanish sohalari bo'yicha jadval.
- **Model Tahlili:**
  - B-Tree: Standart saralangan ma'lumotlar, oraliq qidiruvlar (range queries).
  - GIN: Matnli qidiruv (Full-text search) va JSONB kalitlari bo'yicha qidiruv.
  - BRIN: Katta jadvallarda (Big Data) xotirani minimal sarflab oraliq qidirish.
- **Xulosa:** Muhandislik jihatidan to'liq va xatosiz.

### Test 2: O'zbek Tilidagi Biznes Muammo va "Past Harorat Tuzog'i" (Failure Analysis)
- **Muammo:** Toshkentdagi 17:00-20:00 tirbandligiga texnologik va logistik yechim so'ralganda, model quyidagi cheksiz siklga tushdi:
  > *"Yo'l Tirbandliklarni O'zrocha O'zgartirish va Qo'llash: Yo'l tirbandliklarni o'zrocha o'zgartirish va qo'llash qilish..."*
- **Nima Uchun Bu Sodir Bo'ldi? (Root Cause):**
  - Sinovda `temperature=0.2` o'rnatilgan edi va `repeat_penalty` ko'rsatilmagan.
  - O'zbek tilidagi erkin ijodiy biznes tahlilida, past harorat greedy (ochko'z) token tanlashga majbur qiladi. Model bir marta *"yo'l tirbandliklarni o'zrocha o'zgartirish"* iborasini ishlatgach, keyingi qadamlarda ushbu tokenlarning ehtimolligi yanada oshib, **n-gram repetition loop** vujudga keldi.
- **Yechim (Ishlab chiqarish sozlamasi):** O'zbek tilida erkin matn yozishda `temperature=0.4 – 0.6` va `repeat_penalty=1.1` qo'yilishi shart!

### Test 3: Formal Kategorik Mantiq (Sillogizm)
- **Vazifa:** *"Barcha Blooplar Razzie, barcha Razzielar Lizzie bo'lsa, barcha Blooplar Lizzie bo'ladimi?"*
- **Model Natijasi:** Tranzitivlik qoidasini matematik ifodaladi:
  $$ \text{Bloop} \rightarrow \text{Razzie} $$
  $$ \text{Razzie} \rightarrow \text{Lizzy} $$
  $$ \therefore \text{Bloop} \rightarrow \text{Lizzy} $$
  To'liq va xatosiz isbot.

### Test 4: O'zbek Tili Entitilarini Ajratish va Qat'iy JSON (Haqiqiy Marvarid!)
- **Kiruvchi Xabar:** *"Assalomu alaykum, men kecha buyurtma qilgan #98421 raqamli Samsung Galaxy S24 telefonimni Toshkent shahri Chilonzor 9-mavze 12-uyga soat 18:30 dan keyin yetkazib berishingizni so'rayman. Agar kuryer kelishidan oldin +998901234567 raqamiga qo'ng'iroq qilsa yaxshi bo'lardi."*
- **Model Qaytargan JSON:**
  ```json
  {
    "order_id": 98421,
    "product_name": "Samsung Galaxy S24",
    "delivery_address": {
      "city": "Toshkent",
      "district": "Chilonzor",
      "details": "9-mavzu 12-uy"
    },
    "preferred_time": "18:30",
    "contact_phone": "+998901234567",
    "customer_notes": "Kuryer kelishidan oldin qo'ng'iroq qilsa yaxshi bo'lishi kerak"
  }
  ```
- **Xulosa:** Hech qanday kirish/chiqish so'zlarsiz, to'g'ridan-to'g'ri backend API ga uzatish mumkin bo'lgan mukammal JSON! Telefon, manzil, buyurtma ID raqami 100% to'g'ri ajratildi.

---

## 5. Ishlab Chiqarish Qarorlar Matritsasi (Team Lead uchun)

```
                            ┌──────────────────────────────────────────────┐
                            │    Qanday Vazifa Hal Qilinmoqda?             │
                            └──────────────────────┬───────────────────────┘
                                                   │
                     ┌─────────────────────────────┴─────────────────────────────┐
                     ▼                                                           ▼
         [ O'zbekcha Chatbot, API Agent, JSON ]                     [ Og'ir Matematik Isbot / AIME ]
                     │                                                           │
        ┌────────────┴────────────┐                                              ▼
        ▼                         ▼                                      DeepSeek-R1-Distill
  [ Kichik Xotira (2.4 GB) ] [ Tezkor Javob (15t/s) ]                    tanlansin (CoT kerak)
        │                         │
        ▼                         ▼
  ✅ QWEN2.5-3B ENG MA'QUL TANLOV
  (O'zbekiston fintech va e-commerce uchun ideal)
```

### Qachon Ishlatish Kerak (Best Cases):
1. **Telegram Botlar va E-commerce:** Mijozlar bilan o'zbek tilida muloqot qilish, manzil va buyurtmalarni qabul qilish.
2. **Avtomatlashtirilgan CRM / Call-Center:** Qo'ng'iroq stenogrammalaridan xulosa chiqarish va buyurtma kartasini (JSON) to'ldirish.
3. **Arzon VPS Serverlar (2-4 GB RAM):** GPU sotib olmasdan, oddiy CPU da mijozlarga kechikishlarsiz tezkor javob qaytarish.

### Qachon Ishlatish Mumkin Emas:
1. **Past Haroratda (temp < 0.3) Erkin Esse Yozish:** `repeat_penalty` berilmasa, so'zlarni takrorlash xavfi mavjud.

---

## 6. Ishlab Chiqarish Uchun Tavsiya Etilgan Giperparametrlar

```python
# O'zbek tilida xatosiz va takrorlanishsiz ishlashi uchun:
generation_params = {
    "temperature": 0.4,       # Juda past bo'lmasligi kerak (0.1-0.2 dan qoching)
    "top_p": 0.9,             # Ehtimollik yadrosi
    "repeat_penalty": 1.15,   # Takrorlanish siklining oldini oladi (SHART!)
    "stop": ["<|im_end|>", "<|endoftext|>"]
}
```

---

## 7. Modelni Ishga Tushirish

### Bitta so'rov yuborish:
```bash
docker compose run --rm qwen2_5_3b_instruct_gguf python3 demo.py --prompt "PostgreSQL B-Tree va GIN indekslarini tushuntirib ber."
```

### Interaktiv terminal chat:
```bash
docker compose run --rm qwen2_5_3b_instruct_gguf python3 demo.py --chat
```

### Benchmarklarni qayta ishga tushirish:
```bash
docker compose run --rm qwen2_5_3b_instruct_gguf python3 run_benchmarks.py
```


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF)
- **Qo'shimcha Manba / Upstream:** [https://github.com/QwenLM/Qwen2.5](https://github.com/QwenLM/Qwen2.5)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
