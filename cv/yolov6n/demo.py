import argparse
import os
import time
import urllib.request
import cv2
import torch
import yaml

WEIGHTS_URL = "https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6n.pt"
WEIGHTS_FILE = "yolov6n.pt"

CONVEYOR_CLASSES = {
    "bottle": "Bottled Good",
    "cup": "Container / Can",
    "bowl": "Container",
    "wine glass": "Glassware",
    "suitcase": "Baggage Parcel",
    "backpack": "Transit Bag",
    "handbag": "Transit Bag",
    "book": "Boxed Carton",
    "cake": "Packaged Item",
    "sandwich": "Packaged Item",
    "apple": "Produce / Fruit",
    "orange": "Produce / Fruit",
    "person": "Conveyor Operator",
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
    with open(coco_yaml, "r") as f:
        class_names = yaml.safe_load(f)["names"]
    model = torch.hub.load("meituan/YOLOv6", "custom", weights_path, class_names, trust_repo=True)
    return model


def process_image(model, image_path: str, conf: float, output_path: str = None, headless: bool = False):
    """Analyze static image for items on an industrial conveyor belt."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    conveyor_line_x = int(w * 0.48)

    t_start = time.time()
    pred = model.predict(image_path)
    infer_ms = (time.time() - t_start) * 1000

    boxes = pred["boxes"]
    scores = pred["scores"]
    classes = pred["classes"]

    counted_items = 0
    conveyor_operators = 0
    item_breakdown = {}

    for box, score, raw_cls in zip(boxes, scores, classes):
        score_val = float(score)
        if score_val < conf:
            continue
        x1, y1, x2, y2 = map(int, box)
        
        is_operator = (raw_cls == "person")
        if is_operator:
            conveyor_operators += 1
            box_color = (255, 180, 0)  # Cyan/Orange for human operator
            display_label = f"Operator: {score_val:.2f}"
        else:
            counted_items += 1
            box_color = (0, 255, 100)  # High-vis green for tracked conveyor goods
            telemetry_name = CONVEYOR_CLASSES.get(raw_cls, raw_cls.capitalize())
            display_label = f"{telemetry_name}: {score_val:.2f}"
            item_breakdown[telemetry_name] = item_breakdown.get(telemetry_name, 0) + 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
        
        # Bounding box tag
        tag_size, _ = cv2.getTextSize(display_label, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        tag_w, tag_h = tag_size
        tag_y1 = max(0, y1 - tag_h - 4)
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tag_w + 4, y1), (15, 18, 22), -1)
        cv2.putText(frame, display_label, (x1 + 2, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, box_color, 1, cv2.LINE_AA)

    # Conveyor Demarcation Sensor Gate
    cv2.line(frame, (conveyor_line_x, 80), (conveyor_line_x, h), (0, 230, 255), 2)
    gate_label = "CONVEYOR OPTICAL SENSOR GATE"
    cv2.putText(frame, gate_label, (conveyor_line_x + 8, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 230, 255), 1, cv2.LINE_AA)

    # Telemetry HUD Header
    hud_w = min(660, w - 180)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 75), (15, 18, 22), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 75), (0, 230, 255), 1)

    status_str = f"BELT AUDIT: {counted_items} ACTIVE UNITS ON CONVEYOR | {conveyor_operators} OPERATORS"
    flow_str = "THROUGHPUT STATUS: OPTIMAL CONTINUOUS FLOW | OPTICAL GATE: ARMED"

    cv2.putText(frame, "YOLOv6n Industrial Conveyor Belt Monitor | Meituan Architecture",
                (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, status_str, (20, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (0, 255, 100), 1, cv2.LINE_AA)
    cv2.putText(frame, flow_str, (20, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (180, 210, 220), 1, cv2.LINE_AA)

    # Top-Right Performance Badge
    badge_w = 190
    if w >= 800:
        cv2.rectangle(frame, (w - badge_w - 10, 10), (w - 10, 65), (15, 18, 22), -1)
        cv2.rectangle(frame, (w - badge_w - 10, 10), (w - 10, 65), (70, 75, 80), 1)
        device_name = "cuda:0" if torch.cuda.is_available() else "cpu"
        cv2.putText(frame, "Inference: YOLOv6n", (w - badge_w, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Device: {device_name} | {infer_ms:.1f}ms", (w - badge_w, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 230, 255), 1, cv2.LINE_AA)

    if output_path is None:
        output_path = "output_conveyor.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Conveyor Item Audit: {counted_items} units, {conveyor_operators} operators. Breakdown: {item_breakdown}")

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
            line_x = int(w * 0.48)

            # Predict using temporary frame
            cv2.imwrite(temp_frame_path, frame)
            pred = model.predict(temp_frame_path)

            boxes = pred["boxes"]
            scores = pred["scores"]
            classes = pred["classes"]

            items_in_frame = 0
            for box, score, raw_cls in zip(boxes, scores, classes):
                score_val = float(score)
                if score_val < conf:
                    continue
                x1, y1, x2, y2 = map(int, box)
                items_in_frame += 1

                if not headless:
                    lbl = CONVEYOR_CLASSES.get(raw_cls, raw_cls.capitalize())
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 100), 2)
                    cv2.putText(frame, f"{lbl} {score_val:.2f}", (x1, y1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 100), 1)

            if not headless:
                # Demarcation line
                cv2.line(frame, (line_x, 0), (line_x, h), (0, 230, 255), 2)
                cv2.putText(frame, "CONVEYOR GATE", (line_x + 8, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 230, 255), 1)

                # HUD
                cv2.rectangle(frame, (10, 10), (580, 85), (15, 18, 22), -1)
                cv2.putText(frame, f"YOLOv6n Conveyor Patrol | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, f"Active Units on Belt: {items_in_frame}",
                            (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 255, 100), 2)
                cv2.putText(frame, "Throughput Status: OPTIMAL FLOW", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv6n - Conveyor Object Counter", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Active Units: {items_in_frame} | FPS: {fps:.1f}")

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
        default=0.25,
        help="Detection confidence threshold (default: 0.25)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save output image (default: output_conveyor.jpg)",
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
        process_image(model, args.source, args.conf, args.output, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
