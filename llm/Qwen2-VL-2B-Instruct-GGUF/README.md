# Qwen2-VL-2B-Instruct (GGUF)

> **100-OpenSource-Models-Review | Model #43**  
> **Kategoriya:** Multimodal LLM (Vision-Language) — Tasvir & Matn  
> **Ishlab chiquvchi:** Alibaba Cloud (Qwen Team)  
> **Asosiy Qobiliyat:** Tasvir, hujjat, chizma, grafik va jadvallarni ko'rib tushunish (VQA & OCR)  
> **Format:** GGUF (`Q4_K_M` + `mmproj-f16`)  
> **Inference Engine:** `llama.cpp` Multimodal Projector / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature"

Qwen2-VL-2B — ochiq multimodal (VLM) modellar olamining eng kuchli ixcham vakili. U nafaqat matn, balki tasvirlar, skaner qilingan hujjatlar, cheklar, yo'l harakati kameralari kadrlari va grafik diagrammalarni bevosita tahlil qilib, savollarga javob beradi.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **Dynamic Resolution & OCR:** Turli o'lchamdagi va formatdagi tasvirlarni siqmasdan, mayda matnlar va raqamlarni yuqori aniqlikda o'qiy oladi.
2. **Keng Kameralar Tahlili:** Video kadrlaridagi obyektlar (mashinalar, odamlar, xavflar) va ularning o'zaro joylashuvini aniqlaydi.
3. **Ixcham Hajm (CPU-ready):** 4-bit kvantlash va `mmproj` orqali atigi **~2.2 GB RAM** bilan ishlaydi, oddiy noutbuk yoki mini-kompyuterda vizual AI yaratish imkonini beradi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `bartowski/Qwen2-VL-2B-Instruct-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (~1.4 GB) + `mmproj-f16` (~850 MB) |
| **Parametrlar soni** | **2.21B** (Vision Encoder + LLM Backbone) |
| **Modaliteti** | Matn + Tasvir (JPG, PNG, WebP) |
| **RAM / VRAM sarfi** | **~2.2 – 3.0 GB** |
| **Qo'llanish sohalari** | Video monitoring, avtomatik chek/hujjat o'qish (OCR), smart kameralar |

---

*(Real test sinovlari va benchmark jadvallari navbatdagi qadamda to'ldiriladi)*
