## Description
<!-- Briefly describe the changes introduced by this pull request. If adding a model, specify its domain and directory. -->

## Checklist
- [ ] Model directory follows the standard layout (`_template/HOW_TO_ADD_A_MODEL.md`):
  - [ ] `README.md` with benchmark stats, memory footprint, and usage instructions in technical English.
  - [ ] Standalone test runner script (e.g., `test.py` or `run.py`).
  - [ ] `requirements.txt` with pinned/compatible dependency versions.
- [ ] No binary weight files (`.pt`, `.bin`, `.safetensors`, `.onnx` > 1MB) committed directly to git.
- [ ] Added entry to root `README.md` domain table.
- [ ] Tested locally or via Docker profile.
