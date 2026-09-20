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


def process_image(model, image_path: str, conf: float, proximity_thresh: int, headless: bool):
    """Analyze static image for safety zone breaches."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not open image {image_path}")
        return

    h, w = frame.shape[:2]
    # Define a default critical machinery hazard zone (e.g., right half or central area)
    hazard_zone = (int(w * 0.35), int(h * 0.25), int(w * 0.95), int(h * 0.90))

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

    # Render Hazard Zone
    hz_x1, hz_y1, hz_x2, hz_y2 = hazard_zone
    cv2.rectangle(frame, (hz_x1, hz_y1), (hz_x2, hz_y2), (0, 165, 255), 2)
    cv2.putText(frame, "RESTRICTED HEAVY EQUIPMENT ZONE", (hz_x1 + 10, hz_y1 + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 165, 255), 2)

    breach_count = 0
    proximity_warnings = []

    # Check vehicle proximity & draw vehicles
    for v in vehicles:
        vx1, vy1, vx2, vy2 = v["coords"]
        cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (255, 100, 0), 2)
        cv2.putText(frame, f"{v['type']} {v['conf']:.2f}", (vx1, vy1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

    # Check workers
    for w_obj in workers:
        wx1, wy1, wx2, wy2 = w_obj["coords"]
        w_center = w_obj["center"]

        in_hazard_zone = (hz_x1 <= w_center[0] <= hz_x2 and hz_y1 <= w_center[1] <= hz_y2)
        near_vehicle = False

        for v in vehicles:
            dist = calculate_distance(w_center, v["center"])
            if dist < proximity_thresh:
                near_vehicle = True
                proximity_warnings.append((w_center, v["center"], dist))

        if in_hazard_zone or near_vehicle:
            breach_count += 1
            box_color = (0, 0, 255)
            label = "WORKER HAZARD BREACH!"
        else:
            box_color = (0, 255, 0)
            label = f"Worker {w_obj['conf']:.2f}"

        cv2.rectangle(frame, (wx1, wy1), (wx2, wy2), box_color, 2)
        cv2.putText(frame, label, (wx1, wy1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

    # Draw proximity warning lines
    for p1, p2, dist in proximity_warnings:
        cv2.line(frame, p1, p2, (0, 0, 255), 3)
        mid_point = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
        cv2.putText(frame, f"DANGER: {dist:.0f}px", mid_point,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Dashboard Banner
    if breach_count > 0:
        status_text = f"CRITICAL: {breach_count} SAFETY ZONE VIOLATION(S) DETECTED!"
        status_color = (0, 0, 255)
    else:
        status_text = "SAFETY PROTOCOLS NORMAL: ALL PERSONNEL CLEAR"
        status_color = (0, 255, 0)

    cv2.rectangle(frame, (10, 10), (620, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLO11m Industrial Safety | Workers: {len(workers)} | Machinery: {len(vehicles)}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, status_text, (20, 62),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, status_color, 2)

    output_path = "output_safety.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Safety Assessment: {status_text}")

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
        "--headless",
        action="store_true",
        help="Run headless without GUI (for server execution)",
    )
    args = parser.parse_args()

    print("Loading YOLO11m model (yolo11m.pt)...")
    model = YOLO("yolo11m.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.proximity_px, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.proximity_px, args.headless)


if __name__ == "__main__":
    main()
