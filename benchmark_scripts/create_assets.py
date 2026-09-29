import os
import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer

assets_dir = "/app/benchmark_scripts/assets"
os.makedirs(assets_dir, exist_ok=True)

# 1. Uzbek texts (in Cyrillic for MMS model)
uz_texts = {
    "uz_test_1_fintech.wav": "Ҳурматли мижоз, саксон олти нол нол билан тугайдиган картангиздан тўрт юз эллик минг сўм ечилди. Жорий қолдиқ бир миллион икки юз ўттиз минг беш юз сўмни ташкил этмоқда.",
    "uz_test_2_tech_ai.wav": "Микросервислар архитектураси ва Кубернетес кластерларида сунъий интеллект моделларини Докер контейнерларида деплой қилиш сервер тезкорлигини уч бараварга оширди.",
    "uz_test_3_complex.wav": "Тошкент шаҳри Шайхонтоҳур тумани Қоратош кўчасидаги давлат хизматлари марказига соат ўн тўрт нол нолда навбатга ёзилдингиз."
}

print("Synthesizing Uzbek audio files...")
uz_tok = AutoTokenizer.from_pretrained("facebook/mms-tts-uzb-script_cyrillic")
uz_model = VitsModel.from_pretrained("facebook/mms-tts-uzb-script_cyrillic")
rate = uz_model.config.sampling_rate

for fname, text in uz_texts.items():
    inp = uz_tok(text, return_tensors="pt")
    with torch.no_grad():
        wav = uz_model(**inp).waveform[0].numpy()
    out_path = os.path.join(assets_dir, fname)
    scipy.io.wavfile.write(out_path, rate, wav)
    print(f"  Generated {fname} ({len(wav)/rate:.2f}s)")

# 2. English texts
en_texts = {
    "en_test_1_fintech.wav": "Your account balance has been updated. A wire transfer of two thousand four hundred and fifty dollars was processed successfully.",
    "en_test_2_tech_ai.wav": "Deploying transformer-based large language models inside Docker containers requires optimized inference engines and hardware calibration.",
    "en_test_3_navigation.wav": "Navigate to four fifty Lexington Avenue in downtown Manhattan, avoiding toll bridges and heavily congested highway intersections."
}

print("Synthesizing English audio files...")
en_tok = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
en_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
rate_en = en_model.config.sampling_rate

for fname, text in en_texts.items():
    inp = en_tok(text, return_tensors="pt")
    with torch.no_grad():
        wav = en_model(**inp).waveform[0].numpy()
    out_path = os.path.join(assets_dir, fname)
    scipy.io.wavfile.write(out_path, rate_en, wav)
    print(f"  Generated {fname} ({len(wav)/rate_en:.2f}s)")

# 3. Kazakh texts
kz_texts = {
    "kz_test_1_fintech.wav": "Құрметті клиент, сіздің картаңыздан қырық бес мың теңге көлемінде төлем сәтті жүргізілді. Ағымдағы қалдық тексерілді.",
    "kz_test_2_tech.wav": "Жасанды интеллект модельдері мен серверлік инфрақұрылым деректерді өңдеу жылдамдығын айтарлықтай арттырды.",
    "kz_test_3_services.wav": "Астана қаласы, Мәңгілік Ел даңғылында орналасқан халыққа қызмет көрсету орталығына сағат он бесте кезек белгіленді."
}

print("Synthesizing Kazakh audio files...")
kz_tok = AutoTokenizer.from_pretrained("facebook/mms-tts-kaz")
kz_model = VitsModel.from_pretrained("facebook/mms-tts-kaz")
rate_kz = kz_model.config.sampling_rate

for fname, text in kz_texts.items():
    inp = kz_tok(text, return_tensors="pt")
    with torch.no_grad():
        wav = kz_model(**inp).waveform[0].numpy()
    out_path = os.path.join(assets_dir, fname)
    scipy.io.wavfile.write(out_path, rate_kz, wav)
    print(f"  Generated {fname} ({len(wav)/rate_kz:.2f}s)")

print("All audio assets synthesized successfully!")
