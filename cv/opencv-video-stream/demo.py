#!/usr/bin/env python3
"""
OpenCV Video Stream & Ingestion Pipeline
Part of 100-OpenSource-Models-Review (CV Series)

Zero-latency video ingestion, frame buffering, real-time FPS telemetry,
aspect-ratio resizing, and HUD graphics compositing for edge/monitoring cameras.
"""

import argparse
import os
import sys
import time
import cv2
import numpy as np


def draw_hud(frame, fps=0.0, frame_count=0, latency_ms=0.0, source_info=""):
    """Draw professional monitoring telemetry HUD on the frame."""
    h, w = frame.shape[:2]
    
    # Top banner
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 50), (20, 24, 28), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
    
    # Text headers
    cv2.putText(frame, "OpenCV Video Stream Engine", (15, 26),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 255), 2)
    cv2.putText(frame, f"Src: {source_info} | Res: {w}x{h}", (15, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.40, (180, 190, 200), 1)

    # Telemetry metrics
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 230, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 120), 2)
    cv2.putText(frame, f"Latency: {latency_ms:.2f} ms", (w - 230, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 200, 50), 1)
    cv2.putText(frame, f"Frame: #{frame_count}", (w - 100, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)

    # Crosshair / Corner brackets
    pad = 25
    cv2.rectangle(frame, (pad, 65), (w - pad, h - pad), (60, 70, 80), 1)
    # Corner markers
    clen = 15
    # Top-left
    cv2.line(frame, (pad, 65), (pad + clen, 65), (0, 230, 255), 2)
    cv2.line(frame, (pad, 65), (pad, 65 + clen), (0, 230, 255), 2)
    # Top-right
    cv2.line(frame, (w - pad, 65), (w - pad - clen, 65), (0, 230, 255), 2)
    cv2.line(frame, (w - pad, 65), (w - pad, 65 + clen), (0, 230, 255), 2)
    # Bottom-left
    cv2.line(frame, (pad, h - pad), (pad + clen, h - pad), (0, 230, 255), 2)
    cv2.line(frame, (pad, h - pad), (pad, h - pad - clen), (0, 230, 255), 2)
    # Bottom-right
    cv2.line(frame, (w - pad, h - pad), (w - pad - clen, h - pad), (0, 230, 255), 2)
    cv2.line(frame, (w - pad, h - pad), (w - pad, h - pad - clen), (0, 230, 255), 2)


def run_image(image_path: str, output_path: str = None, headless: bool = False):
    """Process a single static test frame."""
    t0 = time.time()
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to load image from '{image_path}'")
        sys.exit(1)
        
    latency_ms = (time.time() - t0) * 1000.0
    draw_hud(frame, fps=1000.0 / max(latency_ms, 0.01), frame_count=1,
             latency_ms=latency_ms, source_info=os.path.basename(image_path))

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, frame)
        print(f"Saved processed frame to: {output_path} (Latency: {latency_ms:.2f}ms)")

    if not headless:
        cv2.imshow("OpenCV Stream Pipeline", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_camera(cam_source, output_path: str = None, headless: bool = False):
    """Process live video stream from webcam or RTSP URL."""
    try:
        source_idx = int(cam_source)
    except ValueError:
        source_idx = cam_source

    cap = cv2.VideoCapture(source_idx)
    if not cap.isOpened():
        print(f"Error: Could not open camera / stream '{cam_source}'")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print(f"Connected to stream: {cam_source}")
    print("Press 'q' in video window to exit, 's' to save screenshot.")

    writer = None
    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    while True:
        t_start = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Stream ended or failed to read frame.")
            break

        frame_count += 1
        t_end = time.time()
        latency_ms = (t_end - t_start) * 1000.0

        if t_end - fps_start >= 1.0:
            fps = frame_count / (t_end - fps_start)
            frame_count = 0
            fps_start = t_end

        draw_hud(frame, fps=fps, frame_count=frame_count, latency_ms=latency_ms,
                 source_info=str(cam_source))

        if output_path and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))

        if writer:
            writer.write(frame)

        if not headless:
            cv2.imshow("OpenCV Stream Pipeline", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                snap_path = f"snapshot_{int(time.time())}.jpg"
                cv2.imwrite(snap_path, frame)
                print(f"Snapshot saved: {snap_path}")
        else:
            # Headless run guard
            if frame_count > 60:
                break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="OpenCV Video Stream & Ingestion Pipeline")
    parser.add_argument("--source", type=str, default="data/test_1.jpg",
                        help="Camera ID (0, 1), RTSP URL, or path to image/video file.")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to save output image or video.")
    parser.add_argument("--headless", action="store_true",
                        help="Run in headless mode without X11 GUI window.")

    args = parser.parse_args()

    if args.source.isdigit():
        run_camera(int(args.source), args.output, args.headless)
    elif args.source.startswith("rtsp://") or args.source.startswith("http://"):
        run_camera(args.source, args.output, args.headless)
    elif os.path.isfile(args.source):
        ext = os.path.splitext(args.source)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            run_image(args.source, args.output, args.headless)
        elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
            run_camera(args.source, args.output, args.headless)
        else:
            print(f"Unsupported file format: {ext}")
            sys.exit(1)
    else:
        print(f"Error: source '{args.source}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
