import argparse
import math
import os
import time
import cv2
from ultralytics import YOLO

CLASS_PERSON = 0


def calculate_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def get_feet(box):
    return (int((box[0] + box[2]) / 2), int(box[3]))


def process_image(model, image_path: str, conf: float, cluster_radius: int, headless: bool, output_path: str = None):
    """Analyze static image for dense crowd clusters and inter-person proximity."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    results = model(frame, conf=conf, classes=[CLASS_PERSON], verbose=False)
    boxes = results[0].boxes

    persons = []
    for box in boxes:
        coords = list(map(int, box.xyxy[0]))
        score = float(box.conf[0])
        feet = get_feet(coords)
        persons.append({"coords": coords, "feet": feet, "conf": score, "cluster_neighbors": 0})

    # Calculate pairwise proximity and cluster groupings
    n = len(persons)
    proximity_lines = []
    clustered_indices = set()

    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_distance(persons[i]["feet"], persons[j]["feet"])
            if dist < cluster_radius:
                persons[i]["cluster_neighbors"] += 1
                persons[j]["cluster_neighbors"] += 1
                proximity_lines.append((persons[i]["feet"], persons[j]["feet"], dist))
                clustered_indices.add(i)
                clustered_indices.add(j)

    # Draw proximity links between feet
    for p1, p2, dist in proximity_lines:
        cv2.line(frame, p1, p2, (0, 0, 255), 2)
        mid_pt = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
        cv2.circle(frame, mid_pt, 3, (0, 255, 255), -1)

    # Draw persons
    for idx, p in enumerate(persons):
        x1, y1, x2, y2 = p["coords"]
        is_high_dense = idx in clustered_indices and p["cluster_neighbors"] >= 2
        is_pair = idx in clustered_indices

        if is_high_dense:
            color = (0, 0, 255)       # Red: dense cluster node
            label = f"Cluster Node ({p['cluster_neighbors']} adj)"
        elif is_pair:
            color = (0, 165, 255)     # Amber/Orange: proximity pair
            label = f"Proximity ({p['conf']:.2f})"
        else:
            color = (0, 255, 0)       # Green: isolated pedestrian
            label = f"Person ({p['conf']:.2f})"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.circle(frame, p["feet"], 4, color, -1)

        # Draw clean background for label text
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        tag_y1 = max(0, y1 - th - 6)
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tw + 6, tag_y1 + th + 6), (15, 18, 22), -1)
        cv2.rectangle(frame, (x1, tag_y1), (x1 + tw + 6, tag_y1 + th + 6), color, 1)
        cv2.putText(frame, label, (x1 + 3, tag_y1 + th + 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)

    # Density status evaluation
    high_density_nodes = sum(1 for p in persons if p["cluster_neighbors"] >= 2)
    if high_density_nodes >= 3:
        status_msg = f"CRITICAL: {high_density_nodes} INDIVIDUALS IN DENSE CROWD SURGE CLUSTER"
        status_color = (0, 0, 255)
    elif len(clustered_indices) > 0:
        status_msg = f"ADVISORY: {len(clustered_indices)} INDIVIDUALS IN CLOSE PROXIMITY"
        status_color = (0, 165, 255)
    else:
        status_msg = "NORMAL: SPATIALLY DISPERSED PEDESTRIAN FLOW"
        status_color = (0, 255, 0)

    # Dashboard HUD Banner
    hud_w = 680
    hud_h = 82
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 10 + hud_h), (15, 18, 22), -1)
    cv2.rectangle(frame, (10, 10), (10 + hud_w, 10 + hud_h), (60, 64, 72), 1)

    cv2.putText(frame, "YOLOv8m CROWD SPATIAL DENSITY & PROXIMITY ANALYZER",
                (22, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 220, 255), 1, cv2.LINE_AA)
    
    cv2.putText(frame, f"Pedestrians: {n}  |  In Proximity: {len(clustered_indices)}  |  Dense Nodes: {high_density_nodes}  |  Radius: {cluster_radius}px",
                (22, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 205, 215), 1, cv2.LINE_AA)
    
    cv2.putText(frame, f"STATUS: {status_msg}",
                (22, 76), cv2.FONT_HERSHEY_SIMPLEX, 0.46, status_color, 1, cv2.LINE_AA)

    out_file = output_path if output_path else "output_crowd.jpg"
    cv2.imwrite(out_file, frame)
    print(f"Result saved to {out_file}")
    print(f"Crowd Analysis: {status_msg} (People: {n}, Clustered: {len(clustered_indices)}, Dense: {high_density_nodes})")

    if not headless:
        cv2.imshow("YOLOv8m - Crowd Spatial Density Analyzer", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, cluster_radius: int, headless: bool):
    """Real-time crowd cluster and density monitoring."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Crowd Analyzer initialized (source={video_source}, radius={cluster_radius}px).")
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

            results = model(frame, conf=conf, classes=[CLASS_PERSON], verbose=False)
            boxes = results[0].boxes

            persons = []
            for box in boxes:
                coords = list(map(int, box.xyxy[0]))
                feet = get_feet(coords)
                persons.append({"coords": coords, "feet": feet, "neighbors": 0})

            n = len(persons)
            lines = []
            clustered_set = set()

            for i in range(n):
                for j in range(i + 1, n):
                    dist = calculate_distance(persons[i]["feet"], persons[j]["feet"])
                    if dist < cluster_radius:
                        persons[i]["neighbors"] += 1
                        persons[j]["neighbors"] += 1
                        lines.append((persons[i]["feet"], persons[j]["feet"]))
                        clustered_set.add(i)
                        clustered_set.add(j)

            high_density = sum(1 for p in persons if p["neighbors"] >= 2)

            if not headless:
                for p1, p2 in lines:
                    cv2.line(frame, p1, p2, (0, 0, 255), 2)

                for idx, p in enumerate(persons):
                    x1, y1, x2, y2 = p["coords"]
                    if idx in clustered_set and p["neighbors"] >= 2:
                        color = (0, 0, 255)
                        lbl = "Crowd Cluster"
                    elif idx in clustered_set:
                        color = (0, 165, 255)
                        lbl = "Proximity"
                    else:
                        color = (0, 255, 0)
                        lbl = "Person"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, lbl, (x1, y1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

                s_color = (0, 0, 255) if high_density >= 3 else ((0, 165, 255) if len(clustered_set) > 0 else (0, 255, 0))
                s_text = f"CRITICAL: {high_density} IN CONGESTION CLUSTER!" if high_density >= 3 else ("PROXIMITY WARNING" if len(clustered_set) > 0 else "CROWD DISPERSED")

                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv8m Crowd Analyzer | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, s_text, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.62, s_color, 2)
                cv2.putText(frame, f"People: {n} | Clustered: {len(clustered_set)} | Hotspot Nodes: {high_density}",
                            (20, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv8m - Crowd Spatial Density Analyzer", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] People: {n} | High-Density Nodes: {high_density} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print("Crowd density session ended.")


def main():
    parser = argparse.ArgumentParser(description="YOLOv8m Dense Crowd Density & Proximity Cluster Analyzer")
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
        "--cluster-radius",
        type=int,
        default=120,
        help="Proximity distance threshold in pixels for crowd clustering (default: 120)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save output visualization image (default: output_crowd.jpg)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (for server execution)",
    )
    args = parser.parse_args()

    print("Loading YOLOv8m model (yolov8m.pt)...")
    model = YOLO("yolov8m.pt")

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.cluster_radius, args.headless, output_path=args.output)
    else:
        process_stream(model, args.source, args.conf, args.cluster_radius, args.headless)


if __name__ == "__main__":
    main()
