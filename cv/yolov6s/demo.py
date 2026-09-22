import argparse
import os
import time
import urllib.request
import cv2
import torch
import yaml

WEIGHTS_URL = "https://github.com/meituan/YOLOv6/releases/download/0.4.0/yolov6s.pt"
WEIGHTS_FILE = "yolov6s.pt"

VEHICLE_CLASSES = {
    "truck": "Freight Truck",
    "bus": "Transit Bus",
    "car": "Service Fleet",
    "motorcycle": "Yard Vehicle",
    "person": "Dock Operator",
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
    with open(coco_yaml, "r") as f:
        class_names = yaml.safe_load(f)["names"]
    model = torch.hub.load("meituan/YOLOv6", "custom", weights_path, class_names, trust_repo=True)
    return model


def is_point_in_box(point, box):
    px, py = point
    bx1, by1, bx2, by2 = box
    return bx1 <= px <= bx2 and by1 <= py <= by2


def box_overlap_ratio(box_a, box_b):
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    iw = max(0, ix2 - ix1)
    ih = max(0, iy2 - iy1)
    inter = iw * ih
    area_a = max(1, (ax2 - ax1) * (ay2 - ay1))
    return inter / area_a


def process_image(model, image_path: str, conf: float, output_path: str = None, headless: bool = False):
    """Analyze static logistics terminal image for freight vehicle bay occupancy."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    # Define two industrial docking bays (Left Bay 1 and Right Bay 2)
    bay_1 = (int(w * 0.02), int(h * 0.16), int(w * 0.48), int(h * 0.94))
    bay_2 = (int(w * 0.50), int(h * 0.16), int(w * 0.98), int(h * 0.94))

    t_start = time.time()
    pred = model.predict(image_path)
    infer_ms = (time.time() - t_start) * 1000

    boxes = pred["boxes"]
    scores = pred["scores"]
    classes = pred["classes"]

    bay1_occupants = []
    bay2_occupants = []
    vehicle_count = 0
    operator_count = 0
    asset_breakdown = {}

    for box, score, raw_cls in zip(boxes, scores, classes):
        score_val = float(score)
        if score_val < conf:
            continue
        if raw_cls not in VEHICLE_CLASSES:
            continue

        x1, y1, x2, y2 = map(int, box)
        center_pt = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        v_type = VEHICLE_CLASSES[raw_cls]
        asset_breakdown[v_type] = asset_breakdown.get(v_type, 0) + 1

        is_person = (raw_cls == "person")
        if is_person:
            operator_count += 1
            color = (255, 190, 0)  # Cyan/Orange for dock staff
            loc_str = "Yard Staff"
        else:
            vehicle_count += 1
            color = (0, 255, 120)  # Green for vehicles
            
            # Check docking bay occupancy
            in_b1 = is_point_in_box(center_pt, bay_1) or box_overlap_ratio((x1, y1, x2, y2), bay_1) > 0.25
            in_b2 = is_point_in_box(center_pt, bay_2) or box_overlap_ratio((x1, y1, x2, y2), bay_2) > 0.25

            if in_b1:
                bay1_occupants.append(v_type)
                loc_str = "Docked: Bay 1"
                color = (0, 165, 255)
            elif in_b2:
                bay2_occupants.append(v_type)
                loc_str = "Docked: Bay 2"
                color = (0, 165, 255)
            else:
                loc_str = "Terminal Staging"
                color = (0, 255, 120)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Tag label
        label_text = f"{v_type} ({score_val:.2f}) - {loc_str}"
        tag_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        tag_w, tag_h = tag_size
        tag_y1 = max(0, y1 - tag_h - 4)
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tag_w + 4, y1), (15, 18, 22), -1)
        cv2.putText(frame, label_text, (x1 + 2, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 1, cv2.LINE_AA)

    # Render Docking Bays
    bay1_occ = len(bay1_occupants) > 0
    bay2_occ = len(bay2_occupants) > 0

    for b_box, b_name, b_occ, occ_list in [
        (bay_1, "DOCKING BAY 1", bay1_occ, bay1_occupants),
        (bay_2, "DOCKING BAY 2", bay2_occ, bay2_occupants)
    ]:
        bx1, by1, bx2, by2 = b_box
        b_col = (0, 70, 255) if b_occ else (0, 230, 100)
        status_text = f"{b_name}: {'OCCUPIED (' + occ_list[0] + ')' if b_occ else 'AVAILABLE / IDLE'}"
        
        # Draw bay perimeter
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), b_col, 2)
        
        # Draw bay badge
        badge_w, badge_h = 240, 26
        cv2.rectangle(frame, (bx1, by1), (bx1 + badge_w, by1 + badge_h), (15, 18, 22), -1)
        cv2.rectangle(frame, (bx1, by1), (bx1 + badge_w, by1 + badge_h), b_col, 1)
        cv2.putText(frame, status_text, (bx1 + 6, by1 + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, b_col, 1, cv2.LINE_AA)

    # Telemetry HUD Header
    hud_w = min(680, w - 190)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 75), (15, 18, 22), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 75), (0, 180, 255), 1)

    bay_summary = f"Bay 1: {'OCCUPIED' if bay1_occ else 'FREE'} | Bay 2: {'OCCUPIED' if bay2_occ else 'FREE'}"
    turnaround = "TURNAROUND: DISPATCH OPTIMAL" if (bay1_occ or bay2_occ) else "TURNAROUND: ALL BAYS AVAILABLE"

    cv2.putText(frame, f"YOLOv6s Freight Terminal Patrol | Meituan Architecture",
                (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"DOCK STATUS: {bay_summary} | {turnaround}",
                (20, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 230, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"YARD ASSETS: {vehicle_count} Commercial Vehicles, {operator_count} Dock Personnel Detected",
                (20, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (180, 210, 220), 1, cv2.LINE_AA)

    # Top-Right Performance Badge
    badge_w = 180
    if w >= 800:
        cv2.rectangle(frame, (w - badge_w - 10, 10), (w - 10, 65), (15, 18, 22), -1)
        cv2.rectangle(frame, (w - badge_w - 10, 10), (w - 10, 65), (70, 75, 80), 1)
        device_name = "cuda:0" if torch.cuda.is_available() else "cpu"
        cv2.putText(frame, "Inference: YOLOv6s", (w - badge_w, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Device: {device_name} | {infer_ms:.1f}ms", (w - badge_w, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 230, 255), 1, cv2.LINE_AA)

    if output_path is None:
        output_path = "output_freight.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Terminal Audit: {vehicle_count} vehicles, {operator_count} dock staff. Bay 1: {bay1_occ}, Bay 2: {bay2_occ}. Breakdown: {asset_breakdown}")

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
            classes = pred["classes"]

            b1_occ = False
            b2_occ = False
            vehicles_found = 0

            for box, score, raw_cls in zip(boxes, scores, classes):
                score_val = float(score)
                if score_val < conf:
                    continue
                if raw_cls not in VEHICLE_CLASSES:
                    continue

                x1, y1, x2, y2 = map(int, box)
                center_pt = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                v_name = VEHICLE_CLASSES[raw_cls]
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
        default=0.30,
        help="Detection confidence threshold (default: 0.30)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save annotated output image",
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
        process_image(model, args.source, args.conf, args.output, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
