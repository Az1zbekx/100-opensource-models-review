import argparse
import os
import time
import cv2
from ultralytics import YOLO

CLASS_PERSON = 0
CONGESTION_ALERT_SECONDS = 10.0


def is_point_in_box(point, box):
    px, py = point
    bx1, by1, bx2, by2 = box
    return bx1 <= px <= bx2 and by1 <= py <= by2


def process_image(model, image_path: str, conf: float, queue_limit: int, headless: bool, output_path: str = None):
    """Analyze queue count in a static image."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not open image {image_path}")
        return

    h, w = frame.shape[:2]
    # Designated queue corridor ROI (central 80% horizontal, bottom 80% vertical)
    roi = (int(w * 0.10), int(h * 0.15), int(w * 0.90), int(h * 0.95))

    results = model(frame, conf=conf, classes=[CLASS_PERSON], verbose=False)
    boxes = results[0].boxes

    queue_count = 0
    bystander_count = 0
    persons_info = []

    # First pass: classify persons inside vs outside queue ROI
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        score = float(box.conf[0])
        foot_point = (int((x1 + x2) / 2), y2)
        in_queue = is_point_in_box(foot_point, roi)
        if in_queue:
            queue_count += 1
            persons_info.append({"coords": (x1, y1, x2, y2), "foot": foot_point, "in_queue": True, "score": score, "q_idx": queue_count})
        else:
            bystander_count += 1
            persons_info.append({"coords": (x1, y1, x2, y2), "foot": foot_point, "in_queue": False, "score": score, "q_idx": 0})

    is_congested = queue_count > queue_limit

    # Draw ROI Box
    rx1, ry1, rx2, ry2 = roi
    roi_color = (0, 0, 255) if is_congested else (0, 220, 100)
    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), roi_color, 2)
    cv2.putText(frame, "CHECKOUT QUEUE ZONE (MONITORED ROI)", (rx1 + 12, ry1 + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, roi_color, 2, cv2.LINE_AA)

    # Draw persons
    for p in persons_info:
        x1, y1, x2, y2 = p["coords"]
        foot_point = p["foot"]
        score = p["score"]

        if p["in_queue"]:
            color = (0, 0, 255) if is_congested else (0, 255, 0)
            label = f"Queue #{p['q_idx']} ({score:.2f})"
        else:
            color = (180, 185, 190)
            label = f"Shopper ({score:.2f})"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, foot_point, 4, color, -1)

        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        tag_y1 = max(0, y1 - th - 6)
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tw + 6, tag_y1 + th + 6), (15, 18, 22), -1)
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tw + 6, tag_y1 + th + 6), color, 1)
        cv2.putText(frame, label, (x1 + 3, tag_y1 + th + 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)

    # Dashboard HUD Banner
    status = "ALERT: QUEUE CONGESTION! DISPATCH BACKUP REGISTER" if is_congested else "STATUS: NORMAL QUEUE FLOW (CAPACITY NOMINAL)"
    status_color = (0, 0, 255) if is_congested else (0, 255, 0)

    hud_w = 680
    hud_h = 82
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 10 + hud_h), (15, 18, 22), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 10 + hud_h), (60, 64, 72), 1)

    cv2.putText(frame, "YOLO11s RETAIL & SERVICE QUEUE MONITOR",
                (22, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 220, 255), 1, cv2.LINE_AA)
    
    cv2.putText(frame, f"Queue Occupancy: {queue_count} (Limit: {queue_limit})  |  Bystanders: {bystander_count}  |  Total: {len(boxes)}",
                (22, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 205, 215), 1, cv2.LINE_AA)
    
    cv2.putText(frame, status,
                (22, 76), cv2.FONT_HERSHEY_SIMPLEX, 0.46, status_color, 1, cv2.LINE_AA)

    out_file = output_path if output_path else "output_queue.jpg"
    cv2.imwrite(out_file, frame)
    print(f"Result saved to {out_file}")
    print(f"People in Queue: {queue_count} (Threshold: {queue_limit}) | {status}")

    if not headless:
        cv2.imshow("YOLO11s - Retail Queue Monitor", frame)
        print("Press any key to close the window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, queue_limit: int, headless: bool):
    """Real-time video stream queue monitoring."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Queue Monitor started (source={video_source}, limit={queue_limit}).")
    print("Press 'q' in window to exit, or Ctrl+C in terminal.")

    congestion_start = None
    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            now = time.time()
            if now - fps_start >= 1.0:
                fps = frame_count / (now - fps_start)
                frame_count = 0
                fps_start = now

            h, w = frame.shape[:2]
            # Designated queue ROI area (central corridor)
            roi = (int(w * 0.20), int(h * 0.15), int(w * 0.80), int(h * 0.95))

            results = model(frame, conf=conf, classes=[CLASS_PERSON], verbose=False)
            boxes = results[0].boxes

            queue_count = 0
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                foot_point = (int((x1 + x2) / 2), y2)

                if is_point_in_box(foot_point, roi):
                    queue_count += 1
                    color = (0, 0, 255) if queue_count > queue_limit else (0, 255, 0)
                    label = f"Queue #{queue_count}"
                else:
                    color = (180, 180, 180)
                    label = "Bystander"

                if not headless:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.circle(frame, foot_point, 4, color, -1)
                    cv2.putText(frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            # Congestion logic
            if queue_count > queue_limit:
                if congestion_start is None:
                    congestion_start = now
                duration = now - congestion_start
                if duration >= CONGESTION_ALERT_SECONDS:
                    status_text = f"CONGESTION ALERT! (+{duration:.0f}s)"
                    status_color = (0, 0, 255)
                else:
                    status_text = f"Queue Building Up ({duration:.0f}s)"
                    status_color = (0, 165, 255)
            else:
                congestion_start = None
                status_text = "FLOW OPTIMAL"
                status_color = (0, 255, 0)

            if not headless:
                rx1, ry1, rx2, ry2 = roi
                cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), status_color, 2)
                cv2.putText(frame, "CHECKOUT QUEUE ZONE", (rx1 + 10, ry1 + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, status_color, 2)

                # Dashboard HUD
                cv2.rectangle(frame, (10, 10), (520, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLO11s Queue Monitor | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, f"Queue: {queue_count} / Limit: {queue_limit} | {status_text}",
                            (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
                cv2.putText(frame, f"Total In-Frame Persons: {len(boxes)}", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLO11s - Retail Queue Monitor", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Queue: {queue_count}/{queue_limit} | {status_text} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Queue monitor terminated.")


def main():
    parser = argparse.ArgumentParser(description="YOLO11s Retail Queue Length & Wait-Time Monitor")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Video source: '0' for webcam, image path, or video file path",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.45,
        help="Confidence threshold for person detection (default: 0.45)",
    )
    parser.add_argument(
        "--queue-limit",
        type=int,
        default=3,
        help="Max recommended persons in queue before alert (default: 3)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save output visualization image (default: output_queue.jpg)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI display (suitable for headless servers)",
    )
    args = parser.parse_args()

    print("Loading YOLO11s model (yolo11s.pt)...")
    model = YOLO("yolo11s.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.queue_limit, args.headless, output_path=args.output)
    else:
        process_stream(model, args.source, args.conf, args.queue_limit, args.headless)


if __name__ == "__main__":
    main()
