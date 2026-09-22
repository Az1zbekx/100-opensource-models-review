#!/usr/bin/env python3
"""
YOLO11n-Seg: Real-Time Instance Segmentation & Pixel-Accurate Object Masking.

Provides multi-class pixel-level polygon segmentation, area coverage analytics,
foreground cutout extraction, and real-time inference across webcam, video,
and static imagery.
"""

import argparse
import os
import sys
import time
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Distinct color palette for 80 COCO classes (BGR format)
np.random.seed(42)
CLASS_COLORS = np.random.randint(40, 240, size=(80, 3), dtype=np.uint8)


def get_color(class_id: int):
    """Retrieve consistent BGR color for class id."""
    idx = int(class_id) % len(CLASS_COLORS)
    return tuple(int(c) for c in CLASS_COLORS[idx])


def draw_segmentation(frame: np.ndarray, result, alpha: float = 0.45, draw_boxes: bool = True):
    """
    Renders polygon masks, contour borders, and bounding boxes onto frame.
    Returns annotated frame, total coverage percentage, and class counts dictionary.
    """
    h, w = frame.shape[:2]
    overlay = frame.copy()
    class_counts = {}
    total_mask_pixels = np.zeros((h, w), dtype=bool)

    if result.masks is None or len(result.masks) == 0:
        return frame, 0.0, class_counts

    boxes = result.boxes
    masks = result.masks

    # Iterate through detected instances
    for i in range(len(boxes)):
        cls_id = int(boxes.cls[i].item())
        conf = float(boxes.conf[i].item())
        cls_name = result.names.get(cls_id, f"cls_{cls_id}")
        color = get_color(cls_id)
        class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

        # Extract polygon coordinates
        poly = masks.xy[i]
        if len(poly) > 0:
            pts = np.int32([poly])
            # Draw semi-transparent filled polygon on overlay
            cv2.fillPoly(overlay, pts, color)
            # Draw solid contour border on main frame
            cv2.polylines(frame, pts, isClosed=True, color=color, thickness=2)

            # Update coverage mask
            mask_single = np.zeros((h, w), dtype=np.uint8)
            cv2.fillPoly(mask_single, pts, 1)
            total_mask_pixels = total_mask_pixels | (mask_single > 0)

        # Draw bounding box and label if requested
        if draw_boxes:
            xyxy = boxes.xyxy[i].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1, cv2.LINE_AA)

            label = f"{cls_name} {conf:.2f}"
            (tw, th), bl = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            # Label tag background
            tag_y1 = max(0, y1 - th - 6)
            tag_y2 = y1
            cv2.rectangle(frame, (x1, tag_y1), (x1 + tw + 6, tag_y2), color, -1)
            cv2.putText(
                frame,
                label,
                (x1 + 3, tag_y2 - 3),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

    # Blend overlay with original frame using alpha transparency
    cv2.addWeighted(overlay, alpha, frame, 1.0 - alpha, 0, frame)

    coverage_pct = (np.count_nonzero(total_mask_pixels) / (h * w)) * 100.0
    return frame, coverage_pct, class_counts


def draw_hud(frame: np.ndarray, fps: float, latency_ms: float, coverage_pct: float, class_counts: dict):
    """Draws upper analytics dashboard onto frame."""
    h, w = frame.shape[:2]
    # Header bar
    hud_h = 42
    sub_img = frame[0:hud_h, 0:w]
    dark_rect = np.zeros(sub_img.shape, dtype=np.uint8)
    res = cv2.addWeighted(sub_img, 0.3, dark_rect, 0.7, 1.0)
    frame[0:hud_h, 0:w] = res

    # Model Title
    cv2.putText(
        frame,
        "YOLO11n-Seg | Instance Segmentation",
        (12, 26),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    # Telemetry info
    hud_text = f"FPS: {fps:.1f} | Latency: {latency_ms:.1f}ms | Mask Area: {coverage_pct:.1f}% | Objects: {sum(class_counts.values())}"
    cv2.putText(
        frame,
        hud_text,
        (w - 530, 26),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )


def run_image(model, source_path: str, output_path: str, conf: float, alpha: float, headless: bool):
    """Process static image file with instance segmentation."""
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
    num_objects = len(result.boxes) if result.boxes is not None else 0
    annotated, coverage, counts = draw_segmentation(frame, result, alpha=alpha)
    draw_hud(annotated, fps=(1000.0 / max(infer_time, 1.0)), latency_ms=infer_time, coverage_pct=coverage, class_counts=counts)

    print(f"  Inference: {infer_time:.2f} ms | Detected: {num_objects} instances | Mask coverage: {coverage:.1f}%")
    for cls_name, cnt in sorted(counts.items()):
        print(f"    - {cls_name}: {cnt}")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, annotated)
        print(f"  Result saved to: {output_path}")

    if not headless:
        cv2.imshow("YOLO11n-Seg Demo", annotated)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_video(model, source_path: str, output_path: str, conf: float, alpha: float, headless: bool):
    """Process video file with instance segmentation."""
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

        annotated, coverage, counts = draw_segmentation(frame, results[0], alpha=alpha)
        fps_live = 1000.0 / max(infer_time, 1.0)
        draw_hud(annotated, fps_live, infer_time, coverage, counts)

        if out:
            out.write(annotated)

        if not headless:
            cv2.imshow("YOLO11n-Seg Video", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Processing interrupted by user.")
                break

    cap.release()
    if out:
        out.release()
    if not headless:
        cv2.destroyAllWindows()

    elapsed = time.time() - t_start
    print(f"Finished processing {frame_idx} frames in {elapsed:.2f}s ({frame_idx / max(elapsed, 0.001):.1f} avg FPS)")
    if output_path:
        print(f"Video saved to: {output_path}")


def run_camera(model, cam_idx: int, conf: float, alpha: float):
    """Run live real-time segmentation using webcam."""
    print(f"Connecting to webcam index {cam_idx}...")
    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {cam_idx}.")
        print("Tip: Check device connection or test with --source 1")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\nLive camera running!")
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save screenshot")
    print("  '+' / '-' - Increase/decrease mask transparency (alpha)")
    print("-" * 50)

    fps_smooth = 0.0
    screenshot_idx = 1

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

        annotated, coverage, counts = draw_segmentation(frame, results[0], alpha=alpha)
        draw_hud(annotated, fps_smooth, infer_time, coverage, counts)

        cv2.imshow("YOLO11n-Seg Live Webcam", annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Exiting live stream.")
            break
        elif key == ord("s"):
            fn = f"segmentation_snapshot_{screenshot_idx}.jpg"
            cv2.imwrite(fn, annotated)
            print(f"Saved snapshot to {fn}")
            screenshot_idx += 1
        elif key in (ord("+"), ord("=")):
            alpha = min(1.0, alpha + 0.1)
            print(f"Mask alpha: {alpha:.2f}")
        elif key in (ord("-"), ord("_")):
            alpha = max(0.1, alpha - 0.1)
            print(f"Mask alpha: {alpha:.2f}")

    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="YOLO11n-Seg Instance Segmentation & Pixel Masking Demo"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for default webcam, video file path, or image file path.",
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
        help="Path to yolo11n-seg.pt weight file (defaults to local or auto-download).",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Confidence threshold for instance detection (default: 0.35).",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.45,
        help="Transparency alpha for mask blending (0.0=clear, 1.0=opaque, default: 0.45).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode without graphical UI display.",
    )
    args = parser.parse_args()

    # Resolve weights path
    weights_path = args.weights
    if not weights_path:
        local_dir = os.path.dirname(os.path.abspath(__file__))
        local_weights = os.path.join(local_dir, "yolo11n-seg.pt")
        if os.path.exists(local_weights):
            weights_path = local_weights
        else:
            weights_path = "yolo11n-seg.pt"

    print(f"Loading YOLO11n-Seg model: {weights_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Compute device: {device.upper()}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    model = YOLO(weights_path)
    model.to(device)

    # Route source type
    if args.source.isdigit():
        cam_idx = int(args.source)
        run_camera(model, cam_idx, conf=args.conf, alpha=args.alpha)
    elif os.path.isfile(args.source):
        ext = os.path.splitext(args.source)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
            run_image(model, args.source, args.output, args.conf, args.alpha, args.headless)
        elif ext in (".mp4", ".avi", ".mov", ".mkv"):
            run_video(model, args.source, args.output, args.conf, args.alpha, args.headless)
        else:
            print(f"Error: Unsupported file format '{ext}'")
            sys.exit(1)
    else:
        print(f"Error: Source '{args.source}' is neither a camera index nor an existing file.")
        sys.exit(1)


if __name__ == "__main__":
    main()
