import argparse
import os
import sys
import time
import cv2
import numpy as np
import requests

MODEL_URL = "https://huggingface.co/Kalray/yolov4-tiny/resolve/main/yolov4-tiny.onnx"
DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yolov4-tiny.onnx")

COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

ANCHORS = [
    [(81, 82), (135, 169), (344, 319)],  # 13x13 grid
    [(10, 14), (23, 27), (37, 58)],      # 26x26 grid
]


def ensure_model(model_path):
    if not os.path.exists(model_path):
        print(f"[SkyWatch-Tiny] Model weights not found at '{model_path}'.")
        print(f"[SkyWatch-Tiny] Downloading official YOLOv4-tiny ONNX from Hugging Face...")
        resp = requests.get(MODEL_URL, stream=True, timeout=60)
        resp.raise_for_status()
        with open(model_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        print("[SkyWatch-Tiny] Download completed successfully.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Edge Micro-UAV / Low-Power Aerial Surveillance Target Detector using YOLOv4-tiny"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Video source: '0' for webcam, or path to video/image file.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL_PATH,
        help="Path to yolov4-tiny.onnx file.",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for target detection.",
    )
    parser.add_argument(
        "--nms",
        type=float,
        default=0.40,
        help="NMS IoU threshold.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI window and save output directly.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output_aerial.jpg",
        help="Output image/video path when running in headless mode.",
    )
    return parser.parse_args()


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -25.0, 25.0)))


def decode_predictions(outs, orig_w, orig_h, conf_thresh, nms_thresh):
    boxes = []
    confidences = []
    class_ids = []

    for scale_idx, raw_out in enumerate(outs):
        # raw_out shape: (1, 255, grid_h, grid_w)
        grid_h = raw_out.shape[2]
        grid_w = raw_out.shape[3]
        out_trans = raw_out[0].transpose(1, 2, 0).reshape(grid_h, grid_w, 3, 85)
        scale_anchors = ANCHORS[scale_idx]

        for cy in range(grid_h):
            for cx in range(grid_w):
                for a_idx, (pw, ph) in enumerate(scale_anchors):
                    cell = out_trans[cy, cx, a_idx]
                    obj_conf = sigmoid(cell[4])
                    if obj_conf < conf_thresh:
                        continue

                    class_scores = sigmoid(cell[5:])
                    cls_id = int(np.argmax(class_scores))
                    final_score = float(obj_conf * class_scores[cls_id])

                    if final_score >= conf_thresh:
                        bx = (sigmoid(cell[0]) + cx) / grid_w
                        by = (sigmoid(cell[1]) + cy) / grid_h
                        bw = (np.exp(np.clip(cell[2], -10.0, 10.0)) * pw) / 416.0
                        bh = (np.exp(np.clip(cell[3], -10.0, 10.0)) * ph) / 416.0

                        x1 = max(0, int((bx - bw / 2.0) * orig_w))
                        y1 = max(0, int((by - bh / 2.0) * orig_h))
                        w_box = min(orig_w - x1, int(bw * orig_w))
                        h_box = min(orig_h - y1, int(bh * orig_h))

                        boxes.append([x1, y1, w_box, h_box])
                        confidences.append(final_score)
                        class_ids.append(cls_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_thresh, nms_thresh)
    final_detections = []
    if len(indices) > 0:
        for idx in indices:
            i = int(idx)
            x, y, w_box, h_box = boxes[i]
            cid = class_ids[i]
            cname = COCO_CLASSES[cid] if cid < len(COCO_CLASSES) else f"class_{cid}"
            final_detections.append({
                "box": (x, y, x + w_box, y + h_box),
                "conf": confidences[i],
                "class": cname,
            })
    return final_detections


