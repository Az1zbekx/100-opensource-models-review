## Ishga tushirish

Bu model uchun **faqat Docker** kerak — Python, kutubxonalar yoki versiya nomuvofiqligi haqida bosh qotirish shart emas.

```bash
git clone https://github.com/<username>/100-opensource-models-review.git
cd 100-opensource-models-review/<kategoriya>/<model-nomi>

docker compose up --build
```

Yoki, qulaylik uchun:

```bash
./run.sh
```

Natija konsolga chiqadi (yoki fayl ko'rinishida bo'lsa, `output/` papkasida paydo bo'ladi).

Model birinchi ishga tushirilganda kerakli og'irliklar avtomatik yuklab olinadi — internet aloqasi kerak. Keyingi ishga tushirishlar Docker keshi tufayli tezroq bo'ladi.
