import argparse
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(
        description="Smart Office & Classroom Energy Occupancy Guardian using YOLOv5n"
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
        default="yolov5nu.pt",
        help="YOLOv5n model weight checkpoint.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Confidence threshold for person & object detection.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window and save output image/video directly.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_office.jpg",
        help="Output image/video path when running in headless mode.",
    )
    return parser.parse_args()


def draw_hud(frame, occupant_count, laptop_count, fps, device_str, empty_timer):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # Determine energy states
    is_occupied = occupant_count > 0
    if is_occupied:
        header_color = (46, 204, 113)  # Emerald Green
        status_text = "ROOM OCCUPIED - ACTIVE"
        hvac_state = "CLIMATE CONTROL: COMFORT 21°C"
        lighting_state = "LIGHTING GRID: 100% (480 W)"
        eco_saving = "SAVING: 0% (Standard Draw)"
    else:
        header_color = (0, 165, 255)  # Amber / Warning
        status_text = f"ROOM VACANT - STANDBY ({max(0, 10 - int(empty_timer))}s TO ECO)"
        if empty_timer > 5.0:
            hvac_state = "CLIMATE CONTROL: ECO STANDBY 18°C"
            lighting_state = "LIGHTING GRID: 10% NIGHT (48 W)"
            eco_saving = "ECO-SAVINGS: 90% (Est. $0.12/hr)"
        else:
            hvac_state = "CLIMATE CONTROL: TRANSITIONING"
            lighting_state = "LIGHTING GRID: DIMMING..."
            eco_saving = "ECO-SAVINGS: CALCULATING..."

    # Top Control Dashboard Bar
    # Top Control Dashboard Bar - Solid dark panel for high contrast
    cv2.rectangle(frame, (20, 20), (560, 195), (20, 22, 25), -1)

    cv2.rectangle(frame, (20, 20), (560, 195), header_color, 2)
    cv2.putText(
        frame,
        "ECOSENSOR: ENERGY OCCUPANCY GUARDIAN",
        (35, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"STATUS: {status_text}",
        (35, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.54,
        header_color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Occupant Count: {occupant_count} | Active Workstations: {laptop_count}",
        (35, 102),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (240, 240, 240),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"{hvac_state}",
        (35, 128),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (0, 220, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"{lighting_state}",
        (35, 154),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (100, 240, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"{eco_saving}",
        (35, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        header_color,
        2,
        cv2.LINE_AA,
    )

    # Telemetry badge top-right - Solid dark background
    badge_w, badge_h = 240, 75
    badge_x = w - badge_w - 20
    cv2.rectangle(
        frame, (badge_x, 20), (badge_x + badge_w, 20 + badge_h), (20, 22, 25), -1
    )
    cv2.rectangle(
        frame, (badge_x, 20), (badge_x + badge_w, 20 + badge_h), (100, 100, 100), 1
    )
    cv2.putText(
        frame,
        f"Inference: YOLOv5n",
        (badge_x + 12, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (0, 230, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Device: {device_str} | FPS: {fps:.1f}",
        (badge_x + 12, 72),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (230, 230, 230),
        1,
        cv2.LINE_AA,
    )


def run_pipeline(args):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"[YOLOv5n EcoSensor] Initializing on device: {device}")
    model = YOLO(args.model)

    is_webcam = args.source.isdigit()
    is_image = any(args.source.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"])

    if is_image:
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error: Unable to open image '{args.source}'")
            sys.exit(1)
        start_t = time.time()
        results = model.predict(source=img, conf=args.conf, device=device, verbose=False)[0]
        proc_time = time.time() - start_t
        fps = 1.0 / max(proc_time, 1e-5)

        occupant_count = 0
        laptop_count = 0
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = model.names.get(cls_id, "")
            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            if cls_name == "person":
                occupant_count += 1
                color = (0, 255, 0)
                label = f"Occupant {occupant_count}: {conf:.2f}"
            elif cls_name in ["laptop", "tv", "cell phone"]:
                laptop_count += 1
                color = (255, 200, 0)
                label = f"Workstation ({cls_name}): {conf:.2f}"
            else:
                color = (180, 180, 180)
                label = f"{cls_name}: {conf:.2f}"

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                img,
                label,
                (x1, max(20, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
                cv2.LINE_AA,
            )

        draw_hud(img, occupant_count, laptop_count, fps, device, empty_timer=0.0)
        cv2.imwrite(args.output, img)
        print(f"Result saved to {args.output}")
        print(f"Room Occupancy Audit: {occupant_count} occupants, {laptop_count} active workstations.")
        return

    source_val = int(args.source) if is_webcam else args.source
    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        print(f"Error: Unable to open video source '{args.source}'")
        sys.exit(1)

    prev_time = time.time()
    empty_duration = 0.0
    last_occupied_time = time.time()

    print("[YOLOv5n EcoSensor] Live streaming initiated. Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-5)
        prev_time = curr_time

        results = model.predict(source=frame, conf=args.conf, device=device, verbose=False)[0]

        occupant_count = 0
        laptop_count = 0
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = model.names.get(cls_id, "")
            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            if cls_name == "person":
                occupant_count += 1
                color = (0, 255, 0)
                label = f"Occupant: {conf:.2f}"
            elif cls_name in ["laptop", "tv", "cell phone"]:
                laptop_count += 1
                color = (255, 200, 0)
                label = f"{cls_name}: {conf:.2f}"
            else:
                continue

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                label,
                (x1, max(20, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2,
                cv2.LINE_AA,
            )

        if occupant_count > 0:
            last_occupied_time = curr_time
            empty_duration = 0.0
        else:
            empty_duration = curr_time - last_occupied_time

        draw_hud(frame, occupant_count, laptop_count, fps, device, empty_duration)

        if not args.headless:
            cv2.imshow("YOLOv5n Smart Energy Occupancy Guardian", frame)
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
