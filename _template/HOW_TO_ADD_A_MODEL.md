# Yangi model qanday qo'shiladi

## Umumiy qoida: faqat Docker

`llm/`, `tts/`, `stt/` kategoriyalaridagi barcha modellar **faqat Docker orqali** ishga tushiriladi. Sababi: bu modellarning kirish/chiqishi matn yoki audio fayl — GUI oyna yoki kamera kerak emas, shuning uchun Docker'da hech qanday murakkablik yo'q (venv/Python versiyasi bilan bosh qotirish shart emas).

**Har bir model papkasida quyidagilar bo'lishi shart:**
- `Dockerfile`
- `docker-compose.yml`
- `run.sh` (qulaylik uchun, `docker compose up --build`ni chaqiradi)
- `demo.py` (yoki mos nom) — asosiy skript
- `requirements.txt`
- `README.md` — ichida **faqat** Docker orqali ishga tushirish ko'rsatmasi (`_template/README_RUN_SECTION.md`dan nusxa olib, `<kategoriya>` va `<model-nomi>`ni almashtiring)

## Yagona istisno: CV kategoriyasi (GUI/kamera kerak bo'lganda)

Agar model kameradan real-time video oladi va natijani vizual (bounding box, oyna) ko'rsatishi kerak bo'lsa (masalan YOLOv8n kabi) — bu holatda **ikkita rejim** beriladi:
- **Native (venv)** — GUI oynasi bilan, vizual tekshirish uchun (tavsiya etiladigan)
- **Docker (headless)** — oynasiz, faqat konsolga natija, kross-platforma muammosiz ishlashi uchun

Bu istisno faqat GUI/kamera talab qiladigan modellarga tegishli. Agar model faqat matn/audio bilan ishlasa (LLM, TTS, STT — hatto ular ham ba'zan kamera bilan ishlashi mumkin bo'lsa, o'sha holatda ham CV qoidasi qo'llanadi), yuqoridagi umumiy qoida (faqat Docker) ishlatiladi.

## Yangi model qo'shish qadamlari

1. `<kategoriya>/<model-nomi>/` papkasini yarating
2. `_template/` papkasidagi `Dockerfile`, `docker-compose.yml`, `run.sh` fayllarini nusxalab, model ehtiyojiga moslang
3. `demo.py` yozing (modelni yuklab, oddiy sinov ishga tushiradigan)
4. README yozing: model haqida ma'lumot + PM uchun tezkor xulosa jadvali (GPU kerakmi, xarajat, va h.k.) + `_template/README_RUN_SECTION.md`dan Docker ko'rsatmasi
5. Bosh `README.md`dagi indeks jadvaliga bitta qator qo'shing
