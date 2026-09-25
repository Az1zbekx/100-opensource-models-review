# BGE-Reranker-v2-M3 (BAAI Cross-Encoder)

> **100-OpenSource-Models-Review | Model #45**  
> **Kategoriya:** Yuqori Aniqlikdagi RAG Reranking & Cross-Encoder  
> **Ishlab chiquvchi:** BAAI (Beijing Academy of Artificial Intelligence)  
> **Arxitektura:** Cross-Encoder (Query va Hujjat o'rtasida to'liq o'zaro diqqat / Full Cross-Attention)  
> **Kontekst oynasi:** **8,192 token**  
> **Format:** PyTorch / Transformers / CPU & GPU

---

## 🎯 Model Haqida va "Killer Feature"

BGE-Reranker-v2-M3 — ishlab chiqarishdagi professional RAG tizimlarida semantik qidiruv natijalarini saralash (re-ranking) bo'yicha global yetakchi modeldir. 

Bi-Encoderlar (masalan BGE-M3) katta bazadan tezkorlik bilan 50 ta nomzod hujjatni ajratib oladi. BGE-Reranker esa ushbu 50 ta nomzodning har birini savol bilan yonma-yon qo'yib, to'liq **Cross-Attention** mexanizmi orqali 0% dan 100% gacha aniq relevanlik koeffitsientini hisoblaydi va eng to'g'ri javobni 1-o'ringa chiqaradi.

### 🌟 Asosiy Ustunliklari ("Killer Feature"):
1. **False-Positive larni yo'qotish:** Bi-encoderlar chalg'ishi mumkin bo'lgan leksik yaqin, ammo ma'nosi teskari bo'lgan (hard negative) jumlalarni aniq ajratadi.
2. **100+ Tillar:** O'zbek, Rus, Ingliz va boshqa tillarda aralash qidiruvda eng yuqori baholash ko'rsatkichiga ega.
3. **8k Uzunlikdagi Matnlar:** Uzoq paragraflarni to'liq ko'rib chiqadi.

---

## 📊 Texnik Pasport

| Parametr | Qiymati |
|---|---|
| **Model nomi** | `BAAI/bge-reranker-v2-m3` |
| **Model hajmi** | ~2.2 GB (FP16 / INT8) |
| **Arxitektura turi** | Cross-Encoder (`AutoModelForSequenceClassification`) |
| **Maksimal uzunlik** | 8,192 tokens |
| **RAM / VRAM sarfi** | **~2.5 – 3.2 GB** |
| **Inference Tezligi** | CPU'da har bir juftlik uchun ~20–40 ms |

---

*(Real test sinovlari va benchmark jadvallari navbatdagi qadamda to'ldiriladi)*
