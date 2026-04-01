# Known Issues and Status

## Architecture Change (v2.0)

Migrated from the broken NVIDIA `llava`-based HF Space clone to the **native 🤗 Transformers API** (`AudioFlamingo3ForConditionalGeneration`), which was added to Transformers in November 2025.

### What changed:
- **Removed** git clone of `huggingface.co/spaces/PierrunoYT/audio-flamingo-3` — no longer needed
- **Removed** DeepSpeed, triton, pytorchvideo, openai-whisper, and other legacy dependencies
- **app.py** now lives in project root and uses `nvidia/audio-flamingo-3-hf` via Transformers
- **requirements.txt** simplified to only what's needed
- **Pinokio scripts** updated: venv at `./env` instead of `app/env`
- Model downloads handled automatically by `huggingface_hub` / `transformers`

## Resolved Issues
- [x] Broken `llava` import (old NVIDIA Docker-only package)
- [x] `peft` / `transformers` version mismatch causing `ModuleNotFoundError`
- [x] Platform-specific DeepSpeed installation complexity
- [x] Incorrect reset/update directory paths
- [x] Unnecessary git clone step

## Remaining Notes
- ⚠️ Model is ~14GB+ (7B params) — first launch will download weights
- ⚠️ Requires NVIDIA GPU with sufficient VRAM (16GB+ recommended)
- ⚠️ Non-commercial research use only (NVIDIA OneWay Noncommercial License)
