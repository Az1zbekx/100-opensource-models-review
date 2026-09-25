#!/usr/bin/env python3
"""
YOLO Office Workspace & Object Detection
Part of 100-OpenSource-Models-Review (CV Series)

Real-time detection of people, smartphones, laptops, remotes, chairs,
and office objects with distraction detection logic and telemetry HUD.
"""

import argparse
import os
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Uzbek object mapping for office environments
UZ_CLASSES = {
    0: "Inson (Xodim)",
    67: "Telefon (Smartfon)",
    65: "Pult (Remote)",
    63: "Noutbuk (Laptop)",
    64: "Sichqoncha (Mouse)",
    66: "Klaviatura (Keyboard)",
    41: "Bakal (Cup)",
    39: "Butilka (Bottle)",
    73: "Kitob (Book)",
    56: "Kreslo (Chair)",
    47: "Olma (Apple)",
    74: "Soat (Clock)"
}

# Color palette for classes (BGR)
CLASS_COLORS = {
    0: (0, 220, 100),    # Inson - Green
    67: (0, 0, 255),     # Telefon - Red Alert
    65: (255, 120, 0),   # Pult - Orange
    63: (255, 200, 0),   # Noutbuk - Cyan/Yellow
    56: (180, 180, 180), # Kreslo - Gray
}


def draw_hud(frame, fps=0.0, counts=None, alert=False):
    """Draw professional detection HUD overlay."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (20, 24, 28), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    cv2.putText(frame, "YOLO11 Workspace Object Detector", (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 255), 2)

    stats_str = f"Inson: {counts.get(0, 0)} | Tel: {counts.get(67, 0)} | Noutbuk: {counts.get(63, 0)}"
    cv2.putText(frame, stats_str, (15, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 210, 220), 1)

    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 140, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 120), 2)

    if alert:
        # Red warning banner for phone distraction
        banner = frame.copy()
        cv2.rectangle(banner, (0, 60), (w, 95), (0, 0, 220), -1)
        cv2.addWeighted(banner, 0.80, frame, 0.20, 0, frame)
        cv2.putText(frame, "OGOHLANTIRISH: Ish joyida telefon aniqlandi!", (20, 84),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 255, 255), 2)


def process_detections(frame, results, conf_thresh=0.4):
    """Draw labeled bounding boxes and count objects."""
    counts = {}
    phone_detected = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = float(box.conf[0])
            if conf < conf_thresh:
                continue

            cls_id = int(box.cls[0])
            counts[cls_id] = counts.get(cls_id, 0) + 1

            if cls_id == 67:
                phone_detected = True

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = CLASS_COLORS.get(cls_id, (200, 150, 50))
            name = UZ_CLASSES.get(cls_id, r.names[cls_id])

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            label = f"{name} {conf * 100:.0f}%"
            (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (x1, max(0, y1 - 22)), (x1 + lw + 6, max(0, y1)), color, -1)
            cv2.putText(frame, label, (x1 + 3, max(0, y1 - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0) if cls_id != 67 else (255, 255, 255), 1)

    return counts, phone_detected


def run_image(model, image_path: str, output_path: str = None, conf: float = 0.4, headless: bool = False):
    """Inference on single static image."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to load image '{image_path}'")
        sys.exit(1)

    t0 = time.time()
    results = model(frame, verbose=False)
    infer_time = (time.time() - t0) * 1000.0

    counts, alert = process_detections(frame, results, conf)
    draw_hud(frame, fps=1000.0 / max(infer_time, 0.1), counts=counts, alert=alert)

    print(f"Processed '{image_path}' in {infer_time:.2f}ms | Objects found: {dict([(UZ_CLASSES.get(k, k), v) for k, v in counts.items()])}")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, frame)
        print(f"Annotated result saved to: {output_path}")

    if not headless:
        cv2.imshow("YOLO Workspace Detection", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_camera(model, cam_source, conf: float = 0.4, output_path: str = None, headless: bool = False):
    """Inference on camera or video stream."""
    try:
        source_idx = int(cam_source)
    except ValueError:
        source_idx = cam_source

    cap = cv2.VideoCapture(source_idx)
    if not cap.isOpened():
        print(f"Error: Could not open stream '{cam_source}'")
        sys.exit(1)

    print(f"Stream opened: {cam_source}. Press 'q' to quit.")

    writer = None
    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = model(frame, verbose=False)
        counts, alert = process_detections(frame, results, conf)

        now = time.time()
        if now - fps_start >= 1.0:
            fps = frame_count / (now - fps_start)
            frame_count = 0
            fps_start = now

        draw_hud(frame, fps=fps, counts=counts, alert=alert)

        if output_path and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))

        if writer:
            writer.write(frame)

        if not headless:
            cv2.imshow("YOLO Workspace Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            if frame_count > 60:
                break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="YOLO Office Workspace Object Detector")
    parser.add_argument("--source", type=str, default="data/test_1.jpg",
                        help="Camera ID, video path, or image path.")
    parser.add_argument("--weights", type=str, default="yolo11n.pt",
                        help="Weights path (default: yolo11n.pt).")
    parser.add_argument("--conf", type=float, default=0.4,
                        help="Confidence threshold (default: 0.4).")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to save annotated result.")
    parser.add_argument("--headless", action="store_true",
                        help="Run without displaying OpenCV window.")
    parser.add_argument("--device", type=str, default="auto",
                        choices=["auto", "cuda", "cpu"])

    args = parser.parse_args()

    # Determine device
    if args.device == "cuda":
        device = "cuda:0"
    elif args.device == "cpu":
        device = "cpu"
    else:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

    print(f"Loading YOLO model '{args.weights}' on {device}...")
    model = YOLO(args.weights)
    model.to(device)

    if args.source.isdigit():
        run_camera(model, int(args.source), args.conf, args.output, args.headless)
    elif args.source.startswith("rtsp://") or args.source.startswith("http://"):
        run_camera(model, args.source, args.conf, args.output, args.headless)
    elif os.path.isfile(args.source):
        ext = os.path.splitext(args.source)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            run_image(model, args.source, args.output, args.conf, args.headless)
        elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
            run_camera(model, args.source, args.conf, args.output, args.headless)
        else:
            print(f"Unsupported file format: {ext}")
            sys.exit(1)
    else:
        print(f"Source '{args.source}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
