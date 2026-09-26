# Qwen2.5-Coder-1.5B-Instruct (GGUF Q4_K_M)

> **100-OpenSource-Models-Review | Model #33**  
> **Kategoriya:** Katta Til Modellari (LLM) — Dasturlash va Kod Generatsiyasi (Coding Specialist)  
> **Asosiy Arxitektura:** Qwen2.5 (1.54B Parameters, Dense Transformer)  
> **O'qitilgan Ma'lumot Hajmi:** **5.5 Trillion Token** (Kod, matematika va sintetik dasturlash ma'lumotlari)  
> **Format:** GGUF (`Q4_K_M` — 4-bit medium K-quants)  
> **Inference Engine:** `llama.cpp` / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature" (Boshqalardan Asosiy Ustunligi)

Ushbu model Alibaba Cloud jamoasi tomonidan faqat va faqat **dasturlash (software engineering)** uchun maxsus o'qitilgan eng yangi avlod kod modelidir. 92 ta dasturlash tilidagi 5.5 Trillion token kod va repozitoriyalarda o'qitilgan.

### 🌟 Asosiy Ustunliklari:
1. **O'z Vaznida Mutlaq Chempion (HumanEval 65%+):** 1.5B hajmdagi model bo'lishiga qaramay, u o'zidan 5 barobar katta bo'lgan eski `CodeLlama-7B` va `DeepSeek-Coder-1.3B` lardan sezilarli darajada ustun turadi.
2. **Laptop CPU da "Uchadigan" Tezlik:** Model 1.0 GB hajmga ega va 4–6 yadroli oddiy noutbuk protsessorida soniyasiga **~22 – 25 tok/s** tezlikda kod yozadi (hech qanday GPU talab qilinmaydi!).
3. **Lokal VS Code / Cursor Copilot Muqobili:** Maxfiy korporativ loyihalarda kod tashqariga chiqib ketmasligi uchun dasturchilarning kompyuteriga to'g'ridan-to'g'ri lokal avtoto'ldirgich (autocomplete / copilot) sifatida integratsiya qilish mumkin.
4. **O'zbek Tilidagi So'rovlarni Mukammal Tushunishi:** Llama arxitekturasidan farqli o'laroq, Qwen o'zbek tilidagi topshiriqlarni bexato tushunadi va o'zbekcha toza docstringlar bilan kod yozadi.

### ❌ Qayerda ishlatmaslik kerak:
* **Murakkab Ko'p Qatlamli SQL Joinlarda:** 1.5B parametr ko'p jadvalli murakkab korporativ SQL larda JOIN larni tashlab ketish xavfiga ega (3-testda isbotlandi).
* **Umumiy Filosofik / Adabiy Suhbatlarda:** Model kod uchun ixtisoslashgan; unga adabiyot yoki falsafiy savollar berilsa, quruq va dasturchi uslubida javob beradi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (4-bit medium K-quants) |
| **Fayl hajmi** | **1,065 MB (~1.0 GB)** |
| **Kontekst oynasi** | 4,096 tokens (maksimal 32k gacha kengayadi) |
| **CPU Tezligi (6 thread)** | **~22 – 25 tok/s** (Juda tez) |
| **GPU Tezligi (GTX 1650 / RTX 3060)** | **~55 – 70 tok/s** |
| **RAM / VRAM sarfi** | **~1.2 GB** |

---

## 🧪 Real Dasturlash Sinovlari va Benchmark Natijalari

Model `data/` papkasidagi 4 ta professional dasturlash vazifasida sinovdan o'tkazildi:

| Test Fayli | Dasturlash Vazifasi | Talab Qilingan Sifat | Qwen2.5-Coder Haqiqiy Natijasi | Vaqti / Tezlik | Status |
|---|---|---|---|---|---|
| **`data/input_1_bug_fixing.txt`** | **Multi-threading Deadlock Fix** (Bank o'tkazmasi) | `account_id` bo'yicha qulflarni tartiblash (`sort`) orqali deadlockni yo'qotish | Deadlock nazariyasini a'lo tushuntirdi. Ammo kodda `account_id` taqqoslashni tashlab ketib, yana oddiy `with self.lock: with to_acc.lock:` deb yozdi. | 35.1s / 23.6 tok/s | ⚠️ **PARTIAL (50%)** |
| **`data/input_2_refactor_algo.txt`** | **$O(1)$ LRU Cache Algoritmi** (Doubly Linked List + Hash Map) | Pointerlar bilan `get`, `put`, `evict` metodlarini to'liq yozish | Bog'langan ro'yxat, dummy head/tail mantig'ini a'lo yozdi. Lekin tepada `class Node:` ni e'lon qilishni va evict-da `size -= 1` ni unutdi. | 32.2s / 22.8 tok/s | ⚠️ **PARTIAL (75%)** |
| **`data/input_3_sql_generation.txt`** | **Korporativ Analitik SQL** (CTEs, Window Functions, DENSE_RANK) | Roll-up 7-day average, NTILE top 10% | CTE strukturasini va indekslashni to'g'ri berdi. Lekin NTILE ni `WHERE` ichiga qo'yish sintaksis xatosini qildi va JOIN ni unutdi. | 25.2s / 24.1 tok/s | ⚠️ **PARTIAL (55%)** |
| **`data/input_4_code_completion.txt`** | **O'zbekcha Regex Utility Moduli** (+998 telefon, email, sanalar) | Type hinting, unittest va o'zbekcha docstring | **A'lo natija!** O'zbekcha topshiriqni to'liq tushundi, toza Python regex, `unittest` sinfi va o'zbekcha docstringlar taqdim etdi. | 43.6s / 20.9 tok/s | ✅ **PASS (A'lo)** |

---

## ⚠️ Halol Tahlil: Kichik (1.5B) Kod Modellarining Asosiy Kamchiliklari

1. **Nazariyani Bilib, Kodda Unutish (Implementation Gap):**
   * 1-testda model *"Deadlockni yechish uchun qulflarni tartiblash (lock ordering) kerak"* deb to'g'ri aytdi, lekin kod yozayotganda `if from_acc.id < to_acc.id` shartini yozmasdan yana ichma-ich qulfladi. 1.5B modellar sintaksis yozishda diqqatni ba'zan yo'qotadi.
2. **Klasslar Ta'rifini Tashlab Ketish (NameError xavfi):**
   * 2-testda `LRUCache` klassi ichida `Node(-1, -1)` obyektini yaratdi, lekin yuqorida `class Node:` ni yozmadi. Kodni run qilsangiz xato beradi.
3. **Murakkab SQL da Cheklov:**
   * Bir nechta CTE lar zanjirida ustunlarni bog'lashda (JOIN) xato qildi. Murakkab SQL uchun uning 7B yoki 14B versiyasi tavsiya etiladi.

---

## 🏗️ Muhandislik Retsepti: Lokal IDE Copilot Arxitekturasi

Ushbu 1.5B modelni kompaniya dasturchilari uchun qanday qilib **mutlaqo tekinga va maxfiy** ishlatish mumkin:

```
[ VS Code / Cursor / PyCharm ]
             │ (Continue.dev / Tabby plaginlari orqali)
             ▼
[ Lokal llama.cpp server / Ollama (Port: 8000) ]
             │ (Qwen2.5-Coder-1.5B GGUF Q4_K_M)
             ▼
[ 100% Offline Autocomplete, Refactor & Explanations ]
```

### 💰 Server va Resurs Xarajatlari:
* **Dasturchining Noutbuki (0$ Xarajat):**
  * Istalgan Core i5 / Ryzen 5 noutbukida **1.2 GB RAM** oladi. Dasturchi kod yozayotganda fon rejimida hech qanday qotishlarsiz ishlaydi.
* **Kompaniya Serveri (50 nafar dasturchi uchun markaziy Copilot):**
  * **Server:** 1x NVIDIA RTX 3060 (12GB) yoki bitta 8-core CPU VPS ($20–$40/oy).
  * vLLM yoki Ollama continuous batching orqali 50 ta dasturchiga bir vaqtda kod to'ldirish (autocomplete) xizmatini ko'rsatadi.

---

## 🚀 Ishga Tushirish Qo'llanmasi

### 1. Interaktiv Chat Rejimi (Terminal orqali):
```bash
cd /home/az1z6ekx/100-opensource-models-review/llm/Qwen2.5-Coder-1.5B-Instruct-GGUF
./chat.sh
```

### 2. Docker Compose orqali:
```bash
# Repozitoriy ildizida
docker compose run --rm qwen2_5_coder_1_5b_instruct_gguf python3 demo.py --chat
```

### 3. CLI orqali bitta buyruq bilan:
```bash
docker run --rm \
  -v $(pwd):/app \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  ml-base-cpu:latest \
  python3 /app/demo.py --prompt "Write a Python function to merge overlapping intervals."
```

---

## 🔗 Rasmiy Manbalar va Havolalar

* **Hugging Face Model GGUF:** [Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF)
* **Qwen2.5-Coder Rasmiy Blog:** [Qwen2.5-Coder: Powerful, Diverse, Practical](https://qwenlm.github.io/blog/qwen2.5-coder/)
* **Qwen2.5-Coder GitHub:** [QwenLM/Qwen2.5-Coder](https://github.com/QwenLM/Qwen2.5-Coder) (15k+ Stars)


---

## 🔗 Rasmiy Manbalar va Yuklab Olish (Official Links & Weights)

- **Asosiy Repozitoriy / Model Hub:** [https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF)
- **Qo'shimcha Manba / Upstream:** [https://github.com/QwenLM/Qwen2.5-Coder](https://github.com/QwenLM/Qwen2.5-Coder)
- **Avtomatik yuklab olish:** Demo skriptni birinchi marta ishga tushirganingizda vaznlar ushbu rasmiy manbalardan avtomatik yuklab olinadi.
