import argparse
import os
import time
import cv2
from ultralytics import YOLO

# Target COCO classes
CLASS_PERSON = 0
CLASS_LAPTOP = 63
CLASS_PHONE = 67
CLASS_BOOK = 73

DISTRACTION_CONFIRM_SECONDS = 3.0


def process_image(model, image_path: str, conf: float, headless: bool):
    """Process a single image and save/display the result."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    results = model(frame, conf=conf, verbose=False)
    boxes = results[0].boxes

    person_detected = False
    phone_detected = False

    for box in boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        score = float(box.conf[0])

        if cls_id == CLASS_PERSON:
            person_detected = True
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 200, 0), 2)
            cv2.putText(frame, f"Person {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 2)
        elif cls_id == CLASS_PHONE:
            phone_detected = True
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, f"PHONE DETECTED! {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif cls_id in (CLASS_LAPTOP, CLASS_BOOK):
            label = "Laptop" if cls_id == CLASS_LAPTOP else "Book"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if phone_detected:
        status_text = "STATUS: DISTRACTED (Smartphone in use)"
        status_color = (0, 0, 255)
    elif person_detected:
        status_text = "STATUS: FOCUSED (Productive work)"
        status_color = (0, 255, 0)
    else:
        status_text = "STATUS: EMPTY DESK (No person detected)"
        status_color = (200, 200, 200)

    # Draw Status Banner
    cv2.rectangle(frame, (10, 10), (520, 65), (0, 0, 0), -1)
    cv2.putText(frame, status_text, (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)

    output_path = "output_desk.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result successfully saved to '{output_path}'")
    print(f"Assessment: {status_text}")

    if not headless:
        cv2.imshow("YOLO11n - Smart Desk Focus Monitor", frame)
        print("Press any key to close the preview window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Process real-time video stream from webcam or video file."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source '{video_source}'.")
        return

    print(f"Stream initialized (source={video_source}, headless={headless}).")
    print("Controls: Press 'q' in the window to quit, or Ctrl+C in terminal.")

    distraction_start = None
    total_distraction_time = 0.0
    fps_start_time = time.time()
    frame_count = 0
    fps = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            now = time.time()
            if now - fps_start_time >= 1.0:
                fps = frame_count / (now - fps_start_time)
                frame_count = 0
                fps_start_time = now

            results = model(frame, conf=conf, verbose=False)
            boxes = results[0].boxes

            person_found = False
            phone_found = False

            for box in boxes:
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                score = float(box.conf[0])

                if cls_id == CLASS_PERSON:
                    person_found = True
                    if not headless:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 200, 0), 2)
                elif cls_id == CLASS_PHONE:
                    phone_found = True
                    if not headless:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.putText(frame, f"PHONE {score:.2f}", (x1, y1 - 8),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                elif cls_id in (CLASS_LAPTOP, CLASS_BOOK):
                    if not headless:
                        label = "Laptop" if cls_id == CLASS_LAPTOP else "Book"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

            # Focus & Distraction logic
            if person_found and phone_found:
                if distraction_start is None:
                    distraction_start = now
                current_distracted_duration = now - distraction_start
                if current_distracted_duration >= DISTRACTION_CONFIRM_SECONDS:
                    status_text = f"DISTRACTED! ({current_distracted_duration:.1f}s)"
                    status_color = (0, 0, 255)
                else:
                    status_text = "PHONE IN VIEW..."
                    status_color = (0, 165, 255)
            else:
                if distraction_start is not None:
                    total_distraction_time += (now - distraction_start)
                    distraction_start = None

                if person_found:
                    status_text = "FOCUSED & PRODUCTIVE"
                    status_color = (0, 255, 0)
                else:
                    status_text = "DESK EMPTY"
                    status_color = (180, 180, 180)

            # Render UI
            if not headless:
                # Top dashboard
                cv2.rectangle(frame, (10, 10), (480, 90), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLO11n Focus Monitor | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, status_text, (20, 62),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, status_color, 2)
                cv2.putText(frame, f"Total Distracted Time: {total_distraction_time:.1f}s", (20, 82),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

                cv2.imshow("YOLO11n - Smart Desk Focus Monitor", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] {status_text} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("\nSession finished.")
        print(f"Total recorded distraction time: {total_distraction_time:.1f} seconds.")


def main():
    parser = argparse.ArgumentParser(description="YOLO11n Smart Desk Focus & Distraction Monitor")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for laptop webcam, path to image (.jpg, .png), or path to video (.mp4)",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.35,
        help="Detection confidence threshold (default: 0.35)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window (for server or background runs)",
    )
    args = parser.parse_args()

    print("Loading YOLO11n model (yolo11n.pt)...")
    model = YOLO("yolo11n.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
