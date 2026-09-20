import argparse
import os
import time
import urllib.request
import cv2
import torch

WEIGHTS_URL = "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-tiny.pt"
WEIGHTS_FILE = "yolov7-tiny.pt"


def ensure_weights(target_path=WEIGHTS_FILE):
    if not os.path.exists(target_path):
        print(f"Downloading {WEIGHTS_FILE} from official release...")
        urllib.request.urlretrieve(WEIGHTS_URL, target_path)
        print("Download complete.")
    return target_path


def load_yolov7_tiny(weights_path):
    print(f"Loading YOLOv7-tiny ({weights_path})...")
    model = torch.hub.load("WongKinYiu/yolov7", "custom", weights_path, trust_repo=True)
    return model


def process_image(model, image_path: str, conf: float, headless: bool):
    """Analyze static doorway image for pedestrian presence."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image from {image_path}")
        return

    h, w = frame.shape[:2]
    doorway_line_y = int(h * 0.55)

    model.conf = conf
    # class 0 is person in COCO
    results = model(frame)
    df = results.pandas().xyxy[0]
    person_df = df[df["class"] == 0]

    count = len(person_df)
    for _, row in person_df.iterrows():
        x1, y1, x2, y2 = int(row["xmin"]), int(row["ymin"]), int(row["xmax"]), int(row["ymax"])
        score = float(row["confidence"])
        foot_y = y2

        color = (0, 255, 0) if foot_y < doorway_line_y else (0, 165, 255)
        status_lbl = "Inside" if foot_y < doorway_line_y else "Approaching"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"Person {score:.2f} ({status_lbl})", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

    # Draw doorway demarcation line
    cv2.line(frame, (0, doorway_line_y), (w, doorway_line_y), (0, 255, 255), 2)
    cv2.putText(frame, "DOORWAY COUNTING THRESHOLD", (15, doorway_line_y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

    # Dashboard HUD
    cv2.rectangle(frame, (10, 10), (580, 75), (20, 20, 20), -1)
    cv2.putText(frame, f"YOLOv7-tiny Doorway Gatekeeper | Persons in View: {count}",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, f"STATUS: {count} ACTIVE PEDESTRIANS MONITORED",
                (20, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 2)

    output_path = "output_doorway.jpg"
    cv2.imwrite(output_path, frame)
    print(f"Result saved to {output_path}")
    print(f"Doorway Audit: {count} pedestrian(s) detected.")

    if not headless:
        cv2.imshow("YOLOv7-tiny - Doorway Foot-Traffic Counter", frame)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def process_stream(model, video_source, conf: float, headless: bool):
    """Real-time bidirectional In/Out foot traffic tracking."""
    try:
        video_source = int(video_source)
    except ValueError:
        pass

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        return

    print(f"Doorway Gatekeeper initialized (source={video_source}, headless={headless}).")
    print("Press 'q' in video window to exit, or Ctrl+C in terminal.")

    model.conf = conf
    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    in_count = 0
    out_count = 0
    previous_positions = {}

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
            line_y = int(h * 0.55)

            # PyTorch inference
            results = model(frame)
            df = results.pandas().xyxy[0]
            person_df = df[df["class"] == 0]

            current_positions = {}
            for idx, row in person_df.iterrows():
                x1, y1, x2, y2 = int(row["xmin"]), int(row["ymin"]), int(row["xmax"]), int(row["ymax"])
                foot_pt = (int((x1 + x2) / 2), y2)
                current_positions[idx] = foot_pt

                # Check transition against previous frames
                for prev_idx, prev_pt in previous_positions.items():
                    # Check vertical transition across threshold
                    if prev_pt[1] < line_y and foot_pt[1] >= line_y:
                        out_count += 1
                        print(f"[{time.strftime('%H:%M:%S')}] Person EXITED (OUT: {out_count})")
                    elif prev_pt[1] >= line_y and foot_pt[1] < line_y:
                        in_count += 1
                        print(f"[{time.strftime('%H:%M:%S')}] Person ENTERED (IN: {in_count})")

                if not headless:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, foot_pt, 4, (0, 255, 0), -1)
                    cv2.putText(frame, "Person", (x1, y1 - 6),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

            previous_positions = current_positions

            if not headless:
                # Draw Doorway Threshold Line
                cv2.line(frame, (0, line_y), (w, line_y), (0, 255, 255), 2)
                cv2.putText(frame, "DOORWAY PASSAGE LINE", (15, line_y - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

                # Dashboard HUD
                net_occupancy = max(0, in_count - out_count)
                cv2.rectangle(frame, (10, 10), (580, 85), (20, 20, 20), -1)
                cv2.putText(frame, f"YOLOv7-tiny Foot-Traffic | FPS: {fps:.1f}", (20, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
                cv2.putText(frame, f"IN: {in_count} | OUT: {out_count} | Net Occupancy: {net_occupancy}",
                            (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 255, 0), 2)
                cv2.putText(frame, f"Persons in Frame: {len(person_df)}", (20, 78),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

                cv2.imshow("YOLOv7-tiny - Doorway Foot-Traffic Counter", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                if frame_count % 30 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] IN: {in_count} | OUT: {out_count} | Net: {in_count - out_count} | FPS: {fps:.1f}")

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        print(f"Gatekeeper session finished. Final counts - IN: {in_count}, OUT: {out_count}")


def main():
    parser = argparse.ArgumentParser(description="YOLOv7-tiny Doorway In/Out Foot-Traffic Counter")
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for webcam, image path, or video file path",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.40,
        help="Confidence threshold for person detection (default: 0.40)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI (for server execution)",
    )
    args = parser.parse_args()

    weights = ensure_weights()
    model = load_yolov7_tiny(weights)

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    if os.path.isfile(args.source) and args.source.lower().endswith(image_extensions):
        process_image(model, args.source, args.conf, args.headless)
    else:
        process_stream(model, args.source, args.conf, args.headless)


if __name__ == "__main__":
    main()
