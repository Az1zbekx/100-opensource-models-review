# Gemma-2-2B-Instruct (GGUF) — Texnik Hisobot va Ishlab Chiqarish Tahlili

> **100-OpenSource-Models-Review | Model #48**  
> **Kategoriya:** Katta Til Modellari (LLM) — Google On-Device & Edge Flagman  
> **Tashkilot:** Google DeepMind (AQSH / Buyuk Britaniya)  
> **Kontekst hajmi:** **8,192 token** (Sliding Window Attention, Logit Soft-Capping)  
> **O'qitilgan ma'lumot hajmi:** **2+ Trillion token** (Gemini modellaridan bilim distillatsiyasi)  
> **Format:** GGUF (`Q4_K_M`, ~1.63 GB)  
> **Inference Dvigateli:** `llama.cpp` (CPU / GPU offload)

---

## 1. Model Arxitekturasi va "Killer Feature"

Gemma-2-2B — Google DeepMind tomonidan Gemini modellar oilasi texnologiyalari asosida yaratilgan eng mukammal ixcham (2.6 milliard parametrli) ochiq modeldir. U o'z sinfidagi boshqa 2B-3B modellardan bir qancha inqilobiy arxitektura yechimlari bilan ajralib turadi:

1. **Gemini Bilim Distillatsiyasi (Knowledge Distillation):** Model noldan o'rganmagan, balki Google'ning yirik Gemini modellaridan bilim o'tkazish orqali tarbiyalangan. Natijada 2B hajmida bo'lsa-da, katta modellarga xos mantiqiy xulosalash qobiliyatiga ega.
2. **Logit Soft-Capping:** Diqqat qatlamlarida (attention logits) ehtimolliklarning keskin o'sib ketishini matematik jilovlaydi (`tanh` cheklovi). Bu esa modelning bema'ni gaplarni to'qishini (hallucination) va cheksiz so'z takrorlashini sezilarli darajada kamaytiradi.
3. **Sliding Window Attention (SWA):** Har ikkinchi qatlamda 4096 tokenli mahalliy sirpanuvchi oyna va global e'tibor navbatma-navbat almashadi, bu esa KV-kesh xotirasini tejaydi.
4. **Tezkor CPU Inference:** Noutbuk yoki arzon server protsessorida **15.0 tok/s** tezlikda barqaror generatsiya beradi.

---

## 2. Uskuna Talablari va Infratuzilma (Hardware Sizing)

| Konfiguratsiya | Minimal Chekka Qurilma (Laptop CPU) | Optimal Ishlab Chiqarish (GPU) |
|---|---|---|
| **RAM (Operativ xotira)** | **4 GB DDR4** (Bo'sh joy: 2.0 GB) | **4 GB tizim RAM** |
| **VRAM (Video xotira)** | Talab etilmaydi (CPU rejimi) | **2 GB – 4 GB VRAM** (GTX 1650, T4) |
| **Model disk hajmi** | ~1.63 GB (`gemma-2-2b-it-Q4_K_M.gguf`) | ~1.63 GB |
| **KV Cache hajmi (4k/8k)** | ~180 MB | ~180 MB |
| **Inference Tezligi** | CPU'da **~14–15.5 tok/s** | GPU'da **~55–75 tok/s** |

---

## 3. Empirik Benchmark Natijalari (Haqiqiy Sinov Telemetriyasi)

Sinovlar mahalliy serverda (AMD/Intel CPU, 6 thread, `n_ctx=4096`, Docker konteynerida `llama.cpp`) o'tkazildi:

| Test Nomi | Fokus / Yo'nalish | Vaqt (s) | Tokenlar | Tezlik (tok/s) | Natija / Xulosa |
|---|---|---|---|---|---|
| **Test 1: System Architecture** | Event Sourcing vs CRUD taqqoslash jadvali (4 ta mezon) | 18.88 s | 282 | **14.94 tok/s** | ✅ **Mukammal:** Benuqson Markdown jadval va xulosalar |
| **Test 2: Uzbek Comprehension** | Startap ekotizimi va xorijiy venchur investitsiyalari | 22.52 s | 305 | **13.54 tok/s** | ⚠️ **Barqaror, ammo sun'iy:** Fikrlar to'g'ri, uslub robotdek |
| **Test 3: Logic Deduction** | Qutidagi qizil va ko'k sharlar ehtimolligi ($3/5 \times 1/2$) | 12.22 s | 178 | **14.56 tok/s** | ✅ **SOTA Matematika:** $3/10$ to'g'ri qadamlar bilan chiqarildi |
| **Test 4: Code Concurrency** | Thread-safe $O(1)$ xotirali Python `MetricsCollector` | 64.87 s | 971 | **14.97 tok/s** | ⚠️ **Mantiqiy Xato:** O'rtacha hisoblash formulasi xato yozildi |

---

## 4. Testlar Tahlili va Aniqlangan Kritik Muhandislik Saboqlari

### Test 1: Tizim Arxitekturasi (Event Sourcing vs CRUD)
- **Vazifa:** State Storage, Auditability, Performance, Complexity mezonlari bo'yicha toza jadval yaratish.
- **Model Tahlili:** Model professional arxitektor darajasida qisqa va lo'nda jadval berdi:
  - Event Sourcing: Tarixiy o'zgarishlar oqimi saqlanishi, yuqori audit imkoniyati, murakkab infratuzilma.
  - Traditional CRUD: Joriy holatning o'zgarmas surati (snapshot), cheklangan audit, sodda va tez boshlang'ich arxitektura.

### Test 2: O'zbek Tili Tahlili va Matn Tushunish
- **Sinov:** O'zbekiston startap ekotizimi va 150 million dollarlik venchur investitsiyalari haqidagi matndan 2 ta xulosa chiqarish.
- **Model Natijasi:**
  - Kichik Llama va Mistral kabi cheksiz takrorlanish sikliga (degeneration loop) tushmadi.
  - Asosiy faktlarni (startap kengayishi, 150 mln dollar) 100% to'g'ri ajratdi.
  - Kamchilik: Uslub juda robotlashtirilgan bo'lib, jumlalarni *"deb qisqacha yoziladi"* deb yakunladi.

### Test 3: Diskret Ehtimollik va Matematik Mantiq
- **Vazifa:** 3 ta qizil va 2 ta ko'k shar bor qutidan ketma-ket qaytarmasdan 2 ta qizil shar olish ehtimolligi.
- **Model Hisob-kitobi:**
  1. 1-shar qizil bo'lishi: $3 / 5$
  2. 2-shar qizil bo'lishi: $2 / 4 = 1 / 2$
  3. Birgalikdagi ehtimollik: $(3/5) \times (1/2) = 3/10$
- **Xulosa:** To'liq, aniq va ixcham qadamlar.

### Test 4: Parallellik va Dasturlash (Aniqlangan Junior Xato!)
- **Talab:** Thread-safe, xotirasi qat'iy $O(1)$ bo'lgan `MetricsCollector` sinfini yozish.
- **Aniqlangan Xatoliklar:**
  1. **Ortiqcha Navbat (Queue):** Model $O(1)$ onlayn hisob-kitob qilish o'rniga `queue.Queue` ochib, metrikalarni navbatga tiqdi va `get_stats()` chaqirilganda navbatni bo'shatib hisoblaydigan qildi.
  2. **Kritik Arifmetik Xato (Incremental Average):** Model o'rtacha qiymatni hisoblashda quyidagi kodni yozdi:
     ```python
     # XATO: Mavjud o'rtachani (count+1) ga bo'lib yuborgan!
     "avg": stats.get("avg", 0) / (stats.get("count", 0) + 1)
     ```
     To'g'ri formula esa: `"avg": new_sum / new_count` bo'lishi shart edi.
  - **Saboq:** Gemma-2-2B umumiy arxitekturani tushunadi, ammo matematik algoritmlar va inkremental o'rtacha hisoblashda kod darajasida inson nazorati talab qilinadi.

---

## 5. Ixcham 1.5B–2.6B Modellar Taqqoslama Matritsasi

| Model | Parametr | RAM Sarfi | CPU Tezligi | Matematika / Mantiq | O'zbek Tili Sifati |
|---|---|---|---|---|---|
| **Qwen2.5-1.5B-Instruct** | 1.54B | ~1.6 GB | ~28 tok/s | Yaxshi | **Eng kuchli (SOTA)** |
| **SmolLM2-1.7B-Instruct** | 1.71B | ~1.8 GB | ~27 tok/s | O'rtacha | Yaxshi |
| **Gemma-2-2B-Instruct** | **2.61B** | **~2.2 GB** | **~15 tok/s** | **Yuqori (DeepMind)** | O'rtacha (Sun'iy) |
| **Phi-3.5-mini-instruct** | 3.82B | ~3.2 GB | ~12 tok/s | Eng yuqori | Xatolik (Turkcha drift) |

