import argparse
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle"}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Legacy CPU Automated Vehicle Presence & Parking Gate Actuator using YOLOv3-tiny"
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
        default="yolov3-tinyu.pt",
        help="YOLOv3-tiny model weight checkpoint.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.30,
        help="Detection confidence threshold.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window and save output directly.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_gate.jpg",
        help="Output image/video path when running in headless mode.",
    )
    return parser.parse_args()


def draw_hud(frame, vehicles, gate_open, dwell_time, fps, device_str):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # Determine Gate State & Visual Color
    if gate_open:
        gate_status = "BOOM BARRIER: RAISED (ENTRY PERMITTED)"
        gate_color = (0, 255, 100)  # Green
        actuator_state = f"RELAY ACTUATOR: OPEN (Dwell: {dwell_time:.1f}s)"
    else:
        gate_status = "BOOM BARRIER: LOWERED (RESTRICTED ACCESS)"
        gate_color = (0, 0, 255)    # Red
        actuator_state = "RELAY ACTUATOR: STANDBY / LOCKED"

    # Top Control Dashboard Panel
    cv2.rectangle(overlay, (20, 20), (560, 180), (20, 25, 30), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    cv2.rectangle(frame, (20, 20), (560, 180), gate_color, 2)

    cv2.putText(
        frame,
        "GATEKEEPER-3: BOOM BARRIER CONTROLLER",
        (35, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.56,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        gate_status,
        (35, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        gate_color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Incoming Vehicles: {len(vehicles)} | {actuator_state}",
        (35, 102),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (220, 220, 220),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Security Mode: AUTOMATIC RFID / LPR SENSOR LINK ACTIVE",
        (35, 128),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (100, 220, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Hardware Target: LEGACY CPU / SBC OPTIMIZED",
        (35, 154),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (200, 240, 180),
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
        "Inference: YOLOv3-tiny",
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

    # Virtual Gate Barrier Line across lower frame
    gate_y = int(h * 0.72)
    line_color = (0, 255, 100) if gate_open else (0, 0, 255)
    cv2.line(frame, (40, gate_y), (w - 40, gate_y), line_color, 3, cv2.LINE_AA)
    cv2.putText(
        frame,
        "[ BARRIER PERIMETER THRESHOLD ]",
        (w // 2 - 130, gate_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.46,
        line_color,
        2,
        cv2.LINE_AA,
    )


def process_frame(frame, model, args, device):
    results = model.predict(source=frame, conf=args.conf, device=device, verbose=False)[0]

    vehicles = []
    for box in results.boxes:
        cls_id = int(box.cls[0].item())
        cls_name = model.names.get(cls_id, "")
        conf = float(box.conf[0].item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        if cls_name not in VEHICLE_CLASSES:
            continue

        vehicles.append({"box": (x1, y1, x2, y2), "class": cls_name, "conf": conf})

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 220, 255), 2)
        cv2.putText(
            frame,
            f"VEHICLE [{cls_name.upper()}]: {conf:.2f}",
            (x1, max(20, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (0, 220, 255),
            2,
            cv2.LINE_AA,
        )

    return vehicles


def run_pipeline(args):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"[YOLOv3-tiny GateKeeper-3] Initializing on device: {device}")
    model = YOLO(args.model)

    is_webcam = args.source.isdigit()
    is_image = any(args.source.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"])

    if is_image:
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error: Unable to open image '{args.source}'")
            sys.exit(1)
        start_t = time.time()
        vehicles = process_frame(img, model, args, device)
        proc_time = time.time() - start_t
        fps = 1.0 / max(proc_time, 1e-5)

        gate_open = len(vehicles) > 0
        draw_hud(img, vehicles, gate_open, dwell_time=0.0, fps=fps, device_str=device)
        cv2.imwrite(args.output, img)
        print(f"Result saved to {args.output}")
        print(
            f"Gatekeeper Audit: {len(vehicles)} vehicle(s) approaching. Gate status: {'OPEN' if gate_open else 'CLOSED'}."
        )
        return

    source_val = int(args.source) if is_webcam else args.source
    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        print(f"Error: Unable to open video source '{args.source}'")
        sys.exit(1)

    prev_time = time.time()
    last_seen_vehicle_time = 0.0
    HOLD_OPEN_SECS = 4.0

    print("[YOLOv3-tiny GateKeeper-3] Live gate monitor running. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-5)
        prev_time = curr_time

        vehicles = process_frame(frame, model, args, device)

        if len(vehicles) > 0:
            last_seen_vehicle_time = curr_time
            gate_open = True
            dwell_time = 0.0
        else:
            time_since_clear = curr_time - last_seen_vehicle_time
            if time_since_clear < HOLD_OPEN_SECS and last_seen_vehicle_time > 0:
                gate_open = True
                dwell_time = HOLD_OPEN_SECS - time_since_clear
            else:
                gate_open = False
                dwell_time = 0.0

        draw_hud(frame, vehicles, gate_open, dwell_time, fps, device)

        if not args.headless:
            cv2.imshow("YOLOv3-tiny Automated GateKeeper", frame)
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
