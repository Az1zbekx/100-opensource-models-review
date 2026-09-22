import argparse
import os
import sys
import time
import cv2
import numpy as np
from PIL import Image
import torch
from transformers import pipeline


COLORMAPS = {
    "inferno": cv2.COLORMAP_INFERNO,
    "magma": cv2.COLORMAP_MAGMA,
    "plasma": cv2.COLORMAP_PLASMA,
    "turbo": cv2.COLORMAP_TURBO,
}


def load_depth_pipeline(device_choice: str = "auto"):
    if device_choice == "auto":
        device_id = 0 if torch.cuda.is_available() else -1
    elif device_choice == "cuda":
        device_id = 0
    else:
        device_id = -1

    device_name = "CUDA (NVIDIA GPU)" if device_id >= 0 else "CPU"
    print(f"Initializing Depth-Anything-V2-Small on: {device_name}...")
    load_start = time.time()

    pipe = pipeline(
        task="depth-estimation",
        model="depth-anything/Depth-Anything-V2-Small-hf",
        device=device_id
    )

    print(f"Model successfully loaded in {time.time() - load_start:.2f}s.")
    return pipe, device_name


def process_depth_map(depth_result, colormap_choice: str = "inferno"):
    # depth_result is PIL.Image or dict from pipeline
    if isinstance(depth_result, dict) and "depth" in depth_result:
        depth_pil = depth_result["depth"]
    else:
        depth_pil = depth_result

    # Convert to numpy array
    depth_np = np.array(depth_pil)

    # Normalize depth map to 0..255 uint8
    depth_min, depth_max = depth_np.min(), depth_np.max()
    if depth_max > depth_min:
        depth_norm = ((depth_np - depth_min) / (depth_max - depth_min) * 255.0).astype(np.uint8)
    else:
        depth_norm = np.zeros_like(depth_np, dtype=np.uint8)

    # Apply color mapping
    if colormap_choice == "gray":
        depth_color = cv2.cvtColor(depth_norm, cv2.COLOR_GRAY2BGR)
    else:
        cmap = COLORMAPS.get(colormap_choice, cv2.COLORMAP_INFERNO)
        depth_color = cv2.applyColorMap(depth_norm, cmap)

    return depth_norm, depth_color