---

## 6. Ishlab Chiqarish Qarorlar Matritsasi (Team Lead uchun)

```
                            ┌──────────────────────────────────────────────┐
                            │    Qanday Vazifa Uchun 2B Model Kerak?       │
                            └──────────────────────┬───────────────────────┘
                                                   │
                     ┌─────────────────────────────┴─────────────────────────────┐
                     ▼                                                           ▼
         [ Mantiqiy Xulosa, Matn Tahlili, Jadval ]                  [ O'zbek Tilidagi Mijoz Chatboti ]
                     │                                                           │
        ┌────────────┴────────────┐                                              ▼
        ▼                         ▼                                      Qwen2.5-1.5B yoki
  [ Laptop / Edge CPU ]     [ Qat'iy Matematika ]                        Qwen2.5-3B tanlansin
        │                         │                                      (Gemma o'zbekchada sun'iy)
        ▼                         ▼
  ✅ GEMMA-2-2B TAVSIYA     ⚠️ KOD YOZILGANDA
  ETILADI (Barqaror, 15t/s) INSON TEKSHIRUVI SHART
```

### Qachon Ishlatish Kerak (Best Cases):
1. **Ofis Noutbuklarida Mahalliy Yordamchi:** Internetga ulanmasdan turib, xat yozish, matnlarni tahrirlash, jadval ko'rinishida taqqoslash.
2. **Matnli Mantiqiy Qoidalar (Rule Engine):** Hujjatlardan shartlarni tekshirish va xulosa chiqarish.
3. **Arzon Bulutli Serverlar (1 vCPU, 2GB RAM):** Eng minimal resursda ishlovchi micro-API lar.

### Qachon Ishlatish Mumkin Emas:
1. **Nazoratsiz Moliyaviy Algoritm / Kod Generatsiyasi:** Inkremental o'rtacha hisoblash kabi formulalarda xato qilishi mumkin.
2. **Tabiiy O'zbekcha Dialoglar:** O'zbekcha jumlalari qotib qolgan va sun'iy jaranglaydi.

---

## 7. Modelni Ishga Tushirish

### Bitta so'rov yuborish:
```bash
docker compose run --rm gemma_2_2b_instruct_gguf python3 demo.py --prompt "Explain process vs thread in 3 bullets."
```

### Interaktiv terminal chat:
```bash
docker compose run --rm gemma_2_2b_instruct_gguf python3 demo.py --chat
```

### Benchmarklarni qayta ishga tushirish:
```bash
docker compose run --rm gemma_2_2b_instruct_gguf python3 run_benchmarks.py
```
