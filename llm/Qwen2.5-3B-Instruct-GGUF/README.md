# Qwen2.5-3B-Instruct (GGUF)

> **100-OpenSource-Models-Review | Model #49**  
> **Kategoriya:** Katta Til Modellari (LLM) — Ko'p Tillik / Oltin O'rtaliq 3B  
> **Ishlab chiquvchi:** Alibaba Cloud (Qwen Team)  
> **O'qitilgan ma'lumot hajmi:** **18 Trillion token**  
> **Format:** GGUF (`Q4_K_M`)  
> **Inference Engine:** `llama.cpp` / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature"

Qwen2.5-3B — Alibaba Cloud tomonidan taqdim etilgan 3B o'lchamdagi eng kuchli va universal model hisoblanadi. U 18 trillion tokenlik gigant korpusda o'qitilgan bo'lib, o'zining ko'p tillilik (shu jumladan o'zbek tili va turkiy tillar oilasi), qat'iy tizimli ko'rsatmalarga bo'ysunish hamda tuzilmaviy JSON/SQL generatsiyasi bo'yicha hatto o'tgan avlod 7B modellaridan ham yuqori natijalarni namoyish etadi.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **O'zbek va Turkiy Tillarda Yetakchilik:** 29 dan ortiq tillarda, jumladan o'zbek tilida tabiiy grammatika va boy lug'at boyligi bilan ravon javob bera oladi.
2. **Kengaytirilgan Kontekst (128k gacha):** Asl arxitekturasi 32k kontekstni to'liq qamrab oladi va YaRN mexanizmi bilan 128k tokengacha bo'lgan yirik hujjatlarni tahlil qilish imkonini beradi.
3. **Mukammal Kod va JSON Formatlash:** Agentlar, API integratsiyalari va RAG tizimlari uchun aniq schema bo'yicha xatosiz JSON qaytarish qobiliyati yuqori.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `Qwen/Qwen2.5-3B-Instruct-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (~2.14 GB) |
| **Parametrlar soni** | **3.09B** |
| **Kontekst oynasi** | 32,768 tokens (128k gacha qo'llab-quvvatlaydi) |
| **RAM / VRAM sarfi** | **~2.4 – 3.2 GB** |
| **Target Platforma** | CPU / 4GB VRAM GPU (GTX 1650), Arzon VPS, Lokal server |

---

## 🚀 Qanday Ishga Tushiriladi?

### 1. Terminal orqali interaktiv chat:
```bash
./chat.sh
```

### 2. Bitta prompt yoki faylni test qilish:
```bash
python3 demo.py --prompt "O'zbekistonning IT sohasidagi asosiy 3 ta ustunligini sanab bering"
python3 demo.py --input-file data/input_1_architecture_summary.txt
```
