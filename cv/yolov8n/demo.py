import argparse
import os
import time

import cv2
from ultralytics import YOLO

ABSENCE_THRESHOLD = 15   
CONFIRM_FRAMES = 30      


def main(headless: bool):
    model = YOLO("yolov8n.pt")

    video_source = os.environ.get("VIDEO_SOURCE", 0)
    try:
        video_source = int(video_source)
    except ValueError:
        pass 

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Failed to open video source: {video_source}")
        return

    state = "PRESENT"
    absence_start_time = None
    pending_present = True
    pending_count = 0

    print(f"Started (headless={headless}). {'Press q to exit.' if not headless else 'Press Ctrl+C to stop.'}")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame, classes=[0], conf=0.5, verbose=False)
            boxes = results[0].boxes
            raw_present = len(boxes) > 0
            now = time.time()

            if not headless:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            if raw_present == pending_present:
                pending_count += 1
            else:
                pending_present = raw_present
                pending_count = 1

            if pending_count == CONFIRM_FRAMES:
                if pending_present:
                    if state != "PRESENT":
                        print(f"[{time.strftime('%H:%M:%S')}] Person returned.")
                    state = "PRESENT"
                    absence_start_time = None
                else:
                    if state == "PRESENT":
                        state = "ABSENT"
                        absence_start_time = now
                        print(f"[{time.strftime('%H:%M:%S')}] Person left.")

            if state == "ABSENT" and absence_start_time:
                elapsed = now - absence_start_time
                if elapsed >= ABSENCE_THRESHOLD and state != "ALERTED":
                    state = "ALERTED"
                    print(f"[{time.strftime('%H:%M:%S')}] ALERT! Absent for {elapsed:.0f} seconds.")

            if not headless:
                cv2.imshow("Presence test", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window (standard for Docker)",
    )
    args = parser.parse_args()
    main(headless=args.headless)