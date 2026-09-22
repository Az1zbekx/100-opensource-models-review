import argparse
import math
import os
import time
import cv2
from ultralytics import YOLO

CLASS_PERSON = 0
CLASS_CAR = 2
CLASS_MOTORCYCLE = 3
CLASS_BUS = 5
CLASS_TRUCK = 7

VEHICLE_IDS = {CLASS_CAR: "Car", CLASS_MOTORCYCLE: "Motorcycle", CLASS_BUS: "Bus", CLASS_TRUCK: "Truck"}


def calculate_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def is_point_in_box(point, box):
    px, py = point
    bx1, by1, bx2, by2 = box
    return bx1 <= px <= bx2 and by1 <= py <= by2


def process_image(model, image_path: str, conf: float, conflict_dist: int, headless: bool, output_path: str = "output_crosswalk.jpg"):
    """Analyze static street image for crosswalk safety and jaywalking."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    # Designated crosswalk zone (middle-bottom horizontal band)
    crosswalk_roi = (int(w * 0.10), int(h * 0.50), int(w * 0.90), int(h * 0.92))
    cx1, cy1, cx2, cy2 = crosswalk_roi

    results = model(frame, conf=conf, classes=[CLASS_PERSON] + list(VEHICLE_IDS.keys()), verbose=False)
    boxes = results[0].boxes

    pedestrians = []
    vehicles = []

    for box in boxes:
        cls_id = int(box.cls[0])
        coords = list(map(int, box.xyxy[0]))
        score = float(box.conf[0])
        foot_pt = (int((coords[0] + coords[2]) / 2), coords[3])
        center_pt = (int((coords[0] + coords[2]) / 2), int((coords[1] + coords[3]) / 2))

        if cls_id == CLASS_PERSON:
            in_crosswalk = is_point_in_box(foot_pt, crosswalk_roi)
            pedestrians.append({
                "coords": coords,
                "foot": foot_pt,
                "in_crosswalk": in_crosswalk,
                "conf": score,
            })
        elif cls_id in VEHICLE_IDS:
            vehicles.append({
                "coords": coords,
                "center": center_pt,
                "type": VEHICLE_IDS[cls_id],
                "conf": score,
            })

    # Render Crosswalk Zone
    cv2.rectangle(frame, (cx1, cy1), (cx2, cy2), (255, 255, 0), 2)
    cv2.putText(frame, "DESIGNATED CROSSWALK ZONE (ZEBRA CROSSING)",
                (cx1 + 10, cy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)

    # Render vehicles
    for v in vehicles:
        vx1, vy1, vx2, vy2 = v["coords"]
        cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (255, 120, 0), 2)
        cv2.putText(frame, f"{v['type']} ({v['conf']:.2f})", (vx1, vy1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 120, 0), 1)

    conflict_lines = []
    jaywalking_count = 0

    # Evaluate pedestrians
    for p in pedestrians:
        px1, py1, px2, py2 = p["coords"]
        p_foot = p["foot"]

        if p["in_crosswalk"]:
            status_label = "Pedestrian: Crosswalk"
            color = (0, 255, 0)
        else:
            status_label = "JAYWALKING IN TRAFFIC"
            color = (0, 0, 255)
            jaywalking_count += 1

        # Check vehicle conflict
        for v in vehicles:
            dist = calculate_distance(p_foot, v["center"])
            if dist < conflict_dist:
                conflict_lines.append((p_foot, v["center"], dist))
                color = (0, 0, 255)
                status_label = "CONFLICT HAZARD!"

        cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)
        cv2.circle(frame, p_foot, 4, color, -1)
        cv2.putText(frame, status_label, (px1, py1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    # Render conflict lines
    for p_pt, v_pt, dist in conflict_lines:
        cv2.line(frame, p_pt, v_pt, (0, 0, 255), 2)
        mid = (int((p_pt[0] + v_pt[0]) / 2), int((p_pt[1] + v_pt[1]) / 2))
        cv2.putText(frame, f"Hazard: {dist:.0f}px", mid,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # Status Banner
    if len(conflict_lines) > 0:
        overall_status = f"CRITICAL: {len(conflict_lines)} PEDESTRIAN-VEHICLE CONFLICT HAZARD(S)!"
        banner_color = (0, 0, 255)
    elif jaywalking_count > 0:
        overall_status = f"WARNING: {jaywalking_count} JAYWALKING PEDESTRIAN(S) OUTSIDE CROSSWALK"
        banner_color = (0, 165, 255)
    else:
        overall_status = "INTERSECTION SAFE: CROSSWALK PROTOCOLS NORMAL"
        banner_color = (0, 255, 0)

    hud_w = min(w - 20, 680)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 75), (20, 22, 25), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 75), (55, 60, 65), 1)
    cv2.putText(frame, f"YOLOv9s Crosswalk Guardian | Pedestrians: {len(pedestrians)} | Vehicles: {len(vehicles)}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)
    cv2.putText(frame, overall_status, (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.50, banner_color, 2)

    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Crosswalk Safety Assessment: {overall_status}")

    if not headless:
        cv2.imshow("YOLOv9s - Pedestrian Crosswalk Guardian", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, conflict_dist: int, headless: bool):
    """Real-time intersection and crosswalk safety tracking."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Crosswalk Guardian initialized (source={video_source}, conflict_dist={conflict_dist}px).")
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

            h, w = frame.shape[:2]
            crosswalk_roi = (int(w * 0.15), int(h * 0.45), int(w * 0.85), int(h * 0.90))
            cx1, cy1, cx2, cy2 = crosswalk_roi

            results = model(frame, conf=conf, classes=[CLASS_PERSON] + list(VEHICLE_IDS.keys()), verbose=False)
            boxes = results[0].boxes

            pedestrians = []
            vehicles = []

            for box in boxes:
                cls_id = int(box.cls[0])
                coords = list(map(int, box.xyxy[0]))
                foot_pt = (int((coords[0] + coords[2]) / 2), coords[3])
                center_pt = (int((coords[0] + coords[2]) / 2), int((coords[1] + coords[3]) / 2))

                if cls_id == CLASS_PERSON:
                    in_crosswalk = is_point_in_box(foot_pt, crosswalk_roi)
                    pedestrians.append({"coords": coords, "foot": foot_pt, "in_crosswalk": in_crosswalk})
                elif cls_id in VEHICLE_IDS:
                    vehicles.append({"coords": coords, "center": center_pt, "type": VEHICLE_IDS[cls_id]})

            conflicts = []
            jaywalkers = 0

            for p in pedestrians:
                px1, py1, px2, py2 = p["coords"]
                p_foot = p["foot"]

                if p["in_crosswalk"]:
                    color = (0, 255, 0)
                    lbl = "Crosswalk"
                else:
                    color = (0, 0, 255)
                    lbl = "JAYWALKING"
                    jaywalkers += 1

                for v in vehicles:
                    dist = calculate_distance(p_foot, v["center"])
                    if dist < conflict_dist:
                        conflicts.append((p_foot, v["center"]))
                        color = (0, 0, 255)
                        lbl = "CONFLICT!"

                if not headless:
                    cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)
                    cv2.putText(frame, lbl, (px1, py1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

            if not headless:
                # Draw vehicles
                for v in vehicles:
                    vx1, vy1, vx2, vy2 = v["coords"]
                    cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (255, 120, 0), 2)
                    cv2.putText(frame, v["type"], (vx1, vy1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 120, 0), 1)

                # Draw crosswalk boundary
                cv2.rectangle(frame, (cx1, cy1), (cx2, cy2), (255, 255, 0), 2)
                cv2.putText(frame, "CROSSWALK ZONE", (cx1 + 10, cy1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

                # Draw conflict lines
                for p_pt, v_pt in conflicts:
                    cv2.line(frame, p_pt, v_pt, (0, 0, 255), 2)

                # Status HUD
                if len(conflicts) > 0:
                    status_str = f"CRITICAL: {len(conflicts)} CONFLICT HAZARD(S)!"
                    s_color = (0, 0, 255)
                elif jaywalkers > 0:
                    status_str = f"WARNING: {jaywalkers} JAYWALKER(S)"
                    s_color = (0, 165, 255)
                else:
                    status_str = "INTERSECTION SAFE"
                    s_color = (0, 255, 0)

                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv9s Crosswalk Guardian | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, status_str, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.62, s_color, 2)
                cv2.putText(frame, f"Pedestrians: {len(pedestrians)} | Vehicles: {len(vehicles)}", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv9s - Pedestrian Crosswalk Guardian", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] Conflicts: {len(conflicts)} | Jaywalkers: {jaywalkers} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Crosswalk guardian session concluded.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv9s Pedestrian Crosswalk Safety & Jaywalking Guardian")
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
        "--conflict-dist",
        type=int,
        default=160,
        help="Proximity distance threshold in pixels between pedestrian and vehicle (default: 160)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_crosswalk.jpg",
        help="Path to save output visualization image (default: output_crosswalk.jpg)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (for server / background runs)",
    )
    args = parser.parse_args()

    print("Loading YOLOv9s model (yolov9s.pt)...")
    model = YOLO("yolov9s.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.conflict_dist, args.headless, args.output)
    else:
        process_stream(model, args.source, args.conf, args.conflict_dist, args.headless)


if __name__ == "__main__":
    main()
