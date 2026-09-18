#!/usr/bin/env python3
"""
Scaffolds folders for multiple YOLO-family models that share the
same ultralytics API. Creates demo.py, Dockerfile, requirements.txt,
and a pre-filled README.md for each.
Usage: python3 _template/scaffold-yolo-family.py
"""

import os

MODELS = [
    # (folder_name, weight_file, local_verdict, note)
    ("yolov3-tiny", "yolov3-tiny.pt", "Juda qulay", ""),
    ("yolov4-tiny", "yolov4-tiny.pt", "Juda qulay", "ultralytics'da to'g'ridan-to'g'ri yuklanmasligi mumkin — tekshirish kerak"),
    ("yolov5n", "yolov5n.pt", "Juda qulay", ""),
    ("yolov5s", "yolov5s.pt", "Juda qulay", ""),
    ("yolov5m", "yolov5m.pt", "Ishlaydi, trainingda kichik batch", ""),
    ("yolov6n", "yolov6n.pt", "Juda qulay", ""),
    ("yolov6s", "yolov6s.pt", "Juda qulay", ""),
    ("yolov7-tiny", "yolov7-tiny.pt", "Juda qulay", ""),
    ("yolov8n", "yolov8n.pt", "Juda qulay", "allaqachon mavjud, bu yerda qayta yaratilmaydi"),
    ("yolov8s", "yolov8s.pt", "Juda qulay", ""),
    ("yolov8m", "yolov8m.pt", "Ishlaydi, batch 1-4", ""),
    ("yolov9t", "yolov9t.pt", "Localga mos", ""),
    ("yolov9s", "yolov9s.pt", "Localga mos", ""),
    ("yolov10n", "yolov10n.pt", "Localga mos", ""),
    ("yolov10s", "yolov10s.pt", "Localga mos", ""),
    ("yolo11n", "yolo11n.pt", "Localga mos", ""),
    ("yolo11s", "yolo11s.pt", "Localga mos", ""),
    ("yolo11m", "yolo11m.pt", "Cheklov bilan", ""),
]

DEMO_TEMPLATE = '''import argparse
import time
from ultralytics import YOLO

def main(source: str):
    print("Loading {weight}...")
    start = time.time()
    model = YOLO("{weight}")   # birinchi marta avtomatik yuklab oladi
    print(f"Model loaded in {{time.time() - start:.2f}}s")

    start_inf = time.time()
    results = model(source)
    print(f"Inference time: {{time.time() - start_inf:.2f}}s")

    results[0].save("output.jpg")
    print("Result saved to output.jpg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str,
                         default="https://ultralytics.com/images/bus.jpg")
    args = parser.parse_args()
    main(args.source)
'''

DOCKERFILE_TEMPLATE = '''FROM ml-base-cpu:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "demo.py"]
'''

README_TEMPLATE = '''# {name}

## Overview
{name} — YOLO oilasiga mansub object detection modeli.

## Technical details
- **Weight file:** `{weight}`
- **Source:** ultralytics (avtomatik yuklanadi)

## GTX 1650 (4GB) uchun baho
- **Holat:** {verdict}
- **Eslatma:** {note}

## Resource requirements
- **CPU-only:** sinovdan o'tkazilmoqda (base image CPU uchun)
- **GPU:** ixtiyoriy, tezlashtirish uchun

## How to run

```bash
docker build -f Dockerfile.base -t ml-base-cpu:latest .
docker compose up {service_name} --build
```

## Natijalar
_(Sinovdan keyin to'ldiriladi: inference vaqti, xotira sarfi, sifat kuzatuvi)_
'''

def scaffold():
    created = 0
    for folder, weight, verdict, note in MODELS:
        path = os.path.join("cv", folder)
        if os.path.exists(path):
            print(f"⏭  {path} allaqachon mavjud, o'tkazib yuborildi")
            continue
        os.makedirs(path)

        with open(os.path.join(path, "demo.py"), "w") as f:
            f.write(DEMO_TEMPLATE.format(weight=weight))

        with open(os.path.join(path, "Dockerfile"), "w") as f:
            f.write(DOCKERFILE_TEMPLATE)

        with open(os.path.join(path, "requirements.txt"), "w") as f:
            f.write("# All dependencies already provided by the base image (ultralytics)\n")

        service_name = folder.replace("-", "_").replace(".", "_").lower()
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(README_TEMPLATE.format(
                name=folder, weight=weight, verdict=verdict,
                note=note or "—", service_name=service_name
            ))

        print(f"✅ {path} yaratildi")
        created += 1

    print(f"\n{created} ta model papkasi yaratildi.")
    print("Keyingi qadam: python3 generate-compose.py")

if __name__ == "__main__":
    scaffold()