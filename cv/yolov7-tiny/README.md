# yolov7-tiny

## Overview
yolov7-tiny — YOLO oilasiga mansub object detection modeli.

## Technical details
- **Weight file:** `yolov7-tiny.pt`
- **Source:** ultralytics (avtomatik yuklanadi)

## GTX 1650 (4GB) uchun baho
- **Holat:** Juda qulay
- **Eslatma:** —

## Resource requirements
- **CPU-only:** sinovdan o'tkazilmoqda (base image CPU uchun)
- **GPU:** ixtiyoriy, tezlashtirish uchun

## How to run

```bash
docker build -f Dockerfile.base -t ml-base-cpu:latest .
docker compose up yolov7_tiny --build
```

## Natijalar
_(Sinovdan keyin to'ldiriladi: inference vaqti, xotira sarfi, sifat kuzatuvi)_
