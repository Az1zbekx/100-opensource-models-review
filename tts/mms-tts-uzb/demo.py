import argparse
import time

import numpy as np
import scipy.io.wavfile
import torch
from transformers import AutoTokenizer, VitsModel


def read_input_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        raise ValueError(
            f"'{path}' is empty — please write your Uzbek Cyrillic text into this file"
        )

    return text


def main(input_file: str, output_file: str):
    print("Loading Uzbek TTS model... (facebook/mms-tts-uzb-script_cyrillic)")
    start_time = time.time()

    model_id = "facebook/mms-tts-uzb-script_cyrillic"

    model = VitsModel.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    print(f"Model loaded. Time taken: {time.time() - start_time:.2f} seconds")

    text = read_input_text(input_file)

    print(f"\nReading text from '{input_file}': '{text}'")

    inputs = tokenizer(text, return_tensors="pt")

    start_inference = time.time()

    with torch.no_grad():
        output = model(**inputs).waveform

    audio_data = output.cpu().numpy().squeeze()

    audio_data = np.clip(audio_data, -1.0, 1.0)
    audio_data = (audio_data * 32767).astype(np.int16)

    sample_rate = model.config.sampling_rate

    audio_data = output.cpu().numpy().squeeze()
    print(
        f"DEBUG: min={audio_data.min()}, max={audio_data.max()}, len={len(audio_data)}"
    )

    audio_data = np.clip(audio_data, -1.0, 1.0)
    audio_data = (audio_data * 32767).astype(np.int16)
    print(f"DEBUG (after scale): min={audio_data.min()}, max={audio_data.max()}")

    scipy.io.wavfile.write(output_file, rate=sample_rate, data=audio_data)

    print(
        f"Process finished "
        f"(Inference time: {time.time() - start_inference:.2f} seconds)."
    )

    print(f"Audio successfully saved to '{output_file}'!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        default="input.txt",
        help="File containing Uzbek Cyrillic text",
    )

    parser.add_argument(
        "--output", type=str, default="result.wav", help="Output audio file name"
    )

    args = parser.parse_args()

    main(args.input, args.output)
