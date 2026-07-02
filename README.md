# Audio Flamingo 3 (Pinokio)

[NVIDIA Audio Flamingo 3](https://huggingface.co/nvidia/audio-flamingo-3-hf) is a large audio–language model for speech, sound, and music understanding. This repository is a **Pinokio launcher**: it installs dependencies into a project-local virtual environment and runs a **Gradio** web UI defined in [`app/app.py`](app/app.py).

## What it does

- Loads the `nvidia/audio-flamingo-3-hf` weights (via Hugging Face Hub on first run; large download).
- Exposes tabs for single-turn Q&A, transcription, and “think” / long-audio style prompts in the browser.

## How to use (Pinokio)

1. Open this app in **Pinokio**.
2. Run **Install** once (PyTorch via `torch.js`, then Python packages from [`app/requirements.txt`](app/requirements.txt)).
3. Run **Start**. When the UI is ready, use **Open Web UI** from the sidebar, or follow the URL shown in the terminal.

**Reset** removes the `env` virtual environment. **Update** runs `git pull` and upgrades Python dependencies.

## Requirements and license

- A capable **NVIDIA GPU** is recommended for practical use; CPU may run but will be slow.
- Model use is subject to NVIDIA’s **non-commercial research** terms; see the About tab in the UI and the model card on Hugging Face.
- If the model weights are gated on Hugging Face, run `huggingface-cli login` (or set the `HF_TOKEN` environment variable) inside the app's virtual environment before starting, otherwise model loading will fail on first run.

## Windows notes

- NVIDIA GPUs use the standard CUDA wheels; AMD GPUs fall back to `torch-directml`, which lags behind mainline PyTorch releases — if install fails on an AMD GPU, see the version-pinning note in [`torch.js`](torch.js).
- No CPU-only fallback beyond the default `torch.js` CPU branch is provided; a 7B-parameter model will be very slow without a GPU.

## Programmatic access

This demo is built for **interactive use in the browser** through Gradio. There is no separate HTTP API enabled by default.

- **Python**: Run the app outside Pinokio from the `app` folder with the same virtualenv and `python app.py`. You can import and call the underlying model code only by extending `app/app.py` yourself (not exposed as a stable public API in this launcher).
- **JavaScript / cURL**: Not applicable unless you add a server route or use Gradio’s optional sharing/API features in code; the stock launcher does not start a documented REST surface.

For automation, prefer **Pinokio** script APIs (`install.js`, `start.js`, etc.) or running `python app.py` under your own process manager.
