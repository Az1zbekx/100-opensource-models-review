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

VEHICLE_LABELS = {
    CLASS_CAR: "Car",
    CLASS_MOTORCYCLE: "Motorcycle",
    CLASS_BUS: "Bus",
    CLASS_TRUCK: "Truck",
}


def process_image(model, image_path: str, conf: float, headless: bool, output_path: str = "output_highway.jpg"):
    """Analyze static highway image for vehicle distribution."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    # Define an active highway detection corridor
    counting_corridor = (0, int(h * 0.20), w, int(h * 0.95))

    results = model(frame, conf=conf, classes=list(VEHICLE_LABELS.keys()), verbose=False)
    boxes = results[0].boxes

    counts = {name: 0 for name in VEHICLE_LABELS.values()}
    total_vehicles = 0

    for box in boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        score = float(box.conf[0])
        v_type = VEHICLE_LABELS.get(cls_id, "Vehicle")

        counts[v_type] += 1
        total_vehicles += 1

        color = (0, 255, 0) if cls_id == CLASS_CAR else (255, 150, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{v_type} {score:.2f}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    # Congestion index
    traffic_density = "HIGH (Congestion Risk)" if total_vehicles >= 8 else ("MODERATE" if total_vehicles >= 4 else "FREE FLOW")
    density_color = (0, 0, 255) if total_vehicles >= 8 else ((0, 165, 255) if total_vehicles >= 4 else (0, 255, 0))

    # Dashboard HUD
    hud_w = min(w - 20, 660)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 85), (20, 22, 25), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 85), (55, 60, 65), 1)
    cv2.putText(frame, f"YOLOv9t Highway Traffic Flow | Density: {traffic_density}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, density_color, 2)
    breakdown_text = f"Total: {total_vehicles} | Cars: {counts['Car']} | Trucks: {counts['Truck']} | Buses: {counts['Bus']} | Moto: {counts['Motorcycle']}"
    cv2.putText(frame, breakdown_text, (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)

    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Vehicle Count Summary: {breakdown_text}")
    print(f"Highway Flow Status: {traffic_density}")

    if not headless:
        cv2.imshow("YOLOv9t - Highway Traffic Flow Counter", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Real-time traffic flow counting and flow rate monitoring."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Highway Flow Counter started (source={video_source}, headless={headless}).")
    print("Press 'q' in video window to exit, or Ctrl+C in terminal.")

    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    cumulative_passed = 0
    gate_prev_y = {}

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
            # Counting gate line (horizontal across middle of frame)
            gate_y = int(h * 0.60)

            results = model(frame, conf=conf, classes=list(VEHICLE_LABELS.keys()), verbose=False)
            boxes = results[0].boxes

            in_frame_counts = {name: 0 for name in VEHICLE_LABELS.values()}
            active_vehicles = 0

            for box in boxes:
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                score = float(box.conf[0])
                v_type = VEHICLE_LABELS.get(cls_id, "Vehicle")
                center_y = int((y1 + y2) / 2)

                in_frame_counts[v_type] += 1
                active_vehicles += 1

                if not headless:
                    color = (0, 255, 0) if cls_id == CLASS_CAR else (255, 150, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{v_type}", (x1, y1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            if not headless:
                # Draw counting gate line
                cv2.line(frame, (0, gate_y), (w, gate_y), (0, 255, 255), 2)
                cv2.putText(frame, "TRAFFIC COUNTING GATE LINE", (15, gate_y - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

                # Dashboard HUD
                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv9t Flow Counter | FPS: {fps:.1f} (GELAN-C)",
                            (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, f"Active Vehicles in Frame: {active_vehicles}",
                            (20, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Cars: {in_frame_counts['Car']} | Trucks: {in_frame_counts['Truck']} | Buses: {in_frame_counts['Bus']} | Moto: {in_frame_counts['Motorcycle']}",
                            (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv9t - Highway Traffic Flow Counter", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Active: {active_vehicles} | Cars: {in_frame_counts['Car']} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Highway traffic flow monitoring session closed.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv9t Highway Traffic Flow & Directional Vehicle Counter")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for webcam, path to image, or path to video",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.40,
        help="Confidence threshold for vehicle detection (default: 0.40)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_highway.jpg",
        help="Path to save output visualization image (default: output_highway.jpg)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (for server / background runs)",
    )
    args = parser.parse_args()

    print("Loading YOLOv9t model (yolov9t.pt)...")
    model = YOLO("yolov9t.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless, args.output)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
