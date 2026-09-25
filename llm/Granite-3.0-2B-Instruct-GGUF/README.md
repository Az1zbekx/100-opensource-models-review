# Granite-3.0-2B-Instruct (GGUF)

> **100-OpenSource-Models-Review | Model #50**  
> **Kategoriya:** Katta Til Modellari (LLM) — Korporativ / Apache 2.0  
> **Ishlab chiquvchi:** IBM Research  
> **O'qitilgan ma'lumot hajmi:** **12 Trillion token**  
> **Format:** GGUF (`Q4_K_M`)  
> **Inference Engine:** `llama.cpp` / CPU & Edge

---

## 🎯 Model Haqida va "Killer Feature"

Granite-3.0-2B — IBM kompaniyasi tomonidan korporativ talablar va biznes jarayonlari uchun maxsus ishlab chiqilgan flagman kichik til modelidir. U 12 trillion tokendan iborat bo'lgan litsenziyalangan biznes, kod, texnik hujjatlar va jadval ma'lumotlari asosida o'qitilgan. Eng muhimi, u to'liq **Apache 2.0** erkin litsenziyasiga ega bo'lib, har qanday tijoriy mahsulotda hech qanday cheklovlarsiz ishlatilishi mumkin.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **100% Apache 2.0 Litsenziyasi:** Ko'plab boshqa ochiq modellardagi cheklovchi litsenziyalardan (Meta Llama Community License va boshqalar) farqli ravishda korxona ichida xavfsiz va xolis qo'llash kafolatlangan.
2. **Korporativ RAG va Jadval Ma'lumotlari:** SQL jadvallar, moliyaviy hisobotlar va korxona bilimlari bazasi (RAG) bo'yicha aniq faktoid xulosalar chiqarishga moslashtirilgan.
3. **Ekstremal Yengillik:** 4-bit kvantlangan GGUF holatida bor-yo'g'i ~1.5 GB operativ xotira sarflaydi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `bartowski/granite-3.0-2b-instruct-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (~1.52 GB) |
| **Parametrlar soni** | **2.54B** |
| **Kontekst oynasi** | 4,096 tokens (128k gacha qo'llab-quvvatlaydi) |
| **RAM / VRAM sarfi** | **~1.7 – 2.3 GB** |
| **Target Platforma** | On-Device, CPU VPS, Korporativ lokal server |

---

## 🚀 Qanday Ishga Tushiriladi?

### 1. Terminal orqali interaktiv chat:
```bash
./chat.sh
```

### 2. Bitta prompt yoki faylni test qilish:
```bash
python3 demo.py --prompt "Explain the key requirements of an enterprise database backup policy"
python3 demo.py --input-file data/input_1_architecture_summary.txt
```
