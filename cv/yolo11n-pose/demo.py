import argparse
import os
import sys
import time
import math
import cv2
import numpy as np
import torch
from ultralytics import YOLO

# COCO 17 Keypoints mapping
KEYPOINTS_DICT = {
    0: "nose",
    1: "left_eye",
    2: "right_eye",
    3: "left_ear",
    4: "right_ear",
    5: "left_shoulder",
    6: "right_shoulder",
    7: "left_elbow",
    8: "right_elbow",
    9: "left_wrist",
    10: "right_wrist",
    11: "left_hip",
    12: "right_hip",
    13: "left_knee",
    14: "right_knee",
    15: "left_ankle",
    16: "right_ankle",
}

# Skeleton connection pairs for drawing
SKELETON_PAIRS = [
    (0, 1), (0, 2), (1, 3), (2, 4),        # Face
    (5, 6), (5, 7), (7, 9),                 # Left arm
    (6, 8), (8, 10),                        # Right arm
    (5, 11), (6, 12), (11, 12),             # Torso
    (11, 13), (13, 15),                     # Left leg
    (12, 14), (14, 16)                      # Right leg
]


def calculate_angle(p1, p2, p3):
    """Calculate the interior angle between three 2D points in degrees."""
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom == 0:
        return 0.0
    cosine = np.clip(np.dot(v1, v2) / denom, -1.0, 1.0)
    return float(np.degrees(np.arccos(cosine)))


