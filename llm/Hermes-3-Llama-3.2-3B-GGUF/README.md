# Hermes-3-Llama-3.2-3B (GGUF)

> **100-OpenSource-Models-Review | Model #36**  
> **Kategoriya:** Katta Til Modellari (LLM) — Avtonom Agent & Tool-Calling  
> **Ishlab chiquvchi:** NousResearch  
> **Asosiy Arxitektura:** Meta Llama-3.2-3B asosida agentik nozik sozlangan (Fine-tuned)  
> **Format:** GGUF (`Q4_K_M`)  
> **Inference Engine:** `llama.cpp` / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature"

Hermes 3 — NousResearch tomonidan yaratilgan ochiq manbali dunyodagi eng ilg'or avtonom agent va vositalarni chaqirish (function calling) modelidir. 3B o'lchamda bo'lishiga qaramay, u murakkab JSON sxemalarini buzmasdan generatsiya qilish va ko'p bosqichli agent ish jarayonlarini boshqarishda 8B modellarga tenglashadi.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **Agentik Function Calling:** `<tools>` va `<tool_call>` teglaridan foydalanib, tashqi API'lar va SQL bazalarni aniq argumentlar bilan chaqira oladi.
2. **Qat'iy JSON Schema intizomi:** Berilgan JSON strukturasini aynan saqlaydi, qavslar va tiplarda adashmaydi.
3. **Rolli va tizimli ko'rsatmalar:** System promptga nihoyatda qat'iy bo'ysunadi (jailbreak yoki ko'rsatmadan chetga chiqish xavfi minimal).

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `NousResearch/Hermes-3-Llama-3.2-3B-GGUF` |
| **Kvantlash darajasi** | `Q4_K_M` (~2.0 GB) |
| **Parametrlar soni** | **3.21B** |
| **Kontekst oynasi** | 4,096 - 8,192 tokens |
| **RAM / VRAM sarfi** | **~2.2 – 2.8 GB** |
| **Maxsus xususiyati** | Tool use, Structured JSON, Multi-turn Agent Flow |

---

*(Real test sinovlari va benchmark jadvallari navbatdagi qadamda to'ldiriladi)*
