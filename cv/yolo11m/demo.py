import argparse
import math
import os
import time
import cv2
from ultralytics import YOLO

# COCO Class IDs
CLASS_PERSON = 0
CLASS_CAR = 2
CLASS_BUS = 5
CLASS_TRUCK = 7

VEHICLE_CLASSES = {CLASS_CAR: "Car", CLASS_BUS: "Bus", CLASS_TRUCK: "Truck/Machinery"}


def calculate_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def get_center(box):
    x1, y1, x2, y2 = box
    return (int((x1 + x2) / 2), int((y1 + y2) / 2))


def calculate_edge_distance_and_closest_point(pt, box):
    """Calculates Euclidean distance and closest point from pt to bounding box edges."""
    px, py = pt
    bx1, by1, bx2, by2 = box

    # Clamp point coordinates to box to find closest boundary point
    cx = max(bx1, min(px, bx2))
    cy = max(by1, min(py, by2))
    dist = math.hypot(px - cx, py - cy)
    return dist, (cx, cy)


def process_image(model, image_path: str, conf: float, proximity_thresh: int, headless: bool, output_path: str = None):
    """Analyze static image for safety zone breaches and machinery proximity hazards."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not open image {image_path}")
        return

    h, w = frame.shape[:2]

    results = model(frame, conf=conf, classes=[CLASS_PERSON, CLASS_CAR, CLASS_BUS, CLASS_TRUCK], verbose=False)
    boxes = results[0].boxes

    workers = []
    vehicles = []

    for box in boxes:
        cls_id = int(box.cls[0])
        coords = list(map(int, box.xyxy[0]))
        score = float(box.conf[0])

        if cls_id == CLASS_PERSON:
            workers.append({"coords": coords, "center": get_center(coords), "conf": score})
        elif cls_id in VEHICLE_CLASSES:
            vehicles.append({"coords": coords, "center": get_center(coords), "type": VEHICLE_CLASSES[cls_id], "conf": score})

    # Render machinery and their safety exclusion perimeter envelopes
    for v in vehicles:
        vx1, vy1, vx2, vy2 = v["coords"]
        v_type = v["type"]
        score = v["conf"]

        # Draw machinery safety clearance boundary
        buf_x1 = max(0, vx1 - proximity_thresh)
        buf_y1 = max(0, vy1 - proximity_thresh)
        buf_x2 = min(w - 1, vx2 + proximity_thresh)
        buf_y2 = min(h - 1, vy2 + proximity_thresh)
        cv2.rectangle(frame, (buf_x1, buf_y1), (buf_x2, buf_y2), (0, 165, 255), 1)

        # Draw vehicle box
        cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (0, 140, 255), 2)
        v_label = f"{v_type} ({score:.2f})"
        (tw, th), _ = cv2.getTextSize(v_label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        tag_y = max(0, vy1 - th - 6)
        cv2.rectangle(frame, (vx1, tag_y), (vx1 + tw + 6, tag_y + th + 6), (15, 18, 22), -1)
        cv2.rectangle(frame, (vx1, tag_y), (vx1 + tw + 6, tag_y + th + 6), (0, 140, 255), 1)
        cv2.putText(frame, v_label, (vx1 + 3, tag_y + th + 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    breach_count = 0
    proximity_warnings = []

    # Check workers against all active machinery
    for w_obj in workers:
        wx1, wy1, wx2, wy2 = w_obj["coords"]
        w_center = w_obj["center"]

        min_dist = float("inf")
        closest_vehicle_pt = None

        for v in vehicles:
            dist, closest_pt = calculate_edge_distance_and_closest_point(w_center, v["coords"])
            if dist < min_dist:
                min_dist = dist
                closest_vehicle_pt = closest_pt

        is_breach = min_dist < proximity_thresh and len(vehicles) > 0

        if is_breach:
            breach_count += 1
            box_color = (0, 0, 255)
            label = f"HAZARD BREACH! ({w_obj['conf']:.2f})"
            if closest_vehicle_pt is not None:
                proximity_warnings.append((w_center, closest_vehicle_pt, min_dist))
        else:
            box_color = (0, 255, 0)
            label = f"Worker Safe ({w_obj['conf']:.2f})"

        cv2.rectangle(frame, (wx1, wy1), (wx2, wy2), box_color, 2)
        cv2.circle(frame, w_center, 4, box_color, -1)

        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        tag_y = max(0, wy1 - th - 6)
        cv2.rectangle(frame, (wx1, tag_y), (wx1 + tw + 6, tag_y + th + 6), (15, 18, 22), -1)
        cv2.rectangle(frame, (wx1, tag_y), (wx1 + tw + 6, tag_y + th + 6), box_color, 1)
        cv2.putText(frame, label, (wx1 + 3, tag_y + th + 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    # Draw proximity clearance warning vectors
    for p1, p2, dist in proximity_warnings:
        cv2.line(frame, p1, p2, (0, 0, 255), 2)
        mid_point = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
        cv2.circle(frame, mid_point, 3, (0, 255, 255), -1)
        d_lbl = f"CLEARANCE: {dist:.0f}px"
        (tw, th), _ = cv2.getTextSize(d_lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.40, 1)
        cv2.rectangle(frame, (mid_point[0] - 2, mid_point[1] - th - 4),
                      (mid_point[0] + tw + 4, mid_point[1] + 4), (15, 18, 22), -1)
        cv2.putText(frame, d_lbl, (mid_point[0], mid_point[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 0, 255), 1, cv2.LINE_AA)

    # Top Dashboard HUD Banner
    if breach_count > 0:
        status_text = f"CRITICAL: {breach_count} WORKER-MACHINERY PROXIMITY HAZARDS DETECTED!"
        status_color = (0, 0, 255)
    else:
        status_text = "SAFETY PROTOCOLS NOMINAL: ALL PERSONNEL CLEAR OF MACHINERY"
        status_color = (0, 255, 0)

    hud_w = 700
    hud_h = 82
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 10 + hud_h), (15, 18, 22), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 10 + hud_h), (60, 64, 72), 1)

    cv2.putText(frame, "YOLO11m INDUSTRIAL SAFETY & MACHINERY GUARDIAN",
                (22, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 220, 255), 1, cv2.LINE_AA)
    
    cv2.putText(frame, f"Workers: {len(workers)}  |  Machinery: {len(vehicles)}  |  Safety Buffer: {proximity_thresh}px  |  Breaches: {breach_count}",
                (22, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 205, 215), 1, cv2.LINE_AA)
    
    cv2.putText(frame, status_text,
                (22, 76), cv2.FONT_HERSHEY_SIMPLEX, 0.46, status_color, 1, cv2.LINE_AA)

    out_file = output_path if output_path else "output_safety.jpg"
    cv2.imwrite(out_file, frame)
    print(f"Result saved to {out_file}")
    print(f"Safety Assessment: {status_text} (Workers: {len(workers)}, Machinery: {len(vehicles)}, Breaches: {breach_count})")

    if not headless:
        cv2.imshow("YOLO11m - Industrial Safety Guardian", frame)
        print("Press any key to close preview...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, proximity_thresh: int, headless: bool):
    """Real-time video feed safety inspection."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Safety Guardian initialized (source={video_source}, proximity={proximity_thresh}px).")
    print("Press 'q' in GUI window to quit, or Ctrl+C in terminal.")

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
            hazard_zone = (int(w * 0.30), int(h * 0.20), int(w * 0.90), int(h * 0.90))

            results = model(frame, conf=conf, classes=[CLASS_PERSON, CLASS_CAR, CLASS_BUS, CLASS_TRUCK], verbose=False)
            boxes = results[0].boxes

            workers = []
            vehicles = []

            for box in boxes:
                cls_id = int(box.cls[0])
                coords = list(map(int, box.xyxy[0]))
                score = float(box.conf[0])

                if cls_id == CLASS_PERSON:
                    workers.append({"coords": coords, "center": get_center(coords), "conf": score})
                elif cls_id in VEHICLE_CLASSES:
                    vehicles.append({"coords": coords, "center": get_center(coords), "type": VEHICLE_CLASSES[cls_id], "conf": score})

            hz_x1, hz_y1, hz_x2, hz_y2 = hazard_zone
            breaches = 0
            proximity_lines = []

            for v in vehicles:
                vx1, vy1, vx2, vy2 = v["coords"]
                if not headless:
                    cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (255, 100, 0), 2)
                    cv2.putText(frame, v["type"], (vx1, vy1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 100, 0), 1)

            for w_obj in workers:
                wx1, wy1, wx2, wy2 = w_obj["coords"]
                w_center = w_obj["center"]

                in_hazard_zone = (hz_x1 <= w_center[0] <= hz_x2 and hz_y1 <= w_center[1] <= hz_y2)
                near_vehicle = False

                for v in vehicles:
                    dist = calculate_distance(w_center, v["center"])
                    if dist < proximity_thresh:
                        near_vehicle = True
                        proximity_lines.append((w_center, v["center"], dist))

                if in_hazard_zone or near_vehicle:
                    breaches += 1
                    color = (0, 0, 255)
                    label = "ALERT: HAZARD!"
                else:
                    color = (0, 255, 0)
                    label = "Safe"

                if not headless:
                    cv2.rectangle(frame, (wx1, wy1), (wx2, wy2), color, 2)
                    cv2.putText(frame, label, (wx1, wy1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            if not headless:
                # Draw hazard boundary
                cv2.rectangle(frame, (hz_x1, hz_y1), (hz_x2, hz_y2), (0, 165, 255), 2)
                cv2.putText(frame, "RESTRICTED MACHINERY ZONE", (hz_x1 + 10, hz_y1 + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)

                # Draw proximity alert lines
                for p1, p2, dist in proximity_lines:
                    cv2.line(frame, p1, p2, (0, 0, 255), 2)

                # Dashboard HUD
                status_color = (0, 0, 255) if breaches > 0 else (0, 255, 0)
                status_msg = f"CRITICAL: {breaches} HAZARD BREACH(ES)!" if breaches > 0 else "STATUS: ALL ZONES SECURE"

                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLO11m Safety Guardian | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, status_msg, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)
                cv2.putText(frame, f"Workers: {len(workers)} | Machinery: {len(vehicles)}", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLO11m - Industrial Safety Guardian", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    status_msg = f"CRITICAL: {breaches} BREACHES" if breaches > 0 else "SECURE"
                    print(f"[{time.strftime('%H:%M:%S')}] {status_msg} | Workers: {len(workers)} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Safety monitoring session closed.")


def main():
    parser = argparse.ArgumentParser(description="YOLO11m Industrial Safety & Hazard Zone Guardian")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for webcam, image path, or video path",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.45,
        help="Confidence threshold (default: 0.45)",
    )
    parser.add_argument(
        "--proximity-px",
        type=int,
        default=160,
        help="Hazardous proximity distance in pixels between worker and machinery (default: 160)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output visualization file path (default: output_safety.jpg)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless without GUI (for server execution)",
    )
    args = parser.parse_args()

    print("Loading YOLO11m model (yolo11m.pt)...")
    model = YOLO("yolo11m.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.proximity_px, args.headless, output_path=args.output)
    else:
        process_stream(model, args.source, args.conf, args.proximity_px, args.headless)


if __name__ == "__main__":
    main()
