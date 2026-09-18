# yolov4-tiny

## Overview
yolov4-tiny — YOLO oilasiga mansub object detection modeli.

## Technical details
- **Weight file:** `yolov4-tiny.pt`
- **Source:** ultralytics (avtomatik yuklanadi)

## GTX 1650 (4GB) uchun baho
- **Holat:** Juda qulay
- **Eslatma:** ultralytics'da to'g'ridan-to'g'ri yuklanmasligi mumkin — tekshirish kerak

## Resource requirements
- **CPU-only:** sinovdan o'tkazilmoqda (base image CPU uchun)
- **GPU:** ixtiyoriy, tezlashtirish uchun

## How to run

```bash
docker build -f Dockerfile.base -t ml-base-cpu:latest .
docker compose up yolov4_tiny --build
```

## Natijalar
_(Sinovdan keyin to'ldiriladi: inference vaqti, xotira sarfi, sifat kuzatuvi)_
