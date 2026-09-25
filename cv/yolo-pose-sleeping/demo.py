#!/usr/bin/env python3
"""
YOLO Pose & Workplace Sleeping / Fatigue Analyzer
Part of 100-OpenSource-Models-Review (CV Series)

17-Keypoint Human Skeleton Analysis for Workplace Fatigue, Sleep Risk,
Head-on-Desk Posture, and Ergonomic Health Telemetry.
"""

import argparse
import os
import sys
import time
import math
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# 17 COCO Keypoints connection lines (Skeleton pairs)
SKELETON_PAIRS = [
    (0, 1), (0, 2), (1, 3), (2, 4),           # Face (nose, eyes, ears)
    (5, 6),                                    # Shoulders
    (5, 7), (7, 9),                            # Left arm (shoulder -> elbow -> wrist)
    (6, 8), (8, 10),                           # Right arm (shoulder -> elbow -> wrist)
    (5, 11), (6, 12), (11, 12)                 # Torso (shoulders -> hips)
]


def analyze_posture(keypoints, confs=None):
    """
    Analyze 2D keypoints to determine posture state:
    Keypoints: shape (17, 2)
    0: Nose, 1: L-Eye, 2: R-Eye, 3: L-Ear, 4: R-Ear
    5: L-Shoulder, 6: R-Shoulder
    7: L-Elbow, 8: R-Elbow
    9: L-Wrist, 10: R-Wrist
    """
    nose = keypoints[0]
    l_shoulder, r_shoulder = keypoints[5], keypoints[6]
    l_wrist, r_wrist = keypoints[9], keypoints[10]

    # Calculate shoulder midpoint
    shoulder_y = (l_shoulder[1] + r_shoulder[1]) / 2.0
    shoulder_w = abs(r_shoulder[0] - l_shoulder[0])

    # Check valid detection
    if shoulder_w < 10:
        return "Normal", (0, 255, 0), "Tana aniqlanmadi"

    # Head drop check: Nose lower than or very close to shoulder level
    head_drop = (nose[1] - shoulder_y)

    # Check if hands are near face (phone posture)
    hand_near_face = False
    for wrist in [l_wrist, r_wrist]:
        if wrist[0] > 0 and wrist[1] > 0:
            dist = math.hypot(wrist[0] - nose[0], wrist[1] - nose[1])
            if dist < shoulder_w * 0.7:
                hand_near_face = True
                break

    if head_drop > -15:
        return "UYQU XAVFI", (0, 0, 255), "Bosh stolga tushgan / Charchoq"
    elif hand_near_face:
        return "TELEFON / QO'L YUZDA", (0, 165, 255), "Qo'l yuz sohasida"
    else:
        return "HUSHYOR / ISHDA", (0, 255, 100), "Normal ish holati"


def draw_hud(frame, fps=0.0, posture_status="Normal", color=(0, 255, 0)):
    """Draw ergonomic posture telemetry HUD."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (20, 24, 28), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    cv2.putText(frame, "YOLO Pose Fatigue & Sleeping Analyzer", (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 230, 255), 2)
    cv2.putText(frame, f"Holat: {posture_status}", (15, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, color, 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 140, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 120), 2)


def process_pose(frame, results, conf_thresh=0.3):
    """Draw skeleton and evaluate posture."""
    status = "Odam aniqlanmadi"
    status_color = (180, 180, 180)

    for r in results:
        if r.keypoints is None or len(r.keypoints.data) == 0:
            continue

        for kp_data in r.keypoints.data:
            kps = kp_data.cpu().numpy() # shape (17, 3) or (17, 2)
            pts = kps[:, :2]

            status, status_color, desc = analyze_posture(pts)

            # Draw skeleton bones
            for p1_idx, p2_idx in SKELETON_PAIRS:
                pt1 = (int(pts[p1_idx][0]), int(pts[p1_idx][1]))
                pt2 = (int(pts[p2_idx][0]), int(pts[p2_idx][1]))

                if pt1[0] > 0 and pt1[1] > 0 and pt2[0] > 0 and pt2[1] > 0:
                    cv2.line(frame, pt1, pt2, (0, 255, 200), 2)

            # Draw keypoint dots
            for pt in pts:
                px, py = int(pt[0]), int(pt[1])
                if px > 0 and py > 0:
                    cv2.circle(frame, (px, py), 4, (0, 120, 255), -1)

    return status, status_color


def run_image(model, image_path: str, output_path: str = None, conf: float = 0.3, headless: bool = False):
    """Inference on single image."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to load '{image_path}'")
        sys.exit(1)

    t0 = time.time()
    results = model(frame, conf=conf, verbose=False)
    infer_time = (time.time() - t0) * 1000.0

    status, status_color = process_pose(frame, results, conf)
    draw_hud(frame, fps=1000.0 / max(infer_time, 0.1), posture_status=status, color=status_color)

    print(f"Processed '{image_path}' in {infer_time:.2f}ms | Posture status: {status}")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, frame)
        print(f"Annotated result saved to: {output_path}")

    if not headless:
        cv2.imshow("YOLO Pose Sleeping Analysis", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_camera(model, cam_source, conf: float = 0.3, output_path: str = None, headless: bool = False):
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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = model(frame, conf=conf, verbose=False)
        status, status_color = process_pose(frame, results, conf)

        now = time.time()
        if now - fps_start >= 1.0:
            fps = frame_count / (now - fps_start)
            frame_count = 0
            fps_start = now

        draw_hud(frame, fps=fps, posture_status=status, color=status_color)

        if output_path and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))

        if writer:
            writer.write(frame)

        if not headless:
            cv2.imshow("YOLO Pose Sleeping Analysis", frame)
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
    parser = argparse.ArgumentParser(description="YOLO Pose Fatigue & Sleeping Analyzer")
    parser.add_argument("--source", type=str, default="data/test_1.jpg",
                        help="Camera ID, video path, or image path.")
    parser.add_argument("--weights", type=str, default="yolo11n-pose.pt",
                        help="Weights path (default: yolo11n-pose.pt).")
    parser.add_argument("--conf", type=float, default=0.3,
                        help="Confidence threshold (default: 0.3).")
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

    print(f"Loading YOLO Pose '{args.weights}' on {device}...")
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
