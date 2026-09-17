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
        print(f"Video manbasini ochib bo'lmadi: {video_source}")
        return

    state = "PRESENT"
    absence_start_time = None
    pending_present = True
    pending_count = 0

    print(f"Boshlandi (headless={headless}). {'Chiqish uchun q bos.' if not headless else 'To\'xtatish uchun Ctrl+C.'}")

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
                        print(f"[{time.strftime('%H:%M:%S')}] Odam qaytdi.")
                    state = "PRESENT"
                    absence_start_time = None
                else:
                    if state == "PRESENT":
                        state = "ABSENT"
                        absence_start_time = now
                        print(f"[{time.strftime('%H:%M:%S')}] Odam ketdi.")

            if state == "ABSENT" and absence_start_time:
                elapsed = now - absence_start_time
                if elapsed >= ABSENCE_THRESHOLD and state != "ALERTED":
                    state = "ALERTED"
                    print(f"[{time.strftime('%H:%M:%S')}] ALERT! {elapsed:.0f} soniya yo'q.")

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
        help="GUI oynasisiz ishga tushirish (Docker uchun standart)",
    )
    args = parser.parse_args()
    main(headless=args.headless)
