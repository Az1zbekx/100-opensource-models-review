# Gemma-2-2B-Instruct (GGUF)

> **100-OpenSource-Models-Review | Model #48**  
> **Kategoriya:** Katta Til Modellari (LLM) — Ixcham On-Device / Edge  
> **Ishlab chiquvchi:** Google DeepMind  
> **O'qitilgan ma'lumot hajmi:** **2 Trillion token**  
> **Format:** GGUF (`Q4_K_M`)  
> **Inference Engine:** `llama.cpp` / CPU & Edge

---

## 🎯 Model Haqida va "Killer Feature"

Gemma-2-2B — Google DeepMind tomonidan Gemini modellar oilasi texnologiyalari asosida yaratilgan eng yengil va eng mukammal ochiq vaznli modeldir. Bor-yo'g'i 2.6 milliard parametrga ega bo'lishiga qaramay, u o'z sinfidagi eng ilg'or arxitektura yangiliklarini (Sliding Window Attention va Logit Soft-Capping) o'zida mujassam etgan.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **Google Gemini Bilim Distillatsiyasi:** Katta Gemini modellaridan bilim o'tkazish (distillation) orqali o'qitilgani bois, 2B toifasida tengsiz mantiqiy aniqlik va xulosalash qobiliyatiga ega.
2. **Logit Soft-Capping & Sliding Window:** Generatsiyada gallyutsinatsiya va cheksiz ehtimollik tarqalishini jilovlovchi soft-capping mexanizmi hamda 4096/8192 tokenli gibrid oynali e'tibor (attention) hisobiga xotirani tejaydi.
3. **Kam Resurs va Edge Moslashuvchanlik:** 4-bit kvantlashda model bor-yo'g'i ~1.6 GB RAM talab qiladi va har qanday zamonaviy noutbuk yoki arzon bulutli serverda bemalol ishlaydi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `bartowski/gemma-2-2b-it-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (~1.63 GB) |
| **Parametrlar soni** | **2.61B** |
| **Kontekst oynasi** | 8,192 tokens |
| **RAM / VRAM sarfi** | **~1.8 – 2.4 GB** |
| **Target Platforma** | On-Device, Edge, Noutbuk CPU, Arzon VPS |

---

## 🚀 Qanday Ishga Tushiriladi?

### 1. Terminal orqali interaktiv chat:
```bash
./chat.sh
```

### 2. Bitta prompt yoki faylni test qilish:
```bash
python3 demo.py --prompt "Explain the difference between process and thread in 3 bullets"
python3 demo.py --input-file data/input_1_architecture_summary.txt
```
