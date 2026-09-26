# Qwen2.5-1.5B-Instruct (GGUF Q4_K_M) — Model Ko'rib Chiqish va Benchmark

> **100-OpenSource-Models-Review | Model #19**  
> **Kategoriya:** Katta Til Modellari (LLM / SLM) — Umumiy Maqsadli Kichik Til Modeli  
> **Asosiy Baza:** Alibaba Cloud Qwen2.5 (1.54B Parameters, 18T Token Korpus)  
> **Format:** GGUF (`Q4_K_M` — 4-bit medium K-quants)  
> **Inference Engine:** `llama.cpp` / CPU & GPU  

[![Category](https://img.shields.io/badge/Category-LLM-blue.svg)]()
[![Model Size](https://img.shields.io/badge/Parameters-1.54B-green.svg)]()
[![Quantization](https://img.shields.io/badge/Quantization-Q4__K__M-orange.svg)]()
[![Context Window](https://img.shields.io/badge/Context-32k-purple.svg)]()
[![Deployment](https://img.shields.io/badge/Docker-Ready-2496ED.svg)]()

**Qwen2.5-1.5B-Instruct** — Alibaba Cloud kompaniyasi tomonidan 18 trillion tokenlik ulkan ko'p tilli (multilingual) ma'lumotlar to'plamida o'qitilgan, 2024-yil oxirida ommaga taqdim etilgan eng kuchli va tejamkor kichik til modellaridan (SLM) biridir. Ushbu model **GGUF Q4_K_M** formatida atigi **986 MB** disk hajmini egallaydi va har qanday arzon server yoki noutbuk CPU'sida bemalol ishlay oladi.

---

## 📑 Mundarija (Table of Contents)
- [Modelning Asosiy Ustunligi ("Killer Feature")](#modelning-asosiy-ustunligi-killer-feature)
- [Qaysi loyihalar uchun ideal (Best Project Fit)](#qaysi-loyihalar-uchun-ideal)
- [🥊 Head-to-Head: Standart Qwen2.5-1.5B vs DeepSeek-R1-Distill-1.5B](#head-to-head-standart-qwen25-15b-vs-deepseek-r1-distill-15b)
- [Texnik Pasport va Apparat Talablari](#texnik-pasport-va-apparat-talablari)
- [🧪 Jahon Standartidagi Sinovlar va Benchmark Natijalari](#test-malumotlari-va-benchmark-natijalari)
  - [1. Boshlang'ich Operatsion Sinovlar](#1-boshlangich-operatsion-sinovlar)
  - [2. Murakkab Algoritmik va Mantiqiy Stress-Testlar (Hard Suite)](#2-murakkab-algoritmik-va-mantiqiy-stress-testlar-hard-suite)
  - [3. 🏆 Rasmiy Olimpiada Sinovlari (AIME 2024 & MATH Level 5)](#3--rasmiy-olimpiada-sinovlari-aime-2024--math-level-5)
- [⚠️ Halol va Aniq Tahlil: Real Sinovdagi Jiddiy Kamchiliklar](#halol-va-aniq-tahlil-real-sinovdagi-jiddiy-kamchiliklar)
- [Muhandislik Retsepti: Production Arxitekturasi va Sozlamalar](#muhandislik-retsepti)
- [Production Server & Masshtablash Xarajatlari (1,000 foydalanuvchi)](#production-server--masshtablash)
- [Docker va CLI orqali Ishga Tushirish](#docker-va-cli-orqali-ishga-tushirish)
- [🔗 Rasmiy Manbalar](#rasmiy-manbalar)

---

## Modelning Asosiy Ustunligi ("Killer Feature")

Ko'plab 1B–2B parametrli modellar (masalan, Llama-3.2-1B yoki SmolLM2) o'zbek tili va murakkab sintaksisda tezda chalkashib, ma'nosiz so'zlarni chiqara boshlaydi. 

**Qwen2.5-1.5B ning asosiy ustunliklari:**
1. **Turkiy va Ko'p Tilli Korpusning Kengligi:** 18T tokenning katta qismi Osiyo va turkiy tillarga moslashgani sababli, 1.5B hajmda o'zbek tilini tushunish va grammatik jihatdan to'g'ri gap tuzish bo'yicha o'z sinfida mutlaq yetakchi.
2. **Strukturaviy Ma'lumotlarni Chiqarish (Zero-Shot JSON Extraction):** Matndan aniq JSON schema bo'yicha ma'lumotlarni hech qanday ortiqcha markdown axlatsiz (`100% valid JSON`) ajratib oladi.
3. **Mikroskopik Resurs Sarfi:** Diskda **986 MB**, tezkor xotirada (RAM) **~1.1 GB**. Har qanday $5/oylik VPS'da backend servislari bilan birgalikda hech qanday qotishlarsiz ishlaydi.
4. **Yuqori Tezlik:** Oddiy CPU'da (4 thread) barqaror **~24 – 25 tok/s** tezlik bilan ishlaydi (foydalanuvchi matn yozilishini deyarli kutmaydi).

---

## Qaysi loyihalar uchun ideal (Best Project Fit)

### ✅ Bu model qayerda zo'r ishlaydi:
* **Mahalliy Telegram botlar va FAQ yordamchilar:** Korxona ichki hujjatlari, foydalanuvchi savollariga tezkor va xushmuomala javob qaytarish.
* **JSON Entity Extraction & Form Parser:** Mijoz xabarlari, e'lonlar yoki rezyumelardan telefon raqami, ism, narx, manzil va boshqa maydonlarni JSON formatida ajratish.
* **SQL Query Generation (Junior/Mid daraja):** Oddiy PostgreSQL, MySQL jadvallari uchun `JOIN`, `WHERE`, `ORDER BY`, `LIMIT` qismlarini to'g'ri yozish.
* **Matnlarni Qisqartirish (Summarization) va Qayta Ishlash:** Katta maqola yoki mijoz shikoyatini 2-3 jumlada qisqacha xulosa qilish.

### ❌ Qayerda mutlaqo ishlatmaslik kerak:
* **Murakkab Matematik va Bayes Ehtimolligi:** Modelda Chain-of-Thought (mulohaza zanjiri) o'qitilmaganligi sababli, ehtimollik formulalarini o'zidan to'qib chiqaradi (hallucination).
* **Ko'p Bosqichli Deduktiv Jumboqlar:** 5+ shartli mantiqiy masalalarda (masalan, kim kimdan keyin kelgani) shartlarni to'liq qamrab ololmaydi va takrorlanish halqasiga (Infinite Loop) tushadi.
* **Senior Dasturchi Darajasidagi Kod Arxitekturasi:** Murakkab mikroservislar, distributed systems yoki chuqur xotira tahlilida xatoliklarga yo'l qo'yadi.

---

## 🥊 Head-to-Head: Standart Qwen2.5-1.5B vs DeepSeek-R1-Distill-1.5B

Ikkala model ham bir xil Alibaba Qwen2.5-1.5B arxitekturasiga asoslangan. Lekin ularning vazifalari tubdan farq qiladi:

| Mezon | Qwen2.5-1.5B-Instruct (Model #19) | DeepSeek-R1-Distill-Qwen-1.5B (Model #31) | Muhandislik Xulosasi |
|---|---|---|---|
| **Asosiy Maqsad** | Tezkor javob, chat, JSON, umumiy ko'rsatmalar | Chuqur mantiqiy mulohaza (Reasoning / CoT) | Turli yo'nalishlar |
| **Fikrlash Turi** | To'g'ridan-to'g'ri javob yozadi (Instant response) | Javobdan oldin `<think>` ichida o'ylanadi | R1 o'ylanadi, Qwen darhol yozadi |
| **Javob Boshlanish Vaqti (TTFT)** | **~0.1 soniya** (Bir zumda boshlanadi) | **10 – 40 soniya** (Mulohaza tugashini kutadi) | 🟢 Qwen foydalanuvchi uchun ancha qulay |
| **JSON Chiqarish Aniqligi** | 🏆 **A'lo (Toza JSON, ortiqcha gapi yo'q)** | Yomonroq (`<think>` teglari JSON'ni buzadi) | 🟢 Qwen yutadi |
| **AIME / Matematika Aniqligi** | **0% – 15%** (Formulalarda chalkashadi) | 🏆 **53.3%** (Olimpiada masalalarini yechadi) | 🟢 DeepSeek-R1 yutadi |
| **CPU Tezligi** | **~24 – 25 tok/s** | **~24 – 26 tok/s** | 🤝 Bir xil |
| **RAM Sarfi** | **~1.1 GB** | **~1.2 GB** | 🤝 Bir xil |

> **Team Lead uchun Xulosa:** Agar loyihaga mijoz bilan tez muloqot qiladigan chatbot yoki backend uchun JSON generator kerak bo'lsa — **Qwen2.5-1.5B-Instruct** tanlanadi. Agar loyihaga buxgalteriya hisob-kitoblarini tekshiruvchi yoki qonuniy mantiqiy xulosalar chiqaruvchi agent kerak bo'lsa — **DeepSeek-R1-Distill** tanlanadi.

---

## 📊 Texnik Pasport va Apparat Talablari

| Parametr | Qiymati / Me'yori |
|---|---|
| **Model nomi** | `Qwen/Qwen2.5-1.5B-Instruct-GGUF` |
| **Fayl nomi** | `qwen2.5-1.5b-instruct-q4_k_m.gguf` |
| **Kvantlash darajasi** | `Q4_K_M` (4-bit medium K-quants) |
| **Fayl hajmi** | **986 MB (< 1.0 GB)** |
| **Kontekst oynasi** | 4,096 tokens (maksimal 32,768 gacha kengaytiriladi) |
| **Laptop CPU (4 thread) tezligi** | **~24.5 – 25.3 tok/s** |
| **GTX 1650 (4GB) GPU tezligi** | **~50 – 65 tok/s** (To'liq VRAM ga sig'adi, ~1.2 GB) |
| **RAM / VRAM umumiy sarfi** | **~1.1 GB** |
| **Chat shabloni** | ChatML (`<|im_start|>system...<|im_end|><|im_start|>user...`) |

---

## 🧪 Jahon Standartidagi Sinovlar va Benchmark Natijalari

Sinovlar noutbuk sharoitida (**Intel/AMD CPU, 4 physical threads, 16GB RAM, GTX 1650 4GB**) haqiqiy `llama.cpp` Docker konteynerida o'tkazildi.

### 1. Boshlang'ich Operatsion Sinovlar

| Test Fayli | Sinov Turi va Mazmuni | Kutilgan Natija | Qwen2.5-1.5B Haqiqiy Natijasi | Vaqt / Tezlik | Status |
|---|---|---|---|---|:---:|
| **`data/input_1_support_uz.txt`** | E-commerce mijoz savoli (Yetkazib berish, to'lov usullari) | O'zbek tilida xushmuomala, to'g'ri biznes javobi | Aniq va tushunarli o'zbekcha javob berdi. Payme/Click va muddatlar to'g'ri yoritildi. | 8.16s / 19.0 tok/s | ✅ **PASS** |
| **`data/input_2_json_extract.txt`** | Ish e'lonidan tuzilmagan matndan JSON ajratish | Toza JSON: `company`, `position`, `salary_usd`, `location` | **100% Valid JSON**. Ortiqcha markdown matnlarsiz to'g'ri ajratdi. | 6.74s / 12.3 tok/s | ✅ **PASS** |
| **`data/input_3_sql_query.txt`** | PostgreSQL bo'yicha oxirgi 30 kunlik eng ko'p xarid qilgan top-5 mijoz | `JOIN`, `WHERE status='completed'`, `INTERVAL 30 DAY` | To'g'ri SQL so'rov va tushuntirish yozildi. | 12.90s / 17.9 tok/s | ✅ **PASS** |

---

### 2. Murakkab Algoritmik va Mantiqiy Stress-Testlar (Hard Suite)

| Test Fayli | Mavzu va Murakkablik Darajasi | Nazariy Yechim (Ground Truth) | Qwen2.5-1.5B Haqiqiy Natijasi | Vaqt / Token / Tezlik | Status |
|---|---|---|---|---|:---:|
| **`data/hard_1_math_bayesian.txt`** | **Bertrand qutisi paradoksi** (Bayes ehtimolligi) | $P(\text{Box}_1 \mid \text{Gold}) = \mathbf{2/3}$ ($1/2$ intuitsiyasi xato) | **Qo'pol matematik xato:** Qutilarni tanlash ehtimoli tangalar soniga mutanosib deb $P(B_1)=2/5$ deb gallyutsinatsiya qildi! | 42.18s / 1024 tok (24.28 tok/s) | ❌ **FAIL** |
| **`data/hard_2_algo_amortized.txt`** | **Algoritmik Amortizatsion Tahlil** (LeetCode Longest Consecutive) | 1. $O(N \log N)$ talabga zid.<br>2. Har bir element $\le 2$ marta ko'riladi $\to O(N)$.<br>3. Shart olib tashlansa $O(N^2)$ ga tushadi. | 1 va 2-savollarga mukammal javob berdi. Biroq 3-savolda shart olib tashlansa ham $O(N)$ qoladi deb noto'g'ri xulosa qildi. | 19.08s / 481 tok (25.21 tok/s) | ⚠️ **PARTIAL** |
| **`data/hard_3_logic_knights.txt`** | **Ritsarlar, Yolg'onchilar va Ayg'oqchilar** (Diskrеt mantiq) | A = Knight, B = Spy, C = Knave | A=Knight, B=Knave, C=Spy deb topdi, lekin B=Knave deb turib uning A haqidagi gapi haqiqatligini aytib, **ichki ziddiyatga** tushdi. | 30.42s / 741 tok (24.36 tok/s) | ⚠️ **PARTIAL** |
| **`data/hard_4_uzbek_logic_puzzle.txt`** | **O'zbek tilidagi 5 bosqichli poyga deduksiyasi** | Anvar(1), Dilshod(2), Bobur(3), Eldor(4), Charos(5) | **Cheksiz takrorlanish (Degeneration loop):** Shartlarni bajara olmay, "Bobur va Dilshod g'olib bo'ldi..." jumlasini 1024 token tugaguncha takrorlab qotdi. | 42.42s / 1024 tok (24.14 tok/s) | ❌ **FAIL (Loop)** |

---

### 3. 🏆 Rasmiy Olimpiada Sinovlari (AIME 2024 & MATH Level 5)

Dunyo bo'yicha yetakchi sun'iy intellekt modellarini baholashda ishlatiladigan xalqaro rasmiy olimpiada masalalaridagi natijalar:

| Test Fayli | Manba | Rasmiy To'g'ri Javob | Qwen2.5-1.5B Haqiqiy Natijasi | Aniqlik Foizi | Status |
|---|---|---|---|:---:|:---:|
| **`data/olympiad_1_aime_game_theory.txt`** | **AIME 2024 (I) — 3-Masala** (O'yinlar nazariyasi, $n \le 2024$) | **`809`** | Modulo 5 mantiqiy g'oyasini tushundi, lekin mayda hisobda adashib **`404`** deb chiqardi. | **20%** | ⚠️ **PARTIAL** |
| **`data/olympiad_2_aime_logarithms.txt`** | **AIME 2024 (I) — 2-Masala** (Logarifmik tenglamalar, $xy$) | **`25`** | Tenglamani to'g'ri o'girdi, biroq algebrada chalkashib $2^{2/5}$ deb xato javob berdi. | **15%** | ❌ **FAIL** |
| **`data/olympiad_3_math_legendre.txt`** | **MATH Benchmark (Level 5)** (Lejandr formulasi, $100$ ta nol) | **`405`** | Lejandr formulasini mukammal yozdi, $n \approx 400$ deb baholadi. Lekin $401, 402, 403, 404...$ deb birma-bir hisoblashda 1024 token limitiga urildi. | **60%** | ⚠️ **PARTIAL (Token Limit)** |

* **Umumiy Olimpiada Natijasi:** **`31.6%`** (Standart 1.5B bazaviy model uchun o'rtacha natija; Chain-of-Thought siz murakkab olimpiadani yechish deyarli imkonsiz).

---

## ⚠️ Halol va Aniq Tahlil: Real Sinovdagi Jiddiy Kamchiliklar

Model ustida o'tkazilgan benchmarklar uning production sharoitida e'tibor qaratilishi shart bo'lgan quyidagi **haqiqiy zaif tomonlarini** fosh qildi:

1. **Cheksiz Takrorlanish Halqasi (Repetition Degeneration Trap):**  
   O'zbek tilidagi murakkab, bir nechta cheklovlar bir vaqtda berilgan so'rovlarda model o'z diqqat matritsasini (attention weights) yo'qotadi va bitta jumlani cheksiz marta qaytarishga o'tib ketadi.
   * *Yechim:* Inference paytida `repeat_penalty: 1.15` parametrini majburiy qo'llash shart!
2. **Ehtimollik va Bayes Formulalarida "Gallyutsinatsiya":**  
   Model ko'p bosqichli formulalarda qadamlarni ichida tekshira olmaydi. Masalan, Bertrand paradoksida u qutilarni tanlash ehtimoli tangalar soniga teng deb, $P(B_1)=2/5$ degan mutlaqo soxta matematik formulani "ishonch bilan" to'qib chiqardi.
3. **Qadamlar Hajmini Baholay Olmaslik (Inefficient Search Steps):**  
   Faktorialdagi nollar sonini hisoblashda, nollar faqat 5 ga karrali sonlarda ko'payishini tushunmasdan, $401, 402, 403...$ kabi keraksiz oraliqlarni birma-bir tahlil qilib, ajratilgan 1024 tokenni bekorga sarflab qo'ydi.

---

## Muhandislik Retsepti: Production Arxitekturasi va Sozlamalar

Agar kompaniyangiz loyihasida ushbu modelni ishlatishga qaror qilsangiz, quyidagi tavsiyalarga amal qiling:

### 1. Optimal Inference Parametrlari
```python
generation_params = {
    "temperature": 0.2,          # Faktik va JSON vazifalar uchun past harorat
    "top_p": 0.85,
    "repeat_penalty": 1.15,      # Takrorlanish loopiga tushib qolmaslik uchun
    "max_tokens": 1024,
    "stop": ["<|im_end|>", "<|endoftext|>"]
}
```

### 2. Router Arxitekturasi (Smart Routing)
Foydalanuvchi so'rovlarini tahlil qilib, mos modelga yo'naltirish:
- **Agar so'rov:** FAQ, mijoz bilan salomlashish, qisqa fakt, matndan JSON olish bo'lsa $\to$ **Qwen2.5-1.5B-Instruct** (Javob vaqti: ~0.5–1s).
- **Agar so'rov:** Murakkab hisob-kitob, soliq/buxgalteriya qoidalari, qiyin algoritm bo'lsa $\to$ **DeepSeek-R1-Distill** yoki kattaroq 8B model (Javob vaqti: ~15–30s).

---

## Production Server & Masshtablash Xarajatlari (1,000 foydalanuvchi)

Kuniga o'rtacha 1,000 ta faol foydalanuvchiga (kuniga ~10,000 ta so'rov) xizmat ko'rsatish uchun:

| Infratuzilma | Konfiguratsiya | Imkoniyati | Oylik Xarajat |
|---|---|---|:---:|
| **Minimal VPS (CPU-only)** | 2 vCPU, 4GB RAM (Hetzner / DigitalOcean) | 1–3 parallel foydalanuvchi | **~$5 – $7 / oy** |
| **Optimal Production Server** | 4 vCPU, 8GB RAM (c2-standard-4 yoki Hetzner CPX31) | 5–10 parallel foydalanuvchi (navbat bilan) | **~$15 – $25 / oy** |
| **GPU Server (Agar kerak bo'lsa)** | 1x NVIDIA T4 yoki GTX 1650 | 25+ parallel foydalanuvchi, 60 tok/s | **~$35 – $50 / oy** |

> **Biznes Xulosasi:** Ushbu model korxona uchun **$0 qo'shimcha GPU xarajati** bilan mavjud backend serverning o'zida yashab, oyiga $10 dan kam mablag' bilan to'liq avtonom ishlay oladi.

---

## 🐳 Docker va CLI orqali Ishga Tushirish

### 1. Docker Compose orqali ishga tushirish (Tavsiya etiladi)
```bash
# Repozitoriy ildizidan
docker compose run --rm qwen2_5_1_5b_instruct_gguf python3 demo.py --prompt "O'zbekistonda IT sohasining rivojlanishi haqida 3 ta asosiy fikr yoz." --tokens 300
```

### 2. Standalone Docker Run
```bash
# Konteynerni qurish
docker build -t qwen2.5-1.5b-instruct llm/Qwen2.5-1.5B-Instruct-GGUF

# Interaktiv chat rejimida ishga tushirish
docker run --rm -it -v ~/.cache/huggingface:/root/.cache/huggingface qwen2.5-1.5b-instruct python3 demo.py --chat
```

### 3. To'liq Benchmark Suite ni qayta tekshirish
```bash
docker compose run --rm qwen2_5_1_5b_instruct_gguf python3 run_benchmark_suite.py
```

---

## 🔗 Rasmiy Manbalar

- [Alibaba Qwen2.5 Rasmiy Blog va Texnik Hisobot](https://qwenlm.github.io/blog/qwen2.5/)
- [HuggingFace Qwen2.5-1.5B-Instruct-GGUF Repozitoriysi](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)
- [llama.cpp Rasmiy GitHub Loyihasi](https://github.com/ggerganov/llama.cpp)


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)
- **Qo'shimcha Manba / Upstream:** [https://github.com/QwenLM/Qwen2.5](https://github.com/QwenLM/Qwen2.5)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
