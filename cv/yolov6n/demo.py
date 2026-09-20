import argparse
import os
import time
import urllib.request
import cv2
import torch

WEIGHTS_URL = "https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6n.pt"
WEIGHTS_FILE = "yolov6n.pt"

TARGET_CLASSES = {
    24: "Package/Box",
    39: "Bottle",
    41: "Cup",
    45: "Bowl",
    73: "Carton/Book",
}


def ensure_weights(target_path=WEIGHTS_FILE):
    if not os.path.exists(target_path):
        print(f"Downloading {WEIGHTS_FILE} from Meituan release...")
        urllib.request.urlretrieve(WEIGHTS_URL, target_path)
        print("Download complete.")
    return target_path


def load_yolov6n(weights_path):
    print(f"Loading YOLOv6n ({weights_path})...")
    hub_cache = os.path.expanduser("~/.cache/torch/hub/meituan_YOLOv6_main")
    coco_yaml = os.path.join(hub_cache, "data/coco.yaml")
    model = torch.hub.load("meituan/YOLOv6", "custom", weights_path, coco_yaml, trust_repo=True)
    return model


def process_image(model, image_path: str, conf: float, headless: bool):
    """Analyze static image for items on an industrial conveyor."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    conveyor_line_x = int(w * 0.50)

    pred = model.predict(image_path)
    boxes = pred["boxes"]
    scores = pred["scores"]
    labels = pred["labels"]

    counted_items = 0
    item_breakdown = {}

    for box, score, label in zip(boxes, scores, labels):
        if score < conf:
            continue
        x1, y1, x2, y2 = map(int, box)
        cls_id = int(label)
        cls_name = TARGET_CLASSES.get(cls_id, f"Item-{cls_id}")

        counted_items += 1
        item_breakdown[cls_name] = item_breakdown.get(cls_name, 0) + 1

        color = (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{cls_name} ({score:.2f})", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    # Draw Conveyor Demarcation Line
    cv2.line(frame, (conveyor_line_x, 0), (conveyor_line_x, h), (0, 255, 255), 2)
    cv2.putText(frame, "CONVEYOR SENSOR LINE", (conveyor_line_x + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Dashboard HUD
    status = f"THROUGHPUT: {counted_items} ACTIVE ITEMS DETECTED"
    cv2.rectangle(frame, (10, 10), (580, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLOv6n Industrial Conveyor Patrol | Meituan Architecture",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, status, (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 2)

    output_path = "output_conveyor.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Conveyor Item Audit: {status} | Details: {item_breakdown}")

    if not headless:
        cv2.imshow("YOLOv6n - Conveyor Object Counter", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Real-time conveyor belt inspection and item counting."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Conveyor Patrol initialized (source={video_source}, headless={headless}).")
    print("Press 'q' in video window to exit, or Ctrl+C in terminal.")

    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    total_passed = 0
    temp_frame_path = "/tmp/yolov6_temp.jpg"

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
            line_x = int(w * 0.50)

            # Predict using temporary frame
            cv2.imwrite(temp_frame_path, frame)
            pred = model.predict(temp_frame_path)

            boxes = pred["boxes"]
            scores = pred["scores"]
            labels = pred["labels"]

            items_in_frame = 0
            for box, score, label in zip(boxes, scores, labels):
                if score < conf:
                    continue
                x1, y1, x2, y2 = map(int, box)
                cls_id = int(label)
                items_in_frame += 1

                if not headless:
                    lbl = TARGET_CLASSES.get(cls_id, "Item")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{lbl} {score:.2f}", (x1, y1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

            if not headless:
                # Demarcation line
                cv2.line(frame, (line_x, 0), (line_x, h), (0, 255, 255), 2)
                cv2.putText(frame, "CONVEYOR GATE", (line_x + 8, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

                # HUD
                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv6n Conveyor Patrol | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, f"Active Items on Belt: {items_in_frame}",
                            (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 255, 0), 2)
                cv2.putText(frame, f"Throughput Status: OPTIMAL FLOW", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv6n - Conveyor Object Counter", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Active Items: {items_in_frame} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)
        if not headless:
            cv2.destroyAllWindows()
        print("Conveyor patrol session finished.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv6n Industrial Conveyor Belt Object Counter")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for webcam, image path, or video file path",
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
        help="Run without GUI (for server execution)",
    )
    args = parser.parse_args()

    weights = ensure_weights()
    model = load_yolov6n(weights)

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
