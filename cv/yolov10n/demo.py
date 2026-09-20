import argparse
import os
import time
import cv2
from ultralytics import YOLO

CLASS_PERSON = 0


def process_image(model, image_path: str, conf: float, line_ratio: float, headless: bool):
    """Process a single image with tripwire boundary evaluation."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    tripwire_y = int(h * line_ratio)

    results = model(frame, conf=conf, classes=[CLASS_PERSON], verbose=False)
    boxes = results[0].boxes

    intruders = 0
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        score = float(box.conf[0])
        foot_y = y2
        foot_x = int((x1 + x2) / 2)

        # In restricted zone (below tripwire)
        is_breach = foot_y >= tripwire_y
        if is_breach:
            intruders += 1
            color = (0, 0, 255)
            label = f"INTRUDER ({score:.2f})"
        else:
            color = (0, 255, 0)
            label = f"Authorized ({score:.2f})"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, (foot_x, foot_y), 5, color, -1)
        cv2.putText(frame, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Draw Tripwire
    line_color = (0, 0, 255) if intruders > 0 else (0, 255, 255)
    cv2.line(frame, (0, tripwire_y), (w, tripwire_y), line_color, 3)
    cv2.putText(frame, "PERIMETER SECURITY TRIPWIRE (RESTRICTED BELOW)",
                (20, tripwire_y - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, line_color, 2)

    # Status Banner
    status = f"CRITICAL: {intruders} PERIMETER BREACH(ES) DETECTED!" if intruders > 0 else "STATUS: PERIMETER CLEAR"
    banner_color = (0, 0, 255) if intruders > 0 else (0, 255, 0)

    cv2.rectangle(frame, (10, 10), (580, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLOv10n Tripwire Guardian | NMS-Free End-to-End",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, status, (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.55, banner_color, 2)

    output_path = "output_tripwire.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Perimeter Status: {status}")

    if not headless:
        cv2.imshow("YOLOv10n - Perimeter Tripwire Guardian", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, line_ratio: float, headless: bool):
    """Process live video stream with dynamic line-crossing tracking."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Tripwire Guardian initialized (source={video_source}, line_ratio={line_ratio}).")
    print("Press 'q' in video window to exit, or Ctrl+C in terminal.")

    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    previous_centroids = {}  # track coordinates across frames
    total_crossings = 0
    alert_flash_timer = 0

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
            tripwire_y = int(h * line_ratio)

            results = model(frame, conf=conf, classes=[CLASS_PERSON], verbose=False)
            boxes = results[0].boxes

            current_centroids = []
            active_intruders = 0

            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                score = float(box.conf[0])
                foot_pt = (int((x1 + x2) / 2), y2)
                current_centroids.append(foot_pt)

                # Check breach
                if foot_pt[1] >= tripwire_y:
                    active_intruders += 1
                    color = (0, 0, 255)
                    label = f"INTRUDER {score:.2f}"
                else:
                    color = (0, 255, 0)
                    label = f"Safe {score:.2f}"

                if not headless:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.circle(frame, foot_pt, 5, color, -1)
                    cv2.putText(frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            # Detect line crossings
            for c in current_centroids:
                # If someone recently crossed above -> below
                for prev_c in previous_centroids.values():
                    if prev_c[1] < tripwire_y and c[1] >= tripwire_y:
                        # Crossing event!
                        total_crossings += 1
                        alert_flash_timer = 20  # flash alert for 20 frames
                        print(f"[{time.strftime('%H:%M:%S')}] ALERT: Tripwire line crossed! Total: {total_crossings}")
                        break

            previous_centroids = {i: pt for i, pt in enumerate(current_centroids)}

            if not headless:
                # Draw tripwire line
                wire_color = (0, 0, 255) if (active_intruders > 0 or alert_flash_timer > 0) else (0, 255, 255)
                cv2.line(frame, (0, tripwire_y), (w, tripwire_y), wire_color, 3)
                cv2.putText(frame, "RESTRICTED PERIMETER LINE", (20, tripwire_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, wire_color, 2)

                # Top HUD
                status_color = (0, 0, 255) if (active_intruders > 0 or alert_flash_timer > 0) else (0, 255, 0)
                status_text = f"BREACH DETECTED! ({active_intruders} in zone)" if active_intruders > 0 else "PERIMETER SECURE"

                if alert_flash_timer > 0:
                    alert_flash_timer -= 1
                    status_text = "ALERT: TRIPWIRE CROSSING EVENT!"

                cv2.rectangle(frame, (10, 10), (550, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv10n Tripwire Guardian | FPS: {fps:.1f} (NMS-Free)",
                            (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, status_text, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)
                cv2.putText(frame, f"Total Line Crossings: {total_crossings} | Persons: {len(boxes)}",
                            (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv10n - Perimeter Tripwire Guardian", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Active: {active_intruders} | Crossings: {total_crossings} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print(f"Perimeter monitoring concluded. Total recorded crossings: {total_crossings}")


def main():
    parser = argparse.ArgumentParser(description="YOLOv10n Perimeter Tripwire Line Crossing Guardian")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for webcam, image path, or video path",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Detection confidence threshold (default: 0.35)",
    )
    parser.add_argument(
        "--line-ratio",
        type=float,
        default=0.55,
        help="Tripwire line vertical position ratio (0.0=top, 1.0=bottom, default: 0.55)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (headless server/docker)",
    )
    args = parser.parse_args()

    print("Loading YOLOv10n model (yolov10n.pt)...")
    model = YOLO("yolov10n.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.line_ratio, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.line_ratio, args.headless)


if __name__ == "__main__":
    main()
