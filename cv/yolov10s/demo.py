import argparse
import os
import time
import cv2
from ultralytics import YOLO

# Vehicle COCO Class IDs
CLASS_CAR = 2
CLASS_MOTORCYCLE = 3
CLASS_BUS = 5
CLASS_TRUCK = 7

VEHICLE_CLASSES = {
    CLASS_CAR: "Car",
    CLASS_MOTORCYCLE: "Motorcycle",
    CLASS_BUS: "Bus",
    CLASS_TRUCK: "Truck",
}

LOITERING_LIMIT_SECONDS = 5.0  # seconds before loitering alert


def is_point_in_box(point, box):
    px, py = point
    bx1, by1, bx2, by2 = box
    return bx1 <= px <= bx2 and by1 <= py <= by2


def process_image(model, image_path: str, conf: float, headless: bool):
    """Analyze static image for vehicles parked in restricted zones."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    # Define restricted fire lane / no-parking zone (e.g., center-left lane)
    restricted_zone = (int(w * 0.10), int(h * 0.25), int(w * 0.90), int(h * 0.95))

    results = model(frame, conf=conf, classes=list(VEHICLE_CLASSES.keys()), verbose=False)
    boxes = results[0].boxes

    violator_count = 0
    total_vehicles = 0

    rx1, ry1, rx2, ry2 = restricted_zone

    for box in boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        score = float(box.conf[0])
        v_name = VEHICLE_CLASSES.get(cls_id, "Vehicle")
        center_pt = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        total_vehicles += 1

        is_violation = is_point_in_box(center_pt, restricted_zone)
        if is_violation:
            violator_count += 1
            color = (0, 0, 255)
            label = f"PARKING VIOLATION: {v_name} ({score:.2f})"
        else:
            color = (0, 255, 0)
            label = f"Legal: {v_name} ({score:.2f})"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, center_pt, 4, color, -1)
        cv2.putText(frame, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 2)

    # Draw Restricted Zone
    zone_color = (0, 0, 255) if violator_count > 0 else (0, 165, 255)
    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), zone_color, 2)
    cv2.putText(frame, "RESTRICTED FIRE LANE / NO PARKING ZONE", (rx1 + 10, ry1 + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, zone_color, 2)

    # Status Banner
    status = f"CRITICAL: {violator_count} VEHICLE(S) ILLEGALLY PARKED!" if violator_count > 0 else "STATUS: RESTRICTED LANE CLEAR"
    banner_color = (0, 0, 255) if violator_count > 0 else (0, 255, 0)

    cv2.rectangle(frame, (10, 10), (600, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLOv10s Parking Patrol | Total Vehicles: {total_vehicles}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, status, (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.55, banner_color, 2)

    output_path = "output_parking.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Parking Assessment: {status}")

    if not headless:
        cv2.imshow("YOLOv10s - Smart Parking Patrol", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Real-time parking bay loitering audit."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Parking Patrol initialized (source={video_source}, headless={headless}).")
    print("Press 'q' in GUI window to quit, or Ctrl+C in terminal.")

    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    loiter_start = None
    accumulated_loiter = 0.0

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
            restricted_zone = (int(w * 0.15), int(h * 0.20), int(w * 0.85), int(h * 0.90))
            rx1, ry1, rx2, ry2 = restricted_zone

            results = model(frame, conf=conf, classes=list(VEHICLE_CLASSES.keys()), verbose=False)
            boxes = results[0].boxes

            violators_in_zone = 0

            for box in boxes:
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_pt = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                v_name = VEHICLE_CLASSES.get(cls_id, "Vehicle")

                in_zone = is_point_in_box(center_pt, restricted_zone)
                if in_zone:
                    violators_in_zone += 1
                    color = (0, 0, 255)
                    label = f"VIOLATION: {v_name}"
                else:
                    color = (0, 255, 0)
                    label = v_name

                if not headless:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.circle(frame, center_pt, 4, color, -1)
                    cv2.putText(frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            # Loitering logic
            if violators_in_zone > 0:
                if loiter_start is None:
                    loiter_start = now
                current_duration = now - loiter_start
                if current_duration >= LOITERING_LIMIT_SECONDS:
                    status_text = f"ILLEGAL LOITERING! ({current_duration:.0f}s in Red Zone)"
                    status_color = (0, 0, 255)
                else:
                    status_text = f"Vehicle Lingering ({current_duration:.0f}s)"
                    status_color = (0, 165, 255)
            else:
                if loiter_start is not None:
                    accumulated_loiter += (now - loiter_start)
                    loiter_start = None
                status_text = "ZONE CLEAR: NO VIOLATIONS"
                status_color = (0, 255, 0)

            if not headless:
                # Draw restricted zone boundary
                zone_border = (0, 0, 255) if violators_in_zone > 0 else (0, 165, 255)
                cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), zone_border, 2)
                cv2.putText(frame, "NO PARKING / EMERGENCY ACCESS ZONE", (rx1 + 10, ry1 + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, zone_border, 2)

                # Dashboard HUD
                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv10s Parking Patrol | FPS: {fps:.1f} (NMS-Free)",
                            (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, status_text, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)
                cv2.putText(frame, f"Vehicles in Restricted Zone: {violators_in_zone} / Total: {len(boxes)}",
                            (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv10s - Smart Parking Patrol", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] {status_text} | Violators: {violators_in_zone} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Parking patrol session finished.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv10s Smart Parking Bay & Restricted Loitering Patrol")
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
        help="Confidence threshold for vehicle detection (default: 0.45)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless without GUI (for server execution)",
    )
    args = parser.parse_args()

    print("Loading YOLOv10s model (yolov10s.pt)...")
    model = YOLO("yolov10s.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
