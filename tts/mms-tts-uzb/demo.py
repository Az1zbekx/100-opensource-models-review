import argparse
import time
import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer

def main(text: str, output_file: str):
    print("Loading Uzbek TTS model... (facebook/mms-tts-uzb)")
    start_time = time.time()
    
    model_id = "facebook/mms-tts-uzb"
    model = VitsModel.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    print(f"Model loaded. Time taken: {time.time() - start_time:.2f} seconds")
    print(f"\nReading text: '{text}'")
    
    inputs = tokenizer(text, return_tensors="pt")
    
    start_inference = time.time()
    with torch.no_grad():
        output = model(**inputs).waveform
    
    audio_data = output.cpu().numpy().squeeze()
    sample_rate = model.config.sampling_rate
    
    scipy.io.wavfile.write(output_file, rate=sample_rate, data=audio_data)
    
    print(f"Process finished (Inference time: {time.time() - start_inference:.2f} seconds).")
    print(f"Audio successfully saved to '{output_file}'!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default="Hello, my name is artificial intelligence.", help="Text to be converted to audio")
    parser.add_argument("--output", type=str, default="result.wav", help="Output audio file name")
    args = parser.parse_args()
    main(args.text, args.output)