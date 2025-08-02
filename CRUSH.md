# CRUSH Configuration for Audio Flamingo 3 Pinokio Package

## Build/Test/Lint Commands
- **Install**: `node install.js` (via Pinokio interface)
- **Start**: `node start.js` (launches Gradio app at app/app.py)
- **Update**: `node update.js` (git pull)
- **Reset**: `node reset.js` (removes env directory)
- **Link**: `node link.js` (deduplication)
- **Test Python deps**: `cd app && python -c "import torch; print('PyTorch OK')"`
- **Check Gradio**: `cd app && python -c "import gradio; print('Gradio OK')"`

## Code Style Guidelines

### JavaScript (Pinokio Scripts)
- Use `module.exports = { run: [...] }` pattern for Pinokio scripts
- Conditional execution with `when` clauses using template syntax `{{condition}}`
- Use `shell.run` method for command execution with `venv`, `path`, `message` params
- Template variables: `{{args && args.venv ? args.venv : null}}`
- Event monitoring with regex patterns for async operations

### Python (Requirements/Dependencies)
- Pin critical versions: `transformers==4.46.0`, `accelerate==0.34.2`, `peft==0.14.0`
- Use `uv pip install` for faster package management
- Virtual environment in `app/env/` directory
- Audio processing: soundfile, librosa, openai-whisper, pydub
- ML stack: torch, transformers, gradio, accelerate

### Project Structure
- Root: Pinokio configuration files (*.js)
- `app/`: Cloned HuggingFace space with Python application
- `app/env/`: Python virtual environment
- `requirements.txt`: Python dependencies in root
- No package.json - pure Pinokio package

### Error Handling
- Use conditional `when` clauses for platform-specific installs
- GPU detection: `gpu === 'nvidia'`, `gpu === 'amd'`
- Platform detection: `platform === 'win32'`, `platform === 'linux'`, `platform === 'darwin'`
- Graceful fallbacks for CPU-only installations