import argparse
import os
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

ABSENCE_THRESHOLD = 15.0
CONFIRM_FRAMES = 10

def parse_args():
    parser = argparse.ArgumentParser(
        description="Real-Time Workplace Presence & Vigilance Monitor using YOLOv8n"
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
        default="yolov8n.pt",
        help="YOLOv8n model checkpoint path.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.45,
        help="Confidence threshold for person detection.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window and save output directly.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="cv/yolov8n/data/output_1.jpg",
        help="Output path when running in headless mode.",
    )
    return parser.parse_args()


def draw_hud(frame, person_count, state, elapsed_absence, fps, device_str):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    if state == "PRESENT":
        status_color = (0, 255, 100)
        status_text = "OPERATOR PRESENT (ACTIVE)"
    elif state == "ALERTED":
        status_color = (0, 0, 255)
        status_text = f"ALERT: ABSENT FOR {elapsed_absence:.0f}s"
    else:
        status_color = (0, 165, 255)
        status_text = f"AWAY: DWELL {elapsed_absence:.0f}s"

    # Top Dashboard Bar - Solid dark panel for high contrast
    cv2.rectangle(frame, (20, 20), (560, 175), (20, 22, 25), -1)

    cv2.rectangle(frame, (20, 20), (560, 175), status_color, 2)

    cv2.putText(
        frame,
        "YOLOV8N: OPERATOR VIGILANCE MONITOR",
        (35, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.56,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"STATUS: {status_text}",
        (35, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        status_color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Personnel Detected: {person_count} | Mode: WORKSPACE VIGILANCE",
        (35, 102),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (240, 240, 240),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Absence Threshold: {ABSENCE_THRESHOLD:.0f}s (Security Timeout)",
        (35, 128),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (0, 220, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Station Security: LOCKED" if state == "ALERTED" or state == "ABSENT" else "Station Security: OPERATIONAL",
        (35, 154),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (50, 70, 255) if (state == "ALERTED" or state == "ABSENT") else (80, 255, 120),
        2,
        cv2.LINE_AA,
    )

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
        "Inference: YOLOv8n",
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


def process_frame(frame, model, args, device):
    results = model.predict(source=frame, classes=[0], conf=args.conf, device=device, verbose=False)[0]
    person_count = len(results.boxes)
    for box in results.boxes:
        conf = float(box.conf[0].item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 100), 2)
        cv2.putText(
            frame,
            f"OPERATOR: {conf:.2f}",
            (x1, max(20, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 100),
            2,
            cv2.LINE_AA,
        )
    return person_count


def run_pipeline(args):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"[YOLOv8n Vigilance] Initializing on device: {device}")
    model = YOLO(args.model)

    is_webcam = args.source.isdigit()
    is_image = any(args.source.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"])

    if is_image:
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error: Unable to open image '{args.source}'")
            sys.exit(1)
        start_t = time.time()
        person_count = process_frame(img, model, args, device)
        proc_time = time.time() - start_t
        fps = 1.0 / max(proc_time, 1e-5)

        state = "PRESENT" if person_count > 0 else "ABSENT"
        draw_hud(img, person_count, state, elapsed_absence=0.0, fps=fps, device_str=device)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        cv2.imwrite(args.output, img)
        print(f"Result saved to {args.output}")
        print(f"Presence Audit: {person_count} operator(s) detected. State: {state}")
        return

    source_val = int(args.source) if is_webcam else args.source
    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        print(f"Error: Unable to open video source '{args.source}'")
        sys.exit(1)

    state = "PRESENT"
    absence_start = None
    prev_time = time.time()

    print("[YOLOv8n Vigilance] Live stream started. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-5)
        prev_time = curr_time

        person_count = process_frame(frame, model, args, device)
        if person_count > 0:
            state = "PRESENT"
            absence_start = None
            elapsed_absence = 0.0
        else:
            if absence_start is None:
                absence_start = curr_time
            elapsed_absence = curr_time - absence_start
            if elapsed_absence >= ABSENCE_THRESHOLD:
                state = "ALERTED"
            else:
                state = "ABSENT"

        draw_hud(frame, person_count, state, elapsed_absence, fps, device)

        if not args.headless:
            cv2.imshow("YOLOv8n Operator Vigilance Monitor", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        else:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            cv2.imwrite(args.output, frame)
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args)