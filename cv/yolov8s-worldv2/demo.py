#!/usr/bin/env python3
"""
YOLO-World (v2): Real-Time Open-Vocabulary Object Detection.

Enables zero-shot detection of arbitrary user-defined concepts via natural
language prompts, without requiring model fine-tuning or re-training.
Supports static images, video files, and live webcam feeds.
"""

import argparse
import os
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Dynamic color generator for custom vocabulary classes
np.random.seed(1337)
COLOR_CACHE = {}


def get_color(class_name: str):
    """Retrieve or generate consistent vibrant BGR color for class name."""
    if class_name not in COLOR_CACHE:
        # Generate vibrant color
        h = int(abs(hash(class_name))) % 180
        s = 200
        v = 240
        bgr = cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0][0]
        COLOR_CACHE[class_name] = (int(bgr[0]), int(bgr[1]), int(bgr[2]))
    return COLOR_CACHE[class_name]


def draw_detections(frame: np.ndarray, result, conf_threshold: float = 0.25):
    """Draws bounding boxes, labels, and extracts class statistics."""
    counts = {}
    if result.boxes is None or len(result.boxes) == 0:
        return frame, counts

    boxes = result.boxes
    for i in range(len(boxes)):
        conf = float(boxes.conf[i].item())
        if conf < conf_threshold:
            continue

        cls_id = int(boxes.cls[i].item())
        cls_name = result.names.get(cls_id, f"class_{cls_id}")
        counts[cls_name] = counts.get(cls_name, 0) + 1
        color = get_color(cls_name)

        xyxy = boxes.xyxy[i].cpu().numpy().astype(int)
        x1, y1, x2, y2 = xyxy

        # Bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)

        # Label tag
        label = f"{cls_name} {conf:.2f}"
        (tw, th), bl = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)
        tag_y1 = max(0, y1 - th - 6)
        tag_y2 = y1
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tw + 6, tag_y2), color, -1)
        cv2.putText(
            frame,
            label,
            (x1 + 3, tag_y2 - 3),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return frame, counts


def draw_hud(frame: np.ndarray, fps: float, latency_ms: float, active_classes: list, counts: dict):
    """Renders upper and lower HUD analytics banners."""
    h, w = frame.shape[:2]

    # Top HUD
    top_h = 44
    sub_top = frame[0:top_h, 0:w]
    dark_top = np.zeros(sub_top.shape, dtype=np.uint8)
    frame[0:top_h, 0:w] = cv2.addWeighted(sub_top, 0.25, dark_top, 0.75, 1.0)

    cv2.putText(
        frame,
        "YOLO-World v2 | Open-Vocabulary Zero-Shot Detector",
        (12, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    total_objs = sum(counts.values())
    telemetry = f"FPS: {fps:.1f} | Latency: {latency_ms:.1f}ms | Objects: {total_objs}"
    cv2.putText(
        frame,
        telemetry,
        (w - 420, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    # Bottom Vocabulary Strip
    bot_h = 28
    sub_bot = frame[h - bot_h:h, 0:w]
    dark_bot = np.zeros(sub_bot.shape, dtype=np.uint8)
    frame[h - bot_h:h, 0:w] = cv2.addWeighted(sub_bot, 0.25, dark_bot, 0.75, 1.0)

    vocab_str = "Prompt Vocab: [" + ", ".join(active_classes[:7])
    if len(active_classes) > 7:
        vocab_str += f", +{len(active_classes) - 7} more"
    vocab_str += "]"
    cv2.putText(
        frame,
        vocab_str,
        (12, h - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.44,
        (200, 240, 255),
        1,
        cv2.LINE_AA,
    )


def run_image(model, source_path: str, output_path: str, conf: float, active_classes: list, headless: bool):
    """Process static image file."""
    if not os.path.exists(source_path):
        print(f"Error: Source image not found at '{source_path}'")
        sys.exit(1)

    print(f"Processing image: {source_path}")
    frame = cv2.imread(source_path)
    if frame is None:
        print(f"Error: Could not decode image '{source_path}'")
        sys.exit(1)

    t0 = time.perf_counter()
    results = model(frame, conf=conf, verbose=False)
    infer_time = (time.perf_counter() - t0) * 1000.0

    result = results[0]
    annotated, counts = draw_detections(frame, result, conf_threshold=conf)
    fps_val = 1000.0 / max(infer_time, 1.0)
    draw_hud(annotated, fps_val, infer_time, active_classes, counts)

    print(f"  Inference: {infer_time:.2f} ms | Detected: {sum(counts.values())} objects")
    for cls_name, cnt in sorted(counts.items()):
        print(f"    - {cls_name}: {cnt}")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, annotated)
        print(f"  Result saved to: {output_path}")

    if not headless:
        cv2.imshow("YOLO-World Demo", annotated)
        print("Press any key to close window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_video(model, source_path: str, output_path: str, conf: float, active_classes: list, headless: bool):
    """Process video file."""
    cap = cv2.VideoCapture(source_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{source_path}'")
        sys.exit(1)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_in = cap.get(cv2.CAP_PROP_FPS) or 30.0

    out = None
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps_in, (w, h))

    print(f"Processing video: {source_path} ({w}x{h} @ {fps_in:.1f} FPS)")
    frame_idx = 0
    t_start = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        t0 = time.perf_counter()
        results = model(frame, conf=conf, verbose=False)
        infer_time = (time.perf_counter() - t0) * 1000.0

        annotated, counts = draw_detections(frame, results[0], conf_threshold=conf)
        fps_live = 1000.0 / max(infer_time, 1.0)
        draw_hud(annotated, fps_live, infer_time, active_classes, counts)

        if out:
            out.write(annotated)

        if not headless:
            cv2.imshow("YOLO-World Video", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Processing interrupted by user.")
                break

    cap.release()
    if out:
        out.release()
    if not headless:
        cv2.destroyAllWindows()

    elapsed = time.time() - t_start
    print(f"Finished {frame_idx} frames in {elapsed:.2f}s ({frame_idx / max(elapsed, 0.001):.1f} avg FPS)")
    if output_path:
        print(f"Video saved to: {output_path}")


def run_camera(model, cam_idx: int, conf: float, active_classes: list):
    """Run live real-time detection on webcam feed."""
    print(f"Connecting to webcam index {cam_idx}...")
    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {cam_idx}.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\nLive camera running!")
    print(f"Current vocabulary: {active_classes}")
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save snapshot to disk")
    print("-" * 50)

    fps_smooth = 0.0
    snapshot_idx = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Failed to grab frame from camera.")
            time.sleep(0.01)
            continue

        t0 = time.perf_counter()
        results = model(frame, conf=conf, verbose=False)
        infer_time = (time.perf_counter() - t0) * 1000.0

        fps_instant = 1000.0 / max(infer_time, 1.0)
        fps_smooth = 0.9 * fps_smooth + 0.1 * fps_instant if fps_smooth > 0 else fps_instant

        annotated, counts = draw_detections(frame, results[0], conf_threshold=conf)
        draw_hud(annotated, fps_smooth, infer_time, active_classes, counts)

        cv2.imshow("YOLO-World Live Webcam", annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Exiting live stream.")
            break
        elif key == ord("s"):
            fn = f"yoloworld_snapshot_{snapshot_idx}.jpg"
            cv2.imwrite(fn, annotated)
            print(f"Snapshot saved to: {fn}")
            snapshot_idx += 1

    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="YOLO-World v2: Open-Vocabulary Zero-Shot Object Detector"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for default webcam, video file path, or image file path.",
    )
    parser.add_argument(
        "--classes",
        type=str,
        default="person, laptop, smartphone, coffee cup, keyboard, backpack, eyeglasses, wristwatch",
        help="Comma-separated list of target vocabulary classes to detect dynamically.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path to save annotated output image or video.",
    )
    parser.add_argument(
        "--weights",
        type=str,
        default="",
        help="Path to yolov8s-worldv2.pt weights file.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for detection (default: 0.25).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode without graphical UI display.",
    )
    args = parser.parse_args()

    # Parse target vocabulary
    vocab_list = [c.strip() for c in args.classes.split(",") if c.strip()]
    if not vocab_list:
        vocab_list = ["person", "laptop", "cell phone"]

    # Resolve weights
    weights_path = args.weights
    if not weights_path:
        local_dir = os.path.dirname(os.path.abspath(__file__))
        local_weights = os.path.join(local_dir, "yolov8s-worldv2.pt")
        if os.path.exists(local_weights):
            weights_path = local_weights
        else:
            weights_path = "yolov8s-worldv2.pt"

    print(f"Loading YOLO-World v2 model: {weights_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Compute device: {device.upper()}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    model = YOLO(weights_path)
    model.to(device)

    # Set custom open vocabulary
    print(f"Setting open-vocabulary prompts: {vocab_list}")
    model.set_classes(vocab_list)

    # Route source
    if args.source.isdigit():
        cam_idx = int(args.source)
        run_camera(model, cam_idx, conf=args.conf, active_classes=vocab_list)
    elif os.path.isfile(args.source):
        ext = os.path.splitext(args.source)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
            run_image(model, args.source, args.output, args.conf, vocab_list, args.headless)
        elif ext in (".mp4", ".avi", ".mov", ".mkv"):
            run_video(model, args.source, args.output, args.conf, vocab_list, args.headless)
        else:
            print(f"Error: Unsupported file format '{ext}'")
            sys.exit(1)
    else:
        print(f"Error: Source '{args.source}' is neither a camera index nor an existing file.")
        sys.exit(1)


if __name__ == "__main__":
    main()