def draw_hud(frame, title, stats, instructions=None):
    """Draw a clean, semi-transparent HUD banner on top of the frame."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    cv2.putText(frame, title, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 200), 2)
    stat_str = " | ".join(stats)
    cv2.putText(frame, stat_str, (15, 47), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)

    if instructions:
        inst_overlay = frame.copy()
        cv2.rectangle(inst_overlay, (0, h - 30), (w, h), (20, 20, 20), -1)
        cv2.addWeighted(inst_overlay, 0.75, frame, 0.25, 0, frame)
        cv2.putText(frame, instructions, (15, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)


def analyze_posture_and_ergonomics(kpts):
    """Analyze posture (spine tilt, slouching) from detected keypoints."""
    # Check required keypoints: nose(0), shoulders(5,6), hips(11,12)
    if len(kpts) < 17:
        return None

    nose = kpts[0]
    l_sh, r_sh = kpts[5], kpts[6]
    l_hip, r_hip = kpts[11], kpts[12]

    # Valid if shoulders and at least one hip or ear have confidence > 0.3
    if l_sh[2] < 0.3 or r_sh[2] < 0.3:
        return None

    mid_shoulder = ((l_sh[0] + r_sh[0]) / 2.0, (l_sh[1] + r_sh[1]) / 2.0)
    
    if l_hip[2] > 0.3 and r_hip[2] > 0.3:
        mid_hip = ((l_hip[0] + r_hip[0]) / 2.0, (l_hip[1] + r_hip[1]) / 2.0)
        # Angle of spine relative to vertical line
        dx = mid_shoulder[0] - mid_hip[0]
        dy = mid_hip[1] - mid_shoulder[1]  # positive upwards
        spine_tilt = abs(math.degrees(math.atan2(dx, max(dy, 1e-5))))

        status = "Good Posture" if spine_tilt < 15.0 else ("Mild Slouch" if spine_tilt < 28.0 else "Slouched / Warning")
        color = (0, 255, 0) if spine_tilt < 15.0 else ((0, 200, 255) if spine_tilt < 28.0 else (0, 0, 255))
        return {
            "type": "spine",
            "tilt_angle": spine_tilt,
            "status": status,
            "color": color,
            "point": (int(mid_shoulder[0]), int(mid_shoulder[1]))
        }
    
    # Fallback: Head-to-shoulder angle if hips not visible
    if nose[2] > 0.3:
        dx = nose[0] - mid_shoulder[0]
        dy = mid_shoulder[1] - nose[1]
        neck_tilt = abs(math.degrees(math.atan2(dx, max(dy, 1e-5))))
        status = "Head Up" if neck_tilt < 20.0 else "Forward Head / Slouch"
        color = (0, 255, 0) if neck_tilt < 20.0 else (0, 140, 255)
        return {
            "type": "neck",
            "tilt_angle": neck_tilt,
            "status": status,
            "color": color,
            "point": (int(nose[0]), int(nose[1]))
        }

    return None


def process_frame(model, frame, conf: float = 0.3, enable_posture: bool = True):
    """Run YOLO11n-pose on a single frame and return plotted frame + analytics."""
    h, w = frame.shape[:2]
    t0 = time.time()
    results = model(frame, conf=conf, verbose=False)
    infer_time = (time.time() - t0) * 1000.0

    annotated = results[0].plot(boxes=True, kpt_radius=5, kpt_line=True)

    persons_count = 0
    posture_alerts = []

    if results[0].keypoints is not None and len(results[0].keypoints) > 0:
        kpts_tensor = results[0].keypoints.data.cpu().numpy()
        persons_count = len(kpts_tensor)

        if enable_posture:
            for idx, person_kpts in enumerate(kpts_tensor):
                posture_info = analyze_posture_and_ergonomics(person_kpts)
                if posture_info:
                    posture_alerts.append(posture_info)
                    pt = posture_info["point"]
                    lbl = f"{posture_info['status']} ({posture_info['tilt_angle']:.1f}deg)"
                    cv2.putText(annotated, lbl, (max(10, pt[0] - 50), max(25, pt[1] - 15)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, posture_info["color"], 2)

    return annotated, infer_time, persons_count, posture_alerts


def run_image(model, source_path: str, output_path: str, conf: float, headless: bool):
    """Run inference on a single static image."""
    if not os.path.exists(source_path):
        print(f"Error: Source image not found at '{source_path}'")
        sys.exit(1)

    print(f"Processing image: {source_path}")
    frame = cv2.imread(source_path)
    if frame is None:
        print(f"Error: Could not decode image '{source_path}'")
        sys.exit(1)

    annotated, infer_time, count, alerts = process_frame(model, frame, conf=conf)
    fps = 1000.0 / infer_time if infer_time > 0 else 0.0

    stats = [
        f"Inference: {infer_time:.1f}ms ({fps:.1f} FPS)",
        f"Persons: {count}",
        f"Postures Analyzed: {len(alerts)}"
    ]
    draw_hud(annotated, "YOLO11n-Pose Human Skeleton & Posture Estimation", stats)

    print(f"Completed: Detected {count} person(s) in {infer_time:.1f}ms ({fps:.1f} FPS)")
    for i, a in enumerate(alerts):
        print(f"  Person #{i+1}: {a['status']} (tilt: {a['tilt_angle']:.1f}°)")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, annotated)
        print(f"Annotated result successfully saved to '{output_path}'")

    if not headless:
        cv2.imshow("YOLO11n-Pose Demo", annotated)
        print("Press any key in GUI window to exit...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_camera(model, cam_idx: int, conf: float):
    """Run live real-time pose estimation using webcam."""
    print(f"Connecting to webcam index {cam_idx}...")
    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        print(f"Error: Could not open webcam at index {cam_idx}.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\nLive camera running!")
    print("  Controls:")
    print("    'q' - Quit")
    print("    's' - Save snapshot to pose_snapshot.jpg")
    print("    'p' - Toggle Posture Ergonomics analysis\n")

    enable_posture = True
    prev_time = time.time()
    fps_smooth = 0.0

    cv2.namedWindow("YOLO11n-Pose Camera Demo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("YOLO11n-Pose Camera Demo", 1024, 600)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Failed to grab frame from camera.")
            break

        now = time.time()
        fps_real = 1.0 / (now - prev_time) if (now - prev_time) > 0 else 0.0
        prev_time = now
        fps_smooth = 0.9 * fps_smooth + 0.1 * fps_real if fps_smooth > 0 else fps_real

        annotated, infer_time, count, alerts = process_frame(
            model, frame, conf=conf, enable_posture=enable_posture
        )

        hud_stats = [
            f"Camera FPS: {fps_smooth:.1f}",
            f"Infer: {infer_time:.1f}ms",
            f"People: {count}",
            f"Ergonomics: {'ON' if enable_posture else 'OFF'}"
        ]
        draw_hud(
            annotated,
            "YOLO11n-Pose Real-Time Skeleton Tracker",
            hud_stats,
            "Keys: [Q] Quit | [S] Snapshot | [P] Toggle Ergonomics"
        )

        cv2.imshow("YOLO11n-Pose Camera Demo", annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('s'):
            snap_path = f"pose_snapshot_{int(time.time())}.jpg"
            cv2.imwrite(snap_path, annotated)
            print(f"Snapshot saved to '{snap_path}'")
        elif key == ord('p'):
            enable_posture = not enable_posture
            print(f"Posture Ergonomics analysis: {'ENABLED' if enable_posture else 'DISABLED'}")

        # Safely detect window close ('X' button) across different OpenCV backends
        try:
            if cv2.getWindowProperty("YOLO11n-Pose Camera Demo", cv2.WND_PROP_VISIBLE) < 1:
                break
        except cv2.error:
            break

    cap.release()
    cv2.destroyAllWindows()


def run_video(model, video_path: str, output_path: str, conf: float, headless: bool):
    """Process video file frame by frame."""
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        sys.exit(1)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'.")
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out_writer = None
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"Processing video: {video_path} ({total_frames} frames)...")
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        annotated, infer_time, count, alerts = process_frame(model, frame, conf=conf)
        stats = [
            f"Frame: {frame_idx}/{total_frames}",
            f"Infer: {infer_time:.1f}ms",
            f"Persons: {count}"
        ]
        draw_hud(annotated, "YOLO11n-Pose Video Tracker", stats)

        if out_writer:
            out_writer.write(annotated)

        if not headless:
            cv2.imshow("YOLO11n-Pose Video Demo", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    if out_writer:
        out_writer.release()
        print(f"Annotated video saved to '{output_path}'")
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="YOLO11n-Pose: Real-time 17-Keypoint Human Skeleton & Posture Estimation"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Input source: '0' for default webcam, video file path, or image file path."
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "yolo11n-pose.pt"),
        help="Path to YOLO11n-pose weights."
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.3,
        help="Confidence threshold for keypoints and detection (default: 0.3)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save annotated output image or video."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without displaying graphical OpenCV GUI windows."
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cuda", "cpu"],
        help="Device to run inference on ('auto', 'cuda', or 'cpu')."
    )

    args = parser.parse_args()

    # Determine device
    if args.device == "cuda":
        device = "cuda:0"
    elif args.device == "cpu":
        device = "cpu"
    else:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

    print(f"Loading YOLO11n-Pose from '{args.weights}' on device: {device.upper()}...")
    model = YOLO(args.weights)
    model.to(device)

    # Route source type
    if args.source.isdigit():
        cam_idx = int(args.source)
        run_camera(model, cam_idx, conf=args.conf)
    elif os.path.isfile(args.source):
        ext = os.path.splitext(args.source)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            run_image(model, args.source, args.output, args.conf, args.headless)
        elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
            run_video(model, args.source, args.output, args.conf, args.headless)
        else:
            print(f"Unsupported file extension: {ext}")
            sys.exit(1)
    else:
        print(f"Error: Source '{args.source}' is neither a camera index nor an existing file.")
        sys.exit(1)


if __name__ == "__main__":
    main()
