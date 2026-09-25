# BGE-M3 (BAAI General Embedding)

> **100-OpenSource-Models-Review | Model #44**  
> **Kategoriya:** Semantik Qidiruv, RAG & Ko'p Tilli Vektorli Embedding  
> **Ishlab chiquvchi:** BAAI (Beijing Academy of Artificial Intelligence)  
> **Vektor o'lchami:** 1,024 dimensions  
> **Kontekst oynasi:** **8,192 token** (Uzoq matnlarni to'liq qamrab oladi)  
> **Til qamrovi:** 100+ tillar (O'zbek, Rus, Ingliz va boshqalar)  
> **Inference Engine:** `transformers` / `torch` / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature"

BGE-M3 — zamonaviy RAG (Retrieval-Augmented Generation) va semantik qidiruv tizimlarining jahon miqyosidagi eng kuchli modelidir. "M3" belgisi modelning 3 ta fundamental ustunligini anglatadi:
1. **Multi-Linguality:** 100 dan ortiq tillarda o'qitilgan. O'zbek tilidagi so'rov orqali ingliz tilidagi texnik hujjatlar ichidan eng to'g'ri bo'lakni topib bera oladi (Cross-lingual search).
2. **Multi-Functionality:** Bir vaqtning o'zida ham zich vektor (Dense), ham kalit so'z qidiruvi (Sparse/BM25), ham ko'p vektorli (ColBERT multi-vector) qidiruvni birlashtiradi.
3. **Multi-Granularity:** 8,192 tokenlik kontekst oynasi yordamida nafaqat bitta gapni, balki butun boshli kitob sahifalari yoki texnik shartnomalarni yaxlit vektorga aylantiradi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `BAAI/bge-m3` |
| **Model hajmi** | ~2.2 GB (FP16 / INT8 optimallashtiriladi) |
| **Vektor o'lchami** | 1,024 float32 qiymat |
| **Maksimal matn uzunligi** | 8,192 tokens |
| **RAM / VRAM sarfi** | **~2.5 – 3.2 GB** |
| **Inference Tezligi** | CPU'da har bir matn uchun ~15–35 ms |

---

*(Real test sinovlari va benchmark jadvallari navbatdagi qadamda to'ldiriladi)*
