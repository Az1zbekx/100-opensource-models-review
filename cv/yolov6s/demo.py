import argparse
import os
import time
import urllib.request
import cv2
import torch

WEIGHTS_URL = "https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6s.pt"
WEIGHTS_FILE = "yolov6s.pt"

VEHICLE_CLASSES = {
    2: "Service Car",
    5: "Transit Bus",
    7: "Freight Truck",
}


def ensure_weights(target_path=WEIGHTS_FILE):
    if not os.path.exists(target_path):
        print(f"Downloading {WEIGHTS_FILE} from Meituan release...")
        urllib.request.urlretrieve(WEIGHTS_URL, target_path)
        print("Download complete.")
    return target_path


def load_yolov6s(weights_path):
    print(f"Loading YOLOv6s ({weights_path})...")
    hub_cache = os.path.expanduser("~/.cache/torch/hub/meituan_YOLOv6_main")
    coco_yaml = os.path.join(hub_cache, "data/coco.yaml")
    model = torch.hub.load("meituan/YOLOv6", "custom", weights_path, coco_yaml, trust_repo=True)
    return model


def is_point_in_box(point, box):
    px, py = point
    bx1, by1, bx2, by2 = box
    return bx1 <= px <= bx2 and by1 <= py <= by2


def process_image(model, image_path: str, conf: float, headless: bool):
    """Analyze static logistics terminal image for freight vehicle bay occupancy."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    # Define two freight docking bays (Left Bay 1 and Right Bay 2)
    bay_1 = (int(w * 0.05), int(h * 0.25), int(w * 0.48), int(h * 0.90))
    bay_2 = (int(w * 0.52), int(h * 0.25), int(w * 0.95), int(h * 0.90))

    pred = model.predict(image_path)
    boxes = pred["boxes"]
    scores = pred["scores"]
    labels = pred["labels"]

    bay1_occupied = False
    bay2_occupied = False
    vehicle_count = 0

    for box, score, label in zip(boxes, scores, labels):
        if score < conf:
            continue
        cls_id = int(label)
        if cls_id not in VEHICLE_CLASSES:
            continue

        x1, y1, x2, y2 = map(int, box)
        center_pt = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        v_type = VEHICLE_CLASSES[cls_id]
        vehicle_count += 1

        in_b1 = is_point_in_box(center_pt, bay_1)
        in_b2 = is_point_in_box(center_pt, bay_2)

        if in_b1:
            bay1_occupied = True
            loc_str = "Docked: Bay 1"
            color = (0, 165, 255)
        elif in_b2:
            bay2_occupied = True
            loc_str = "Docked: Bay 2"
            color = (0, 165, 255)
        else:
            loc_str = "Terminal Yard"
            color = (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{v_type} ({score:.2f}) - {loc_str}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    # Draw Docking Bays
    for b_box, b_name, b_occ in [(bay_1, "DOCKING BAY 1", bay1_occupied), (bay_2, "DOCKING BAY 2", bay2_occupied)]:
        bx1, by1, bx2, by2 = b_box
        b_col = (0, 0, 255) if b_occ else (0, 255, 0)
        status = "OCCUPIED" if b_occ else "AVAILABLE"
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), b_col, 2)
        cv2.putText(frame, f"{b_name}: {status}", (bx1 + 10, by1 + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, b_col, 2)

    # Dashboard HUD
    cv2.rectangle(frame, (10, 10), (620, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLOv6s Freight Terminal Patrol | Vehicles: {vehicle_count}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    b_status = f"Bay 1: {'OCCUPIED' if bay1_occupied else 'FREE'} | Bay 2: {'OCCUPIED' if bay2_occupied else 'FREE'}"
    cv2.putText(frame, b_status, (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 2)

    output_path = "output_freight.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Terminal Status: {b_status}")

    if not headless:
        cv2.imshow("YOLOv6s - Freight Terminal Monitor", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Real-time logistics terminal freight bay tracking."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Freight Bay Monitor initialized (source={video_source}, headless={headless}).")
    print("Press 'q' in video window to exit, or Ctrl+C in terminal.")

    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    temp_frame_path = "/tmp/yolov6s_temp.jpg"

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
            bay_1 = (int(w * 0.05), int(h * 0.25), int(w * 0.48), int(h * 0.90))
            bay_2 = (int(w * 0.52), int(h * 0.25), int(w * 0.95), int(h * 0.90))

            cv2.imwrite(temp_frame_path, frame)
            pred = model.predict(temp_frame_path)

            boxes = pred["boxes"]
            scores = pred["scores"]
            labels = pred["labels"]

            b1_occ = False
            b2_occ = False
            vehicles_found = 0

            for box, score, label in zip(boxes, scores, labels):
                if score < conf:
                    continue
                cls_id = int(label)
                if cls_id not in VEHICLE_CLASSES:
                    continue

                x1, y1, x2, y2 = map(int, box)
                center_pt = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                v_name = VEHICLE_CLASSES[cls_id]
                vehicles_found += 1

                if is_point_in_box(center_pt, bay_1):
                    b1_occ = True
                if is_point_in_box(center_pt, bay_2):
                    b2_occ = True

                if not headless:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 120, 0), 2)
                    cv2.putText(frame, v_name, (x1, y1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 120, 0), 1)

            if not headless:
                # Render Bays
                for b_box, b_name, b_occ in [(bay_1, "BAY 1", b1_occ), (bay_2, "BAY 2", b2_occ)]:
                    bx1, by1, bx2, by2 = b_box
                    col = (0, 0, 255) if b_occ else (0, 255, 0)
                    txt = "OCCUPIED" if b_occ else "FREE"
                    cv2.rectangle(frame, (bx1, by1), (bx2, by2), col, 2)
                    cv2.putText(frame, f"{b_name}: {txt}", (bx1 + 10, by1 + 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, col, 2)

                # Dashboard HUD
                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv6s Freight Terminal | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, f"Bay 1: {'OCCUPIED' if b1_occ else 'FREE'} | Bay 2: {'OCCUPIED' if b2_occ else 'FREE'}",
                            (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 255, 0), 2)
                cv2.putText(frame, f"Total Yard Vehicles: {vehicles_found}", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv6s - Freight Terminal Monitor", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Vehicles: {vehicles_found} | Bay1: {b1_occ} | Bay2: {b2_occ} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)
        if not headless:
            cv2.destroyAllWindows()
        print("Freight bay monitoring session completed.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv6s Fleet Logistics Terminal Truck & Bus Bay Monitor")
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

    weights = ensure_weights()
    model = load_yolov6s(weights)

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
