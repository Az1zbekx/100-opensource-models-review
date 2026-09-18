# yolov10s

## Overview
yolov10s — YOLO oilasiga mansub object detection modeli.

## Technical details
- **Weight file:** `yolov10s.pt`
- **Source:** ultralytics (avtomatik yuklanadi)

## GTX 1650 (4GB) uchun baho
- **Holat:** Localga mos
- **Eslatma:** —

## Resource requirements
- **CPU-only:** sinovdan o'tkazilmoqda (base image CPU uchun)
- **GPU:** ixtiyoriy, tezlashtirish uchun

## How to run

```bash
docker build -f Dockerfile.base -t ml-base-cpu:latest .
docker compose up yolov10s --build
```

## Natijalar
_(Sinovdan keyin to'ldiriladi: inference vaqti, xotira sarfi, sifat kuzatuvi)_
