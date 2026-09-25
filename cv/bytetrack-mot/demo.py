#!/usr/bin/env python3
"""
ByteTrack Multi-Object Tracking (MOT) & Trajectory Analysis (Model #27)
Part of 100-OpenSource-Models-Review (CV Series)

SOTA Multi-Object Tracking by Associating Every Detection Box (ECCV 2022).
Persistent ID assignment, occlusion recovery, Kalman trajectory smoothing,
and unique visitor/occupancy counting.
"""

import argparse
import os
import sys
import time
from collections import defaultdict
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Distinct color palette for tracks
TRACK_COLORS = [
    (0, 255, 100), (255, 128, 0), (0, 220, 255), (255, 0, 200),
    (0, 165, 255), (255, 220, 0), (160, 0, 255), (0, 255, 220)
]


def get_color(track_id: int):
    return TRACK_COLORS[track_id % len(TRACK_COLORS)]


def draw_hud(frame, fps=0.0, active_tracks=0, total_unique=0):
    """Draw tracking telemetry HUD."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (20, 24, 28), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    cv2.putText(frame, "ByteTrack Multi-Object Tracker", (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 230, 255), 2)
    cv2.putText(frame, f"Aktiv odamlar: {active_tracks} | Jami kuzatilgan: {total_unique}", (15, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 210, 220), 1)
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 140, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 120), 2)


def process_tracking(frame, results, track_history, unique_ids_set):
    """Draw bounding boxes with persistent IDs and trajectory trails."""
    active_count = 0

    for r in results:
        boxes = r.boxes
        if boxes.id is None:
            continue

        for box in boxes:
            cls_id = int(box.cls[0])
            if cls_id != 0:  # Only track people (person = 0)
                continue

            track_id = int(box.id[0])
            conf = float(box.conf[0])
            unique_ids_set.add(track_id)
            active_count += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = get_color(track_id)

            # Center point
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Track history
            track_history[track_id].append((cx, cy))
            if len(track_history[track_id]) > 30:
                track_history[track_id].pop(0)

            # Draw trajectory trail
            pts = track_history[track_id]
            for i in range(1, len(pts)):
                cv2.line(frame, pts[i - 1], pts[i], color, 2)

            # Draw box & center dot
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

            # Tag
            label = f"ID #{track_id} ({conf * 100:.0f}%)"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.50, 1)
            cv2.rectangle(frame, (x1, max(0, y1 - 22)), (x1 + tw + 6, max(0, y1)), color, -1)
            cv2.putText(frame, label, (x1 + 3, max(0, y1 - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 0), 1)

    return active_count


def run_image(model, image_path: str, output_path: str = None, conf: float = 0.4, headless: bool = False):
    """Single static image test for ByteTrack."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to load '{image_path}'")
        sys.exit(1)

    t0 = time.time()
    # In static image mode, track with persist=False
    results = model.track(frame, persist=False, classes=[0], conf=conf, tracker="bytetrack.yaml", verbose=False)
    infer_time = (time.time() - t0) * 1000.0

    track_history = defaultdict(list)
    unique_set = set()
    active = process_tracking(frame, results, track_history, unique_set)

    draw_hud(frame, fps=1000.0 / max(infer_time, 0.1), active_tracks=active, total_unique=len(unique_set))
    print(f"Processed '{image_path}' in {infer_time:.2f}ms | Tracked {active} persons.")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, frame)
        print(f"Annotated result saved to: {output_path}")

    if not headless:
        cv2.imshow("ByteTrack MOT", frame)
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
        print(f"Error: Unable to open stream '{cam_source}'")
        sys.exit(1)

    print(f"Stream opened: {cam_source}. Press 'q' to quit.")

    writer = None
    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    track_history = defaultdict(list)
    unique_ids_set = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = model.track(frame, persist=True, classes=[0], conf=conf, tracker="bytetrack.yaml", verbose=False)
        active = process_tracking(frame, results, track_history, unique_ids_set)

        now = time.time()
        if now - fps_start >= 1.0:
            fps = frame_count / (now - fps_start)
            frame_count = 0
            fps_start = now

        draw_hud(frame, fps=fps, active_tracks=active, total_unique=len(unique_ids_set))

        if output_path and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))

        if writer:
            writer.write(frame)

        if not headless:
            cv2.imshow("ByteTrack MOT", frame)
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
    parser = argparse.ArgumentParser(description="ByteTrack Multi-Object Tracking")
    parser.add_argument("--source", type=str, default="data/test_1.jpg",
                        help="Camera ID, video path, or image path.")
    parser.add_argument("--weights", type=str, default="yolo11n.pt",
                        help="Detector weights (default: yolo11n.pt).")
    parser.add_argument("--conf", type=float, default=0.4,
                        help="Confidence threshold (default: 0.4).")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to save annotated output.")
    parser.add_argument("--headless", action="store_true",
                        help="Run without displaying OpenCV window.")
    parser.add_argument("--device", type=str, default="auto",
                        choices=["auto", "cuda", "cpu"])

    args = parser.parse_args()

    if args.device == "cuda":
        device = "cuda:0"
    elif args.device == "cpu":
        device = "cpu"
    else:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

    print(f"Loading detector weights '{args.weights}' on {device}...")
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
            print(f"Unsupported format: {ext}")
            sys.exit(1)
    else:
        print(f"Source '{args.source}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