def draw_hud(frame, detections, fps):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    person_count = sum(1 for d in detections if d["class"] == "person")
    vehicle_count = sum(1 for d in detections if d["class"] in ["car", "truck", "bus", "motorcycle"])

    # Tactical Recon Header Panel
    cv2.rectangle(overlay, (20, 20), (580, 185), (15, 20, 25), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    cv2.rectangle(frame, (20, 20), (580, 185), (0, 220, 255), 2)

    cv2.putText(
        frame,
        "SKYWATCH-TINY: AERIAL UAV SURVEILLANCE",
        (35, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.54,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"SAR TARGET ACQUISITION: {len(detections)} LOCK(S) ACTIVE",
        (35, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (0, 255, 120) if len(detections) > 0 else (180, 180, 180),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Personnel Detected: {person_count} | Ground Vehicles: {vehicle_count}",
        (35, 102),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (220, 220, 220),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "TELEM: ALT 45m AGL | HDG 034* NNE | SENSOR: OPTICAL RGB",
        (35, 128),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.46,
        (0, 200, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "RUNTIME: PURE OPENCV DNN (ZERO PYTORCH OVERHEAD)",
        (35, 154),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.46,
        (200, 240, 180),
        1,
        cv2.LINE_AA,
    )

    # Telemetry badge top-right
    badge_w, badge_h = 240, 75
    badge_x = w - badge_w - 20
    cv2.rectangle(
        overlay, (badge_x, 20), (badge_x + badge_w, 20 + badge_h), (15, 20, 25), -1
    )
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
    cv2.rectangle(
        frame, (badge_x, 20), (badge_x + badge_w, 20 + badge_h), (80, 80, 80), 1
    )
    cv2.putText(
        frame,
        "Inference: YOLOv4-tiny",
        (badge_x + 12, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (0, 220, 255),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"Backend: OpenCV DNN | FPS: {fps:.1f}",
        (badge_x + 12, 72),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.44,
        (200, 200, 200),
        1,
        cv2.LINE_AA,
    )

    # Crosshair reticle in frame center
    cx, cy = w // 2, h // 2
    cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 220, 255), 1, cv2.LINE_AA)
    cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 220, 255), 1, cv2.LINE_AA)
    cv2.circle(frame, (cx, cy), 12, (0, 220, 255), 1, cv2.LINE_AA)

    # Draw Tactical Bounding Boxes
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        cname = det["class"]
        conf = det["conf"]

        box_color = (0, 255, 255) if cname == "person" else (0, 200, 100)
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

        # Tactical corner brackets
        corner_len = 10
        cv2.line(frame, (x1, y1), (x1 + corner_len, y1), (255, 255, 255), 2)
        cv2.line(frame, (x1, y1), (x1, y1 + corner_len), (255, 255, 255), 2)
        cv2.line(frame, (x2, y2), (x2 - corner_len, y2), (255, 255, 255), 2)
        cv2.line(frame, (x2, y2), (x2, y2 - corner_len), (255, 255, 255), 2)

        cv2.putText(
            frame,
            f"TGT [{cname.upper()}]: {conf:.2f}",
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.46,
            box_color,
            2,
            cv2.LINE_AA,
        )


def process_image_with_net(net, img, args):
    orig_h, orig_w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(
        img, 1.0 / 255.0, (416, 416), swapRB=True, crop=False
    )
    net.setInput(blob)
    out_names = net.getUnconnectedOutLayersNames()
    outs = net.forward(out_names)
    return decode_predictions(outs, orig_w, orig_h, args.conf, args.nms)


def run_pipeline(args):
    ensure_model(args.model)
    print(f"[SkyWatch-Tiny] Loading ONNX model from: {args.model}")
    net = cv2.dnn.readNetFromONNX(args.model)

    is_webcam = args.source.isdigit()
    is_image = any(args.source.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"])

    if is_image:
        img = cv2.imread(args.source)
        if img is None:
            print(f"Error: Unable to open image '{args.source}'")
            sys.exit(1)
        start_t = time.time()
        detections = process_image_with_net(net, img, args)
        proc_time = time.time() - start_t
        fps = 1.0 / max(proc_time, 1e-5)

        draw_hud(img, detections, fps)
        cv2.imwrite(args.output, img)
        print(f"Result saved to {args.output}")
        print(f"Aerial Surveillance Audit: {len(detections)} targets acquired. Detections: {[d['class'] for d in detections]}")
        return

    source_val = int(args.source) if is_webcam else args.source
    cap = cv2.VideoCapture(source_val)
    if not cap.isOpened():
        print(f"Error: Unable to open video source '{args.source}'")
        sys.exit(1)

    prev_time = time.time()
    print("[SkyWatch-Tiny] Tactical aerial stream running. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-5)
        prev_time = curr_time

        detections = process_image_with_net(net, frame, args)
        draw_hud(frame, detections, fps)

        if not args.headless:
            cv2.imshow("YOLOv4-tiny Aerial Reconnaissance HUD", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        else:
            cv2.imwrite(args.output, frame)
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args)
