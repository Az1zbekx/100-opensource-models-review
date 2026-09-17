# 100 Open-Source Model Review

Bu repo — 100 ta ochiq manbali (open-source) modelni sinab ko'rish, natijalarni hujjatlashtirish va kelajakdagi loyihalarda tayyor, tekshirilgan model sifatida ishlatish maqsadida yaratilgan.

**Test muhiti:** laptop, NVIDIA GTX 1650 (4GB VRAM) — shuning uchun asosan kichik/kvantlangan modellar sinovdan o'tkaziladi. Bu — kamida GPU resursi cheklangan (O'zbekiston bozoridagi ko'p kichik-o'rta loyihalarga xos) sharoitda qaysi modellar amaliy ishlashini ko'rsatadi.

**Kategoriyalar:** LLM, CV (Computer Vision), TTS (Text-to-Speech), STT (Speech-to-Text) — o'zbek tili qo'llab-quvvatlashiga alohida e'tibor bilan.

---

## 📋 Modellar indeksi (PM uchun tezkor ko'rinish)

| Model | Kategoriya | Qaysi project ehtiyoji uchun | GPU kerakmi | Oylik xarajat (taxmin) | Backend bilan bitta serverda? | Batafsil |
|---|---|---|---|---|---|---|
| YOLOv8n | CV | Kamera orqali kuzatuv, hozirlik aniqlash, obyekt sanash | Yo'q | $0 (mavjud serverda) | ✅ Ha | [README](cv/yolov8n/README.md) |

*(Yangi model qo'shilgan sayin shu jadvalga bitta qator qo'shiladi.)*

---

## Repo tuzilishi

```
100-opensource-models-review/
├── README.md              # shu fayl — umumiy indeks
├── _template/             # yangi model qo'shish uchun shablon fayllar va qoida
├── cv/
│   └── yolov8n/           # har bir model o'z papkasida, o'z README'si bilan
├── llm/
├── tts/
├── stt/
└── benchmark_scripts/     # kategoriya bo'yicha umumiy test skriptlari
```

## Har bir model README'sida nima bor

- Model haqida texnik ma'lumot (arxitektura, parametrlar, versiyalar)
- Loyihada nima qilingani va qanday muammolarga duch kelingani
- GPU moslik va resurs talabi (CPU'da ishlaydimi, GPU kerakmi)
- Bulutda ishlatilsa taxminiy oylik xarajat
- Ishga tushirish yo'riqnomasi

## Ishga tushirish

Har bir model papkasi mustaqil — o'z `Dockerfile`, `docker-compose.yml` va `README.md` fayliga ega.

- **LLM / TTS / STT modellari** — faqat Docker orqali ishga tushiriladi (`docker compose up --build` yoki `./run.sh`), venv yoki qo'lda kutubxona o'rnatish shart emas.
- **CV modellari** (kamera/GUI kerak bo'lganda) — ikkita rejim beriladi: native (venv, GUI oynasi bilan) va Docker (headless). Sababi shu modelning o'z README'sida tushuntirilgan.

Yangi model qo'shish qoidasi va shablon fayllar — [`_template/HOW_TO_ADD_A_MODEL.md`](_template/HOW_TO_ADD_A_MODEL.md).