def run_image(pipe, source: str, output_path: str, colormap: str, headless: bool, device_name: str):
    if not os.path.exists(source):
        print(f"Error: Image file '{source}' not found.")
        sys.exit(1)

    print(f"Processing static image: '{source}'...")
    raw_img = Image.open(source).convert("RGB")
    w, h = raw_img.size

    # Run inference
    infer_start = time.time()
    result = pipe(raw_img)
    infer_time = time.time() - infer_start
    fps = 1.0 / infer_time if infer_time > 0 else 0.0

    print(f"Inference complete: {infer_time * 1000:.1f}ms ({fps:.1f} FPS) on {device_name}")

    depth_norm, depth_color = process_depth_map(result, colormap)
    depth_color = cv2.resize(depth_color, (w, h))

    # Convert original PIL to BGR OpenCV
    orig_bgr = cv2.cvtColor(np.array(raw_img), cv2.COLOR_RGB2BGR)

    # Create side-by-side comparison
    side_by_side = np.hstack([orig_bgr, depth_color])

    # Overlay metadata on side-by-side view
    header = f"Depth-Anything-V2-Small | {infer_time*1000:.1f}ms ({fps:.1f} FPS) | {device_name}"
    cv2.putText(side_by_side, header, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(side_by_side, "[Original 2D Input]", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(side_by_side, f"[3D Depth Map ({colormap.upper()})]", (w + 20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Save output
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, depth_color)
        print(f"Depth map saved to: {output_path}")

        # Also save side-by-side artifact
        comp_path = os.path.join(os.path.dirname(output_path), "comparison_" + os.path.basename(output_path))
        cv2.imwrite(comp_path, side_by_side)
        print(f"Side-by-side comparison saved to: {comp_path}")

    if not headless:
        cv2.imshow("Depth Anything V2 - Verification", side_by_side)
        print("Press any key to close the window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def run_webcam(pipe, cam_id: int, colormap: str, headless: bool, device_name: str, output_path: str):
    print(f"Opening webcam camera device: {cam_id}...")
    cap = cv2.VideoCapture(cam_id)

    if not cap.isOpened():
        print(f"\n[Error] Could not open camera device {cam_id}.")
        print("Check if your webcam is connected or accessible at /dev/video0.")
        sys.exit(1)

    # Set camera resolution (standard 640x480 for ultra-high FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Camera successfully opened!")
    print("--------------------------------------------------")
    print("  CONTROLS:")
    print("    'q' - Quit / Exit")
    print("    's' - Save snapshot (image + depth map)")
    print("    'c' - Cycle colormap (inferno -> magma -> plasma -> turbo -> gray)")
    print("--------------------------------------------------")

    cmap_list = ["inferno", "magma", "plasma", "turbo", "gray"]
    cmap_idx = cmap_list.index(colormap) if colormap in cmap_list else 0

    frame_count = 0
    t0 = time.time()
    fps = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from camera.")
                break

            h, w, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)

            # Predict depth
            infer_start = time.time()
            result = pipe(pil_img)
            infer_latency = time.time() - infer_start

            current_cmap = cmap_list[cmap_idx]
            _, depth_color = process_depth_map(result, current_cmap)
            depth_color = cv2.resize(depth_color, (w, h))

            # Calculate rolling FPS
            frame_count += 1
            if time.time() - t0 >= 0.5:
                fps = frame_count / (time.time() - t0)
                frame_count = 0
                t0 = time.time()

            # Create side-by-side view
            combined = np.hstack([frame, depth_color])

            # Overlay HUD
            hud_text = f"FPS: {fps:.1f} | Latency: {infer_latency*1000:.0f}ms | Device: {device_name} | Map: {current_cmap.upper()}"
            cv2.putText(combined, hud_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(combined, "Kamera (2D)", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(combined, "Masofa / 3D Chuqurlik (Yaqin = Yorqin)", (w + 20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            if headless:
                # In headless mode (CI/benchmark), capture 1 frame and exit
                if output_path:
                    cv2.imwrite(output_path, combined)
                    print(f"Headless sample snapshot saved to: {output_path}")
                break

            cv2.imshow("Depth Anything V2 - Real-Time 3D Vision (Laptop Camera)", combined)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
            elif key == ord('s'):
                timestamp = int(time.time())
                save_dir = "data"
                os.makedirs(save_dir, exist_ok=True)
                cam_snap = os.path.join(save_dir, f"capture_{timestamp}_camera.jpg")
                depth_snap = os.path.join(save_dir, f"capture_{timestamp}_depth.jpg")
                comb_snap = os.path.join(save_dir, f"capture_{timestamp}_comparison.jpg")
                cv2.imwrite(cam_snap, frame)
                cv2.imwrite(depth_snap, depth_color)
                cv2.imwrite(comb_snap, combined)
                print(f"[Snapshot Saved] -> {comb_snap}")
            elif key == ord('c'):
                cmap_idx = (cmap_idx + 1) % len(cmap_list)
                print(f"Switched colormap to: {cmap_list[cmap_idx]}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released. Exited successfully.")


def main():
    parser = argparse.ArgumentParser(description="Depth Anything V2 (Small) - Real-Time 3D Monocular Depth Estimation")
    parser.add_argument("--source", type=str, default="data/test_1_office.jpg",
                        help="Input source: '0' for webcam, or path to image file (.jpg/.png)")
    parser.add_argument("--output", type=str, default="data/output_1.jpg",
                        help="Output path for depth map")
    parser.add_argument("--colormap", type=str, default="inferno",
                        choices=["inferno", "magma", "plasma", "turbo", "gray"],
                        help="Color map palette for depth visualization")
    parser.add_argument("--device", type=str, default="auto",
                        choices=["auto", "cuda", "cpu"],
                        help="Inference compute device")
    parser.add_argument("--headless", action="store_true",
                        help="Run without displaying GUI window (saves outputs directly)")
    args = parser.parse_args()

    pipe, device_name = load_depth_pipeline(args.device)

    # Check if source is webcam
    if args.source.isdigit():
        run_webcam(pipe, int(args.source), args.colormap, args.headless, device_name, args.output)
    else:
        run_image(pipe, args.source, args.output, args.colormap, args.headless, device_name)


if __name__ == "__main__":
    main()
