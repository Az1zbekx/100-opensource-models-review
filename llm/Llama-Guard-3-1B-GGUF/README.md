# Llama-Guard-3-1B (GGUF)

> **100-OpenSource-Models-Review | Model #39**  
> **Kategoriya:** Katta Til Modellari (LLM) — AI Xavfsizlik & Kontent Moderatsiyasi (Guardrail)  
> **Ishlab chiquvchi:** Meta AI  
> **Asosiy Maqsad:** Foydalanuvchi so'rovlari va LLM javoblarini 14 ta xavf toifasi bo'yicha tezkor audit qilish  
> **Format:** GGUF (`Q4_K_M`)  
> **Inference Engine:** `llama.cpp` / CPU & Edge

---

## 🎯 Model Haqida va "Killer Feature"

Llama-Guard-3-1B — Meta tomonidan sun'iy intellekt xavfsizligini ta'minlash uchun maxsus yaratilgan professional klassifikator modelidir. Tijorat chatbotlari yoki korporativ LLM tizimlarida xavfli so'rovlar (kiberhujumlar, zararli kodlar, qonunga zid harakatlar)ni asosiy modelga yetib bormasidanoq millisekundlarda to'xtatib qolish (Guardrail) vazifasini bajaradi.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **14 ta Xavfsizlik Toifasi (S1–S14):** Kiberjinoyatlar, shaxsiy ma'lumotlar o'g'irligi, zo'ravonlik, kimyoviy xavflar va boshqalarni standart bo'yicha aniqlaydi.
2. **Ultra-Tezkor Audit:** Javob bir necha token (`safe` yoki `unsafe\nS13`)dan iborat bo'lgani uchun audit vaqti atigi **~40–80 ms** davom etadi.
3. **Ishlab chiqarishga tayyor (Zero-Cost Guardrail):** Har qanday backend tizimiga minimal CPU resursi bilan xavfsizlik darvozasi sifatida ulanadi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `QuantFactory/Llama-Guard-3-1B-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (~800 MB) |
| **Parametrlar soni** | **1.2B** |
| **Chiqish formati** | `safe` YOKI `unsafe` + Xavf kodi (masalan: `S13: Cyberattacks`) |
| **RAM / VRAM sarfi** | **~0.9 – 1.2 GB** |
| **Audit tezligi** | **~40–100 ms** (har bir so'rov uchun) |

---

*(Real test sinovlari va benchmark jadvallari navbatdagi qadamda to'ldiriladi)*
