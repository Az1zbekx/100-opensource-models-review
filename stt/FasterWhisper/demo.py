import argparse
import time

from faster_whisper import WhisperModel


def main(audio_file: str, model_size: str):
    print(f"Loading STT model... (Size: {model_size})")
    start_time = time.time()

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Model loaded. Time taken: {time.time() - start_time:.2f} seconds")
    print(f"\nTranscribing '{audio_file}'...")

    inference_start = time.time()
    segments, info = model.transcribe(audio_file, beam_size=5)

    print(
        f"Detected language: {info.language} (Probability: {info.language_probability:.2f})"
    )
    print("-" * 50)

    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

    print("-" * 50)
    print(
        f"Process finished (Inference time: {time.time() - inference_start:.2f} seconds)."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Offline STT (Faster Whisper)")
    parser.add_argument("--audio", type=str, required=True, help="Path to audio file")
    parser.add_argument(
        "--model",
        type=str,
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Model size",
    )
    args = parser.parse_args()
    main(args.audio, args.model)
