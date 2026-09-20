import argparse
import math
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

VEHICLE_CLASSES = {"car", "bus", "truck", "motorcycle", "bicycle"}
PEDESTRIAN_CLASSES = {"person"}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Urban Intersection & Crosswalk Safety Analyzer using YOLOv5s"
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
        default="yolov5su.pt",
        help="YOLOv5s model weight checkpoint.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Detection confidence threshold.",
    )
    parser.add_argument(
        "--proximity-thresh",
        type=float,
        default=120.0,
        help="Proximity threshold (pixels) between vehicle and pedestrian for hazard alert.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window and save output image/video directly.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_intersection.jpg",
        help="Output image/video path when running in headless mode.",
    )
    return parser.parse_args()


def draw_hud(frame, vehicles, pedestrians, hazard_pairs, fps, device_str):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    total_vehicles = len(vehicles)
    total_pedestrians = len(pedestrians)
    has_hazard = len(hazard_pairs) > 0

    # Traffic Density Category
    if total_vehicles > 8:
        density_label = "CONGESTION: HIGH"
        density_color = (0, 0, 255)
    elif total_vehicles > 3:
        density_label = "CONGESTION: MODERATE"
        density_color = (0, 200, 255)
    else:
        density_label = "CONGESTION: FLUID"
        density_color = (0, 255, 100)

    # Top Dashboard Panel
    cv2.rectangle(overlay, (20, 20), (560, 180), (20, 25, 30), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    border_color = (0, 0, 255) if has_hazard else (0, 200, 255)
    cv2.rectangle(frame, (20, 20), (560, 180), border_color, 2)

    cv2.putText(
        frame,
        "TRAFFICSIGNALIQ: INTERSECTION SAFETY",
        (35, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.56,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    if has_hazard:
        alert_text = f"COLLISION HAZARD ALERT: {len(hazard_pairs)} PAIR(S) IN PROXIMITY"
        alert_color = (0, 0, 255)
    else:
        alert_text = "CROSSWALK STATUS: SAFE DIVERGENCE"
        alert_color = (0, 255, 100)

    cv2.putText(
        frame,
        alert_text,
        (35, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        alert_color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Vehicles: {total_vehicles} | Crossing Pedestrians: {total_pedestrians}",
        (35, 102),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (220, 220, 220),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Traffic Density: {density_label}",
        (35, 128),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        density_color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Signal Advisory: EXTEND PEDESTRIAN CLEARANCE" if has_hazard else "Signal Advisory: OPTIMAL CYCLE",
        (35, 154),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 220, 100) if has_hazard else (200, 240, 200),
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
        "Inference: YOLOv5s",
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
    h, w = frame.shape[:2]
    results = model.predict(source=frame, conf=args.conf, device=device, verbose=False)[0]

    vehicles = []
    pedestrians = []

    for box in results.boxes:
        cls_id = int(box.cls[0].item())
        cls_name = model.names.get(cls_id, "")
        conf = float(box.conf[0].item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if cls_name in VEHICLE_CLASSES:
            vehicles.append({"box": (x1, y1, x2, y2), "center": (cx, cy), "class": cls_name, "conf": conf})
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 180, 0), 2)
            cv2.putText(
                frame,
                f"{cls_name.upper()}: {conf:.2f}",
                (x1, max(20, y1 - 6)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (255, 180, 0),
                2,
                cv2.LINE_AA,
            )
        elif cls_name in PEDESTRIAN_CLASSES:
            pedestrians.append({"box": (x1, y1, x2, y2), "center": (cx, cy), "conf": conf})
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(
                frame,
                f"PEDESTRIAN: {conf:.2f}",
                (x1, max(20, y1 - 6)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

    # Calculate Proximity Hazard Pairs
    hazard_pairs = []
    for v in vehicles:
        vx, vy = v["center"]
        for p in pedestrians:
            px, py = p["center"]
            dist = math.hypot(vx - px, vy - py)
            if dist < args.proximity_thresh:
                hazard_pairs.append((v, p, dist))
                # Draw hazard vector
                cv2.line(frame, (vx, vy), (px, py), (0, 0, 255), 2, cv2.LINE_AA)
                cv2.circle(frame, (vx, vy), 5, (0, 0, 255), -1)
                cv2.circle(frame, (px, py), 5, (0, 0, 255), -1)
                # Hazard indicator text
                mid_x, mid_y = (vx + px) // 2, (vy + py) // 2
                cv2.putText(
                    frame,
                    f"PROXIMITY: {int(dist)}px",
                    (mid_x, mid_y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.42,
                    (0, 0, 255),
                    1,
                    cv2.LINE_AA,
                )

    return vehicles, pedestrians, hazard_pairs


def run_pipeline(args):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"[YOLOv5s TrafficSignalIQ] Initializing on device: {device}")
    model = YOLO(args.model)

    is_webcam = args.source.isdigit()
    is_image = any(args.source.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"])

    if is_image:
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error: Unable to open image '{args.source}'")
            sys.exit(1)
        start_t = time.time()
        vehicles, pedestrians, hazard_pairs = process_frame(img, model, args, device)
        proc_time = time.time() - start_t
        fps = 1.0 / max(proc_time, 1e-5)

        draw_hud(img, vehicles, pedestrians, hazard_pairs, fps, device)
        cv2.imwrite(args.output, img)
        print(f"Result saved to {args.output}")
        print(
            f"Traffic Audit: {len(vehicles)} vehicles, {len(pedestrians)} pedestrians, {len(hazard_pairs)} collision hazards."
        )
        return

    source_val = int(args.source) if is_webcam else args.source
    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        print(f"Error: Unable to open video source '{args.source}'")
        sys.exit(1)

    prev_time = time.time()
    print("[YOLOv5s TrafficSignalIQ] Live stream running. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-5)
        prev_time = curr_time

        vehicles, pedestrians, hazard_pairs = process_frame(frame, model, args, device)
        draw_hud(frame, vehicles, pedestrians, hazard_pairs, fps, device)

        if not args.headless:
            cv2.imshow("YOLOv5s Urban TrafficSignalIQ", frame)
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
