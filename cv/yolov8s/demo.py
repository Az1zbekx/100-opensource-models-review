import argparse
import time
from ultralytics import YOLO

def main(source: str):
    print("Loading yolov8s.pt...")
    start = time.time()
    model = YOLO("yolov8s.pt")   # birinchi marta avtomatik yuklab oladi
    print(f"Model loaded in {time.time() - start:.2f}s")

    start_inf = time.time()
    results = model(source)
    print(f"Inference time: {time.time() - start_inf:.2f}s")

    results[0].save("output.jpg")
    print("Result saved to output.jpg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str,
                         default="https://ultralytics.com/images/bus.jpg")
    args = parser.parse_args()
    main(args.source)
