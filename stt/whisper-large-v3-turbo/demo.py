import argparse
import os
import sys
import time

from faster_whisper import WhisperModel

def format_timestamp(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins:02d}:{secs:05.2f}"

def main(audio_file: str, output_file: str, language: str):
    if not os.path.exists(audio_file):
        print(f"Error: Audio file '{audio_file}' not found.")
        sys.exit(1)

    print("==================================================")
    print("  Whisper-Large-v3-Turbo Speech-to-Text Engine")
    print("  Model: openai/whisper-large-v3-turbo (faster-whisper)")
    print("==================================================")
    print("Loading model parameters (large-v3-turbo, int8)...")
    load_start = time.time()
    model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    load_time = time.time() - load_start
    print(f"Model loaded successfully in {load_time:.2f}s.")

    print(f"Transcribing audio: '{audio_file}'...")
    infer_start = time.time()

    lang_param = None if (not language or language.lower() in ("auto", "none")) else language
    segments, info = model.transcribe(
        audio_file,
        language=lang_param,
        beam_size=5,
        vad_filter=True
    )

    segments_list = list(segments)
    infer_time = time.time() - infer_start
    duration = info.duration
    rtf = infer_time / duration if duration > 0 else 0.0

    print("--------------------------------------------------")
    print(f"Detected Language: {info.language.upper()} (Confidence: {info.language_probability * 100:.1f}%)")
    print(f"Audio Duration: {duration:.2f}s | Inference Time: {infer_time:.2f}s | RTF: {rtf:.3f}x")
    print("--------------------------------------------------")
    print("Transcription Segments:")

    full_text_lines = []
    for s in segments_list:
        line = f"[{format_timestamp(s.start)} -> {format_timestamp(s.end)}] {s.text.strip()}"
        print(f"  {line}")
        full_text_lines.append(line)

    full_text = " ".join(s.text.strip() for s in segments_list)
    print("--------------------------------------------------")
    print(f"Full Text:\n\"{full_text}\"")
    print("==================================================")

    if output_file:
        out_dir = os.path.dirname(os.path.abspath(output_file))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Model: Whisper-Large-v3-Turbo\n")
            f.write(f"Audio: {audio_file}\n")
            f.write(f"Language: {info.language} ({info.language_probability * 100:.1f}%)\n")
            f.write(f"Duration: {duration:.2f}s | Inference Time: {infer_time:.2f}s | RTF: {rtf:.3f}x\n\n")
            f.write("Segments:\n")
            for line in full_text_lines:
                f.write(f"  {line}\n")
            f.write(f"\nFull Transcription:\n{full_text}\n")
        print(f"Transcription saved to '{output_file}'.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_audio = os.path.join(script_dir, "data", "test_1_independence.wav")
    default_output = os.path.join(script_dir, "data", "output_1_independence.txt")
    parser = argparse.ArgumentParser(description="Whisper-Large-v3-Turbo STT Demo")
    parser.add_argument("--audio", type=str, default=default_audio, help="Input audio file")
    parser.add_argument("--output", type=str, default=default_output, help="Output text file")
    parser.add_argument("--language", type=str, default="uz", help="Language code (default: uz)")
    args = parser.parse_args()
    main(args.audio, args.output, args.language)
