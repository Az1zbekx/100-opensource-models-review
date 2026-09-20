import argparse
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

LOGISTICS_CLASSES = {
    "truck": "HEAVY FREIGHT",
    "bus": "TRANSIT CARRIER",
    "car": "LIGHT FLEET / VAN",
    "motorcycle": "COURIER BIKE",
    "person": "GROUND CREW",
}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Commercial Fleet & Intermodal Logistics Yard Dispatcher using YOLOv5m"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Video source: '0' for webcam, or path to video/image file.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov5mu.pt",
        help="YOLOv5m model weight checkpoint.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Detection confidence threshold.",
    )
    parser.add_argument(
        "--max-bays",
        type=int,
        default=12,
        help="Total dock/bay capacity of the monitored logistics zone.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window and save output image/video directly.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_yard.jpg",
        help="Output image/video path when running in headless mode.",
    )
    return parser.parse_args()


def draw_hud(frame, counts, total_vehicles, crew_count, max_bays, fps, device_str):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    heavy_count = counts.get("truck", 0)
    light_count = counts.get("car", 0) + counts.get("motorcycle", 0)
    transit_count = counts.get("bus", 0)

    # Yard Utilization & Dock Capacity
    bay_occupancy_pct = min(100, int((total_vehicles / max(1, max_bays)) * 100))
    free_bays = max(0, max_bays - total_vehicles)

    # Top Control Dashboard Panel
    cv2.rectangle(overlay, (20, 20), (580, 185), (20, 25, 30), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    border_color = (0, 140, 255) if crew_count > 0 else (0, 220, 180)
    cv2.rectangle(frame, (20, 20), (580, 185), border_color, 2)

    cv2.putText(
        frame,
        "FLEETVISION-M: LOGISTICS YARD DISPATCH",
        (35, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.56,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    if crew_count > 0:
        crew_msg = f"GROUND CREW ACTIVE: {crew_count} WORKER(S) IN YARD"
        crew_color = (0, 140, 255)  # Amber warning
    else:
        crew_msg = "GROUND CREW: NO PEDESTRIANS IN TRANSIT AISLE"
        crew_color = (0, 255, 100)

    cv2.putText(
        frame,
        crew_msg,
        (35, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        crew_color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Freight: {heavy_count} Heavy | {transit_count} Transit | {light_count} Light Fleet",
        (35, 102),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (220, 220, 220),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Staging Capacity: {bay_occupancy_pct}% LOAD | {free_bays}/{max_bays} DOCK BAYS FREE",
        (35, 128),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (100, 220, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Turnaround State: DOCKING FLUID" if bay_occupancy_pct < 75 else "Turnaround State: CONGESTION THROTTLING",
        (35, 154),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (0, 255, 120) if bay_occupancy_pct < 75 else (0, 100, 255),
        1,
        cv2.LINE_AA,
    )

    # Telemetry badge top-right
    badge_w, badge_h = 240, 75
    badge_x = w - badge_w - 20
    cv2.rectangle(
        overlay, (badge_x, 20), (badge_x + badge_w, 20 + badge_h), (20, 25, 30), -1
    )
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
    cv2.rectangle(
        frame, (badge_x, 20), (badge_x + badge_w, 20 + badge_h), (80, 80, 80), 1
    )
    cv2.putText(
        frame,
        "Inference: YOLOv5m",
        (badge_x + 12, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (0, 255, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Device: {device_str} | FPS: {fps:.1f}",
        (badge_x + 12, 72),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (200, 200, 200),
        1,
        cv2.LINE_AA,
    )


def process_frame(frame, model, args, device):
    results = model.predict(source=frame, conf=args.conf, device=device, verbose=False)[0]

    counts = {}
    total_vehicles = 0
    crew_count = 0

    for box in results.boxes:
        cls_id = int(box.cls[0].item())
        raw_name = model.names.get(cls_id, "")
        conf = float(box.conf[0].item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        if raw_name not in LOGISTICS_CLASSES:
            continue

        label_name = LOGISTICS_CLASSES[raw_name]
        counts[raw_name] = counts.get(raw_name, 0) + 1

        if raw_name == "person":
            crew_count += 1
            color = (0, 255, 255)  # Yellow for personnel
        elif raw_name == "truck":
            total_vehicles += 1
            color = (0, 165, 255)  # Orange for heavy truck
        elif raw_name == "bus":
            total_vehicles += 1
            color = (255, 100, 0)  # Deep orange
        else:
            total_vehicles += 1
            color = (0, 255, 100)  # Green for light vehicles

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame,
            f"{label_name}: {conf:.2f}",
            (x1, max(20, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            color,
            2,
            cv2.LINE_AA,
        )

    return counts, total_vehicles, crew_count


def run_pipeline(args):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"[YOLOv5m FleetVision-M] Initializing on device: {device}")
    model = YOLO(args.model)

    is_webcam = args.source.isdigit()
    is_image = any(args.source.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"])

    if is_image:
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error: Unable to open image '{args.source}'")
            sys.exit(1)
        start_t = time.time()
        counts, total_vehicles, crew_count = process_frame(img, model, args, device)
        proc_time = time.time() - start_t
        fps = 1.0 / max(proc_time, 1e-5)

        draw_hud(img, counts, total_vehicles, crew_count, args.max_bays, fps, device)
        cv2.imwrite(args.output, img)
        print(f"Result saved to {args.output}")
        print(
            f"Yard Dispatch Audit: {total_vehicles} commercial vehicles, {crew_count} ground staff detected. Asset Breakdown: {counts}"
        )
        return

    source_val = int(args.source) if is_webcam else args.source
    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        print(f"Error: Unable to open video source '{args.source}'")
        sys.exit(1)

    prev_time = time.time()
    print("[YOLOv5m FleetVision-M] Live stream running. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-5)
        prev_time = curr_time

        counts, total_vehicles, crew_count = process_frame(frame, model, args, device)
        draw_hud(frame, counts, total_vehicles, crew_count, args.max_bays, fps, device)

        if not args.headless:
            cv2.imshow("YOLOv5m Commercial Fleet & Yard Dispatcher", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        else:
            cv2.imwrite(args.output, frame)
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args)
