# Audio Flamingo 3 Pinokio Package Setup Instructions

## Package Structure

This Pinokio package clones the Audio Flamingo 3 HuggingFace Space and installs dependencies using a custom requirements.txt for better compatibility. The Audio Flamingo 3 model downloads automatically during first run.

### 1. Package Files ✅ Complete

The package includes these core files:
- `pinokio.js` - Main configuration with Audio Flamingo 3 branding
- `install.js` - Installation script (clones from HuggingFace Spaces)
- `start.js` - Startup script with audio model monitoring
- `torch.js` - PyTorch installation with latest optimizations
- `update.js` - Update script
- `reset.js` - Reset script
- `link.js` - Deduplication script for disk space optimization
- `icon.png` - Audio/AI themed project icon

### 2. Installation Process

The installation process:
1. Clones the Audio Flamingo 3 HuggingFace Space from nvidia/audio-flamingo-3 to app/ directory
2. Installs PyTorch with platform-specific optimizations (CUDA 12.4, DirectML, ROCm)
3. Installs DeepSpeed Windows wheel for enhanced performance
4. Installs dependencies from custom requirements.txt (gradio, transformers>=4.46.0, accelerate, peft, etc.)
5. Sets up virtual environment in app/env/ with all dependencies
6. NVIDIA's audio-flamingo-3 model (~15GB) downloads automatically during first run
7. Creates installation completion marker

### 3. HuggingFace Space Integration

The package now clones from:
```
https://huggingface.co/spaces/nvidia/audio-flamingo-3
```

This ensures:
- Always up-to-date NVIDIA Audio Flamingo 3 code
- Proper requirements.txt handling
- Access to the latest Gradio audio interface
- Official NVIDIA model integration
- Direct access to space updates

### 4. Distribution Files

For the Pinokio package, distribute these files:
- `pinokio.js` - Main configuration
- `install.js` - Installation script (clones HuggingFace Space)
- `start.js` - Startup script with audio monitoring
- `torch.js` - PyTorch installation
- `update.js` - Update script
- `reset.js` - Reset script
- `link.js` - Deduplication script
- `icon.png` - Audio/AI themed project icon
- `README.md` - Audio Flamingo 3 documentation
- `PINOKIO_PACKAGE_README.md` - Package documentation
- `PACKAGE_VALIDATION.md` - Validation checklist
- `SETUP_INSTRUCTIONS.md` - This file
- `PINOKIO_SCRIPT_GUIDE.md` - Comprehensive development guide

### 5. How It Works

1. User installs the Pinokio package (files above)
2. When they click "Install", it:
   - Clones the HuggingFace Space to `app/` directory
   - Installs PyTorch with platform-specific optimizations
   - Installs DeepSpeed Windows wheel for performance
   - Installs dependencies from custom requirements.txt using UV package manager
   - Creates virtual environment in app/env/
   - Verifies the installation
3. User can then start the application through Pinokio interface
4. Model downloads automatically during first startup (~15GB)
5. Gradio web interface becomes available for audio interaction
6. Users can upload audio files and interact with the Audio Flamingo 3 model

### 6. Key Features

- **HuggingFace Space Integration**: Gets latest code from NVIDIA's official space
- **Custom Dependencies**: Uses curated requirements.txt for better compatibility
- **Fast Installation**: Uses UV package manager for lightning-fast dependency installation
- **DeepSpeed Integration**: Windows-optimized DeepSpeed wheel for enhanced performance
- **GPU Optimization**: Supports NVIDIA CUDA, AMD DirectML/ROCm, and CPU fallback
- **Cross-Platform**: Windows, macOS, and Linux support
- **Advanced Features**: XFormers, Triton, and SageAttention optimizations
- **Audio Intelligence**: Large Audio-Language Model for speech, sound, and music understanding
- **Long Audio Support**: Process audio up to 10 minutes in length
- **Multi-Modal Processing**: Advanced audio comprehension capabilities
- **Deduplication Support**: Optional disk space optimization

### 7. Technical Details

**PyTorch Installation:**
- Windows NVIDIA: CUDA 12.4 + XFormers
- Windows AMD: DirectML support
- Linux NVIDIA: CUDA 12.4 + XFormers + SageAttention
- Linux AMD: ROCm 6.2.4 support
- macOS: CPU + Metal acceleration
- CPU fallback: Optimized CPU-only installation

**Audio-Specific Dependencies:**
- transformers>=4.46.0 (latest for audio models)
- gradio>=4.0.0 (modern audio interface)
- accelerate (GPU acceleration)
- peft>=0.14.0 (parameter-efficient fine-tuning)
- huggingface-hub (model downloading)
- torch 2.7.0+ (latest PyTorch)

**Audio Model Features:**
- **Model**: nvidia/audio-flamingo-3 (~15GB)
- **Capabilities**: Speech, sound, and music understanding
- **Context**: Up to 10 minutes of audio input
- **Modes**: Single-turn and thinking mode inference
- **Formats**: WAV, MP3, FLAC, OGG, M4A, and more

### 8. Audio Processing Capabilities

**Supported Audio Formats:**
- WAV (uncompressed, high quality)
- MP3 (compressed, widely compatible)
- FLAC (lossless compression)
- OGG (open source format)
- M4A (Apple audio format)
- Other common audio formats

**Audio Understanding:**
- **Speech Recognition**: Transcribe and understand spoken content
- **Music Analysis**: Analyze musical elements, genres, instruments
- **Sound Recognition**: Identify environmental sounds, effects
- **Long Audio**: Process recordings up to 10 minutes
- **Multi-Turn Conversations**: Extended discussions about audio content

### 9. System Requirements

**Minimum Requirements:**
- RAM: 16GB (32GB+ recommended for optimal audio processing)
- Storage: 20GB free space (for model and dependencies)
- GPU: Recommended for audio model performance (12GB+ VRAM ideal)
- Internet: Stable connection for 15GB model download

**Optimal Performance:**
- GPU: NVIDIA RTX 4070 or better with 12GB+ VRAM
- RAM: 32GB or more
- Storage: SSD with 25GB+ free space
- Audio: Microphone or high-quality audio files

This approach ensures a robust, up-to-date installation that leverages NVIDIA's latest audio intelligence technology and always has access to the most current Audio Flamingo 3 capabilities.