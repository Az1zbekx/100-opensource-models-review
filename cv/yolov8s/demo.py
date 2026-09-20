import argparse
import math
import os
import time
import cv2
from ultralytics import YOLO

CLASS_PERSON = 0
CLASS_BACKPACK = 24
CLASS_HANDBAG = 26
CLASS_SUITCASE = 28

BAGGAGE_CLASSES = {
    CLASS_BACKPACK: "Backpack",
    CLASS_HANDBAG: "Handbag",
    CLASS_SUITCASE: "Suitcase",
}


def calculate_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def get_center(box):
    return (int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2))


def process_image(model, image_path: str, conf: float, headless: bool):
    """Analyze static retail image for shoppers carrying large baggage."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    results = model(frame, conf=conf, classes=[CLASS_PERSON] + list(BAGGAGE_CLASSES.keys()), verbose=False)
    boxes = results[0].boxes

    shoppers = []
    bags = []

    for box in boxes:
        cls_id = int(box.cls[0])
        coords = list(map(int, box.xyxy[0]))
        score = float(box.conf[0])
        center = get_center(coords)

        if cls_id == CLASS_PERSON:
            shoppers.append({"coords": coords, "center": center, "conf": score, "bag": None})
        elif cls_id in BAGGAGE_CLASSES:
            bags.append({"coords": coords, "center": center, "type": BAGGAGE_CLASSES[cls_id], "conf": score})

    # Associate bags with nearest shopper
    for bag in bags:
        closest_shopper = None
        min_dist = float("inf")
        for shopper in shoppers:
            dist = calculate_distance(bag["center"], shopper["center"])
            # Maximum association radius
            if dist < 220 and dist < min_dist:
                min_dist = dist
                closest_shopper = shopper

        if closest_shopper:
            closest_shopper["bag"] = bag

    flagged_shoppers = 0

    # Draw bags
    for bag in bags:
        bx1, by1, bx2, by2 = bag["coords"]
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), (255, 165, 0), 2)
        cv2.putText(frame, f"{bag['type']} ({bag['conf']:.2f})", (bx1, by1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 165, 0), 1)

    # Draw shoppers
    for shopper in shoppers:
        sx1, sy1, sx2, sy2 = shopper["coords"]
        if shopper["bag"] is not None:
            flagged_shoppers += 1
            color = (0, 0, 255)
            label = f"FLAGGED: Shopper + {shopper['bag']['type']}"
            # Draw linking line between shopper and bag
            cv2.line(frame, shopper["center"], shopper["bag"]["center"], (0, 0, 255), 2)
        else:
            color = (0, 255, 0)
            label = f"Shopper ({shopper['conf']:.2f})"

        cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), color, 2)
        cv2.putText(frame, label, (sx1, sy1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 2)

    # Status Banner
    if flagged_shoppers > 0:
        status_msg = f"LOSS PREVENTION: {flagged_shoppers} SHOPPER(S) CARRYING LARGE BAGGAGE"
        status_color = (0, 0, 255)
    else:
        status_msg = "STATUS: NO CONCEALMENT BAGGAGE DETECTED"
        status_color = (0, 255, 0)

    cv2.rectangle(frame, (10, 10), (620, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLOv8s Loss Prevention | Shoppers: {len(shoppers)} | Baggage: {len(bags)}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)
    cv2.putText(frame, status_msg, (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.52, status_color, 2)

    output_path = "output_shopper.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Baggage Audit: {status_msg}")

    if not headless:
        cv2.imshow("YOLOv8s - Retail Loss Prevention", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Real-time retail entrance and aisle baggage tracking."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Baggage Tracker initialized (source={video_source}, headless={headless}).")
    print("Press 'q' in video window to exit, or Ctrl+C in terminal.")

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

            results = model(frame, conf=conf, classes=[CLASS_PERSON] + list(BAGGAGE_CLASSES.keys()), verbose=False)
            boxes = results[0].boxes

            shoppers = []
            bags = []

            for box in boxes:
                cls_id = int(box.cls[0])
                coords = list(map(int, box.xyxy[0]))
                center = get_center(coords)

                if cls_id == CLASS_PERSON:
                    shoppers.append({"coords": coords, "center": center, "bag": None})
                elif cls_id in BAGGAGE_CLASSES:
                    bags.append({"coords": coords, "center": center, "type": BAGGAGE_CLASSES[cls_id]})

            for bag in bags:
                closest_shopper = None
                min_dist = float("inf")
                for shopper in shoppers:
                    dist = calculate_distance(bag["center"], shopper["center"])
                    if dist < 220 and dist < min_dist:
                        min_dist = dist
                        closest_shopper = shopper

                if closest_shopper:
                    closest_shopper["bag"] = bag

            flagged = 0

            if not headless:
                for bag in bags:
                    bx1, by1, bx2, by2 = bag["coords"]
                    cv2.rectangle(frame, (bx1, by1), (bx2, by2), (255, 165, 0), 2)
                    cv2.putText(frame, bag["type"], (bx1, by1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 165, 0), 1)

                for shopper in shoppers:
                    sx1, sy1, sx2, sy2 = shopper["coords"]
                    if shopper["bag"] is not None:
                        flagged += 1
                        color = (0, 0, 255)
                        lbl = f"FLAGGED: +{shopper['bag']['type']}"
                        cv2.line(frame, shopper["center"], shopper["bag"]["center"], (0, 0, 255), 2)
                    else:
                        color = (0, 255, 0)
                        lbl = "Shopper"

                    cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), color, 2)
                    cv2.putText(frame, lbl, (sx1, sy1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 1)

                # Dashboard HUD
                s_color = (0, 0, 255) if flagged > 0 else (0, 255, 0)
                s_text = f"ATTENTION: {flagged} SHOPPER(S) WITH BAGGAGE" if flagged > 0 else "STORE AISLES CLEAR"

                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv8s Loss Prevention | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, s_text, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.62, s_color, 2)
                cv2.putText(frame, f"Active Shoppers: {len(shoppers)} | Baggage Items: {len(bags)}", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv8s - Retail Loss Prevention", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Shoppers: {len(shoppers)} | Flagged: {flagged} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Retail loss prevention session ended.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv8s Retail Shopper & Loss Prevention Baggage Tracker")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for webcam, image path, or video file path",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.45,
        help="Detection confidence threshold (default: 0.45)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (for server execution)",
    )
    args = parser.parse_args()

    print("Loading YOLOv8s model (yolov8s.pt)...")
    model = YOLO("yolov8s.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
