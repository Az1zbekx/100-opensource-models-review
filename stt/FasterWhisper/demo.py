import argparse
import os
import sys
import time
from faster_whisper import WhisperModel


def format_timestamp(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins:02d}:{secs:05.2f}"


def main(audio_file: str, model_size: str, output_file: str, language: str):
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found.")
        sys.exit(1)

    print("==================================================")
    print("  Faster-Whisper (CTranslate2) Offline STT Engine")
    print("==================================================")
    print(f"Loading Whisper model: '{model_size}' (Device: CPU, Compute: int8)...")
    load_start = time.time()

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    load_time = time.time() - load_start
    print(f"Model loaded successfully in {load_time:.2f}s.")
    print(f"Transcribing audio: '{audio_file}'...")

    infer_start = time.time()
    segments, info = model.transcribe(
        audio_file,
        language=language if language else None,
        beam_size=5,
        vad_filter=True
    )

    segments_list = list(segments)
    infer_time = time.time() - infer_start
    audio_duration = info.duration
    rtf = infer_time / audio_duration if audio_duration > 0 else 0.0

    print("--------------------------------------------------")
    print(f"Detected Language: {info.language.upper()} (Confidence: {info.language_probability * 100:.1f}%)")
    print(f"Audio Duration: {audio_duration:.2f}s | Inference Time: {infer_time:.2f}s | RTF: {rtf:.3f}x")
    print("--------------------------------------------------")
    print("Transcription:")

    full_text_lines = []
    for segment in segments_list:
        line = f"[{format_timestamp(segment.start)} -> {format_timestamp(segment.end)}] {segment.text.strip()}"
        print(f"  {line}")
        full_text_lines.append(line)

    full_text = " ".join(s.text.strip() for s in segments_list)
    print("--------------------------------------------------")
    print(f"Full Text: \"{full_text}\"")
    print("==================================================")

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Audio File: {audio_file}\n")
            f.write(f"Detected Language: {info.language} ({info.language_probability * 100:.1f}%)\n")
            f.write(f"Duration: {audio_duration:.2f}s | Latency: {infer_time:.2f}s | RTF: {rtf:.3f}\n")
            f.write("Segments:\n")
            for line in full_text_lines:
                f.write(f"  {line}\n")
            f.write(f"\nFull Transcription:\n{full_text}\n")
        print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="High-Performance Offline STT with Faster-Whisper")
    parser.add_argument("--audio", type=str, required=True, help="Path to input audio file (.wav, .mp3, etc.)")
    parser.add_argument("--model", type=str, default="small", choices=["tiny", "base", "small", "medium", "large-v3"], help="Model size")
    parser.add_argument("--output", type=str, default="", help="Path to save transcription output text file")
    parser.add_argument("--language", type=str, default="", help="Force language code (e.g., 'uz', 'en', 'ru')")
    args = parser.parse_args()

    main(args.audio, args.model, args.output, args.language)
