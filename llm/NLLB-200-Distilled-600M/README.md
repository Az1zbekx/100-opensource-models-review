# NLLB-200-Distilled-600M (Meta AI)

> **100-OpenSource-Models-Review | Model #46**  
> **Kategoriya:** Ko'p Tilli Mashina Tarjimasi (Neural Machine Translation)  
> **Ishlab chiquvchi:** Meta AI (No Language Left Behind)  
> **Tillar soni:** **200 ta til** (O'zbekcha lotin `uzn_Latn` va kirill `uzn_Cyrl` to'liq kiritilgan)  
> **Model hajmi:** 600M parametr (~2.4 GB FP32 / ~1.2 GB FP16)  
> **Inference Engine:** `transformers` / `torch` / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature"

NLLB-200 (No Language Left Behind) — Meta tomonidan dunyodagi 200 ta til o'rtasida to'g'ridan-to'g'ri (oraliq ingliz tilisiz) yuqori sifatli neyron tarjimani amalga oshirish uchun yaratilgan global loyihadir.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **O'zbek tiliga rasmiy yordam:** O'zbek tilining ham Lotin (`uzn_Latn`), ham Kirill (`uzn_Cyrl`) yozuvlarini chuqur grammatik qonuniyatlari bilan tushunadi.
2. **To'g'ridan-to'g'ri Tarjima (Direct Translation):** Masalan Ruscha -> O'zbekcha yoki Turkcha -> O'zbekcha tarjimada oraliq ingliz tiliga o'tmasdan ma'no yo'qotishlarini kamaytiradi.
3. **CPU da Tejamkor Ishlash:** 600M distillangan versiya oddiy CPU da har bir gapni **100–300 ms** ichida tarjima qilib beradi (RAM sarfi ~1.5 GB).

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `facebook/nllb-200-distilled-600M` |
| **Parametrlar soni** | **615 Million** |
| **Qo'llab-quvvatlanadigan tillar** | 200 ta til |
| **O'zbek tili kodlari** | `uzn_Latn` (Lotin), `uzn_Cyrl` (Kirill) |
| **RAM / VRAM sarfi** | **~1.5 – 2.0 GB** |
| **Inference Tezligi** | CPU'da har bir gap uchun ~150–350 ms |

---

*(Real test sinovlari va benchmark jadvallari navbatdagi qadamda to'ldiriladi)*
