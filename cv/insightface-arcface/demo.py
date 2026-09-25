#!/usr/bin/env python3
"""
InsightFace (ArcFace + SCRFD) Deep Face Recognition & Biometrics
Part of 100-OpenSource-Models-Review (CV Series)

SOTA Face Analysis: SCRFD-10G (Face Detection & 5 Landmarks) + ArcFace ResNet-50
(512D Cosine Embedding) + Gender & Age Estimation with Known Face Matching.
"""

import argparse
import os
import sys
import time
import glob
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis


class FaceRecognizer:
    def __init__(self, known_faces_dir="known_faces", threshold=0.45, device="cuda"):
        self.threshold = threshold
        self.known_faces_dir = known_faces_dir
        self.known_embeddings = {}

        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if device == "cuda" else ['CPUExecutionProvider']
        print(f"Loading InsightFace 'buffalo_l' with providers: {providers}...")
        self.app = FaceAnalysis(name="buffalo_l", providers=providers)
        self.app.prepare(ctx_id=0 if device == "cuda" else -1, det_size=(640, 640))

        self.load_known_faces()

    def load_known_faces(self):
        """Precompute face embeddings from known_faces directory."""
        if not os.path.exists(self.known_faces_dir):
            return

        image_files = glob.glob(os.path.join(self.known_faces_dir, "*.*"))
        for img_path in image_files:
            name = os.path.splitext(os.path.basename(img_path))[0]
            img = cv2.imread(img_path)
            if img is None:
                continue

            faces = self.app.get(img)
            if len(faces) > 0:
                # Largest face
                faces = sorted(faces, key=lambda x: (x.bbox[2]-x.bbox[0])*(x.bbox[3]-x.bbox[1]), reverse=True)
                emb = faces[0].embedding
                emb = emb / np.linalg.norm(emb)
                self.known_embeddings[name] = emb
                print(f"Loaded known identity: {name} (from {img_path})")

    def match_face(self, face_emb):
        """Match embedding against known gallery using Cosine Similarity."""
        if not self.known_embeddings:
            return "Noma'lum", 0.0

        target_norm = face_emb / np.linalg.norm(face_emb)
        best_name = "Noma'lum"
        best_sim = 0.0

        for name, k_emb in self.known_embeddings.items():
            sim = float(np.dot(target_norm, k_emb))
            if sim > best_sim:
                best_sim = sim
                if sim >= self.threshold:
                    best_name = name

        return best_name, best_sim


def draw_hud(frame, fps=0.0, num_faces=0):
    """Draw face recognition HUD header."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 50), (20, 24, 28), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    cv2.putText(frame, "InsightFace / ArcFace Biometrics Engine", (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 230, 255), 2)
    cv2.putText(frame, f"Faces detected: {num_faces}", (15, 43),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 210, 220), 1)
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 140, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 120), 2)


def process_faces(frame, recognizer):
    """Detect faces, compute biometrics, match identities, and annotate frame."""
    faces = recognizer.app.get(frame)
    num_faces = len(faces)

    for face in faces:
        bbox = face.bbox.astype(int)
        x1, y1, x2, y2 = bbox

        name, sim = recognizer.match_face(face.embedding)
        gender = "Erkak" if getattr(face, 'gender', 1) == 1 else "Ayol"
        age = getattr(face, 'age', 25)

        # Color: Green if verified known, Orange/Red if unknown
        is_known = (name != "Noma'lum")
        color = (0, 255, 100) if is_known else (0, 140, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # 5 Facial Landmarks (eyes, nose, mouth corners)
        if hasattr(face, 'kps') and face.kps is not None:
            for pt in face.kps:
                px, py = int(pt[0]), int(pt[1])
                cv2.circle(frame, (px, py), 2, (0, 255, 255), -1)

        # Label tags
        label_top = f"{name} ({sim*100:.1f}%)" if is_known else f"{name}"
        label_sub = f"{gender}, ~{age} yosh"

        (tw, th), _ = cv2.getTextSize(label_top, cv2.FONT_HERSHEY_SIMPLEX, 0.50, 1)
        cv2.rectangle(frame, (x1, max(0, y1 - 36)), (x1 + max(tw, 110) + 8, max(0, y1)), color, -1)
        cv2.putText(frame, label_top, (x1 + 4, max(0, y1 - 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 0, 0), 1)
        cv2.putText(frame, label_sub, (x1 + 4, max(0, y1 - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.40, (30, 30, 30), 1)

    return num_faces


def run_image(recognizer, image_path: str, output_path: str = None, headless: bool = False):
    """Inference on single image."""
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Unable to load image '{image_path}'")
        sys.exit(1)

    t0 = time.time()
    num_faces = process_faces(frame, recognizer)
    infer_time = (time.time() - t0) * 1000.0

    draw_hud(frame, fps=1000.0 / max(infer_time, 0.1), num_faces=num_faces)
    print(f"Processed '{image_path}' in {infer_time:.2f}ms | Detected {num_faces} faces.")

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, frame)
        print(f"Annotated result saved to: {output_path}")

    if not headless:
        cv2.imshow("InsightFace Biometrics", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_camera(recognizer, cam_source, output_path: str = None, headless: bool = False):
    """Inference on camera or video stream."""
    try:
        source_idx = int(cam_source)
    except ValueError:
        source_idx = cam_source

    cap = cv2.VideoCapture(source_idx)
    if not cap.isOpened():
        print(f"Error: Unable to open stream '{cam_source}'")
        sys.exit(1)

    print(f"Stream opened: {cam_source}. Press 'q' to quit.")

    writer = None
    fps_start = time.time()
    frame_count = 0
    fps = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        num_faces = process_faces(frame, recognizer)

        now = time.time()
        if now - fps_start >= 1.0:
            fps = frame_count / (now - fps_start)
            frame_count = 0
            fps_start = now

        draw_hud(frame, fps=fps, num_faces=num_faces)

        if output_path and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(output_path, fourcc, 30.0, (w, h))

        if writer:
            writer.write(frame)

        if not headless:
            cv2.imshow("InsightFace Biometrics", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            if frame_count > 60:
                break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="InsightFace / ArcFace Face Recognition")
    parser.add_argument("--source", type=str, default="data/test_1.jpg",
                        help="Camera ID, video path, or image path.")
    parser.add_argument("--known_dir", type=str, default="known_faces",
                        help="Path to known faces directory.")
    parser.add_argument("--threshold", type=float, default=0.45,
                        help="Cosine similarity threshold for matching (default: 0.45).")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to save annotated result.")
    parser.add_argument("--headless", action="store_true",
                        help="Run without displaying OpenCV window.")
    parser.add_argument("--device", type=str, default="auto",
                        choices=["auto", "cuda", "cpu"])

    args = parser.parse_args()

    # Determine device
    device = "cuda" if (args.device == "cuda" or (args.device == "auto" and cv2.cuda.getCudaEnabledDeviceCount() >= 0)) else "cpu"
    # Fallback check
    import torch
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    recognizer = FaceRecognizer(known_faces_dir=args.known_dir, threshold=args.threshold, device=device)

    if args.source.isdigit():
        run_camera(recognizer, int(args.source), args.output, args.headless)
    elif args.source.startswith("rtsp://") or args.source.startswith("http://"):
        run_camera(recognizer, args.source, args.output, args.headless)
    elif os.path.isfile(args.source):
        ext = os.path.splitext(args.source)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            run_image(recognizer, args.source, args.output, args.headless)
        elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
            run_camera(recognizer, args.source, args.output, args.headless)
        else:
            print(f"Unsupported format: {ext}")
            sys.exit(1)
    else:
        print(f"Source '{args.source}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
