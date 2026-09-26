import os

repo = '/home/az1z6ekx/100-opensource-models-review'
readme_file = os.path.join(repo, 'README.md')

with open(readme_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split before '## Repo structure'
parts = content.split('## Repo structure')
table_part = parts[0].strip()

# Directory tree
cv_dirs = sorted([d for d in os.listdir(os.path.join(repo, 'cv')) if os.path.isdir(os.path.join(repo, 'cv', d)) and d != 'venv-cv'])
llm_dirs = sorted([d for d in os.listdir(os.path.join(repo, 'llm')) if os.path.isdir(os.path.join(repo, 'llm', d))])
tts_dirs = sorted([d for d in os.listdir(os.path.join(repo, 'tts')) if os.path.isdir(os.path.join(repo, 'tts', d))])
stt_dirs = sorted([d for d in os.listdir(os.path.join(repo, 'stt')) if os.path.isdir(os.path.join(repo, 'stt', d))])

tree_lines = [
    '100-opensource-models-review/',
    '├── README.md # this file — overall index',
    '├── _template/ # template files and rules for adding a new model',
    '├── cv/',
    '│   ├── requirements.txt # unified master dependencies for all 27 CV models'
]
for d in cv_dirs:
    tree_lines.append(f'│   ├── {d}/')
tree_lines.append('├── llm/')
for d in llm_dirs:
    tree_lines.append(f'│   ├── {d}/')
tree_lines.append('├── tts/')
for d in tts_dirs:
    tree_lines.append(f'│   ├── {d}/')
tree_lines.append('├── stt/')
for d in stt_dirs:
    tree_lines.append(f'│   ├── {d}/')
tree_lines.append('└── benchmark_scripts/ # shared benchmark scripts per category')

tree_str = '\n'.join(tree_lines)

footer_str = f"""## Repo structure

```text
{tree_str}
```

## What's in each model's README

- Technical info about the model (architecture, parameters, versions)
- What was done in the project and what issues were encountered
- GPU compatibility and resource requirements (CPU-only or GPU-required)
- Estimated monthly cost if run in the cloud
- How to run it

## Running the models

Each model folder is self-contained — it has its own `Dockerfile`, `run_benchmarks.py`, and `README.md`.

- **CV models (27)**: Run directly in the dedicated, shared `cv/venv-cv` virtual environment (`pip install -r cv/requirements.txt`) with full local webcam (`--source 0`), GUI preview, or `--headless` batch processing.
- **LLM (21) / TTS (26) / STT (26) models**: Run through Docker (`docker compose up <model-name> --build`) or locally via Python.

Rules and template files for adding a new model — [`_template/HOW_TO_ADD_A_MODEL.md`](_template/HOW_TO_ADD_A_MODEL.md).
"""

final_readme = table_part + "\n\n" + footer_str

with open(readme_file, 'w', encoding='utf-8') as f:
    f.write(final_readme)

print("README.md perfectly reconstructed!")
