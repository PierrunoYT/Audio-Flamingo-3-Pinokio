# Audio Flamingo 3 - Pinokio Package

This directory contains a complete Pinokio installer package for Audio Flamingo 3, NVIDIA's state-of-the-art Large Audio-Language Model (LALM) with a beautiful Gradio web interface for audio understanding and interaction.

## Package Contents

### Core Pinokio Files
- **`pinokio.js`** - Main configuration and dynamic menu system
- **`install.js`** - Complete installation workflow that clones from HuggingFace Spaces and uses custom requirements
- **`start.js`** - Application startup script with port management and audio model monitoring
- **`torch.js`** - Cross-platform PyTorch installation with latest optimizations
- **`update.js`** - Update workflow for package and dependencies
- **`reset.js`** - Clean removal and reset functionality
- **`link.js`** - Deduplication workflow to save disk space
- **`icon.png`** - Project icon (512x512px audio/AI design)

### Additional Files
- **`PINOKIO_SCRIPT_GUIDE.md`** - Comprehensive guide for creating Pinokio scripts
- **`PINOKIO_PACKAGE_README.md`** - This documentation file
- **`PACKAGE_VALIDATION.md`** - Package validation and testing documentation
- **`SETUP_INSTRUCTIONS.md`** - Detailed setup and usage instructions

## Installation Process

The Pinokio installer will:

1. **Clone Repository**: Downloads the Audio Flamingo 3 HuggingFace Space to app/ directory
2. **Install Dependencies**: Uses custom requirements.txt from root directory for controlled dependency management
3. **Install PyTorch**: Platform and GPU-specific PyTorch installation with CUDA 12.4
4. **Install DeepSpeed**: Windows-optimized DeepSpeed wheel for enhanced performance
5. **Setup Environment**: Creates virtual environment with all dependencies in app/env/
6. **Model Download**: Downloads NVIDIA's audio-flamingo-3 model automatically during first run
7. **Verification**: Tests all components for proper installation

## Features

### Smart Menu System
- **Dynamic State Detection**: Shows appropriate options based on installation status
- **Running Process Awareness**: Detects if installation/startup is in progress
- **Direct Web Access**: "Open Web UI" button when application is running
- **Terminal Access**: View logs and output during operation
- **Deduplication Support**: Save disk space with library file deduplication

### Cross-Platform Support
- **Windows**: Full support with CUDA/DirectML/CPU modes
- **macOS**: Native support for Intel and Apple Silicon with Metal acceleration
- **Linux**: Ubuntu/Debian and other distributions with CUDA/ROCm support

### GPU Optimization
- **NVIDIA CUDA**: Automatic detection and installation of CUDA 12.4 with XFormers
- **AMD Support**: DirectML on Windows, ROCm 6.2.4 on Linux
- **CPU Fallback**: Graceful fallback to CPU-only mode with optimizations
- **Memory Management**: Automatic FP16/FP32 precision selection
- **Advanced Optimizations**: Optional Triton (Linux) and SageAttention support

### Audio Intelligence Features
- **Audio Flamingo 3 Model**: NVIDIA's Large Audio-Language Model for audio understanding
- **Multi-Modal Processing**: Speech, sound, and music comprehension
- **Long Audio Support**: Process audio up to 10 minutes in length
- **Single-Turn Mode**: Quick audio analysis and responses
- **Thinking Mode**: Detailed reasoning about audio content
- **Multi-Turn Conversations**: Extended discussions about audio files
- **Format Support**: WAV, MP3, FLAC, OGG, M4A, and more

### Robust Installation
- **Error Handling**: Graceful handling of installation failures
- **Dependency Management**: Proper virtual environment isolation
- **Update Support**: Easy updates without full reinstallation
- **Clean Reset**: Complete removal for fresh starts
- **UV Package Manager**: Lightning-fast dependency installation
- **Deduplication**: Optional disk space optimization

## Usage Instructions

### For End Users
1. Copy this entire directory to your Pinokio packages folder
2. Launch Pinokio and find "Audio Flamingo 3" in your packages
3. Click "Install" to begin the installation process
4. After installation, click "Start" to launch the application
5. Click "Open Web UI" to access the Gradio interface
6. Upload audio files or use microphone input to interact with the model

### For Developers
1. Ensure all source files are in the same directory as the Pinokio scripts
2. Test the installation process in a clean environment
3. Verify cross-platform compatibility
4. Update version numbers in `pinokio.js` as needed

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **RAM**: 16GB (32GB+ recommended)
- **Storage**: 20GB free space
- **Python**: 3.9+ (installed automatically in virtual environment)

### Recommended for Optimal Performance
- **GPU**: NVIDIA RTX 4070 or better with 12GB+ VRAM
- **RAM**: 32GB or more
- **Storage**: SSD with 25GB+ free space
- **Internet**: Stable connection for model downloads (~15GB)
- **Audio**: Microphone or audio files for input

## Model Information

The application uses NVIDIA's Audio Flamingo 3 model:
- **Model**: nvidia/audio-flamingo-3
- **Type**: Large Audio-Language Model (LALM)
- **Capabilities**: Speech, sound, and music understanding
- **Context**: Up to 10 minutes of audio input
- **License**: NVIDIA Open Model License
- **Download**: Automatic during installation (~15GB)

## Troubleshooting

### Common Issues
1. **Installation Fails**: Check internet connection and disk space (20GB+ required)
2. **PyTorch Issues**: Verify CUDA compatibility or use CPU mode
3. **Model Download Fails**: Check internet connection, large model download required
4. **Memory Issues**: Use shorter audio clips or consider more RAM/VRAM
5. **Port Conflicts**: Pinokio automatically finds available ports
6. **Slow Audio Processing**: Normal on CPU, GPU highly recommended for audio models
7. **Audio Upload Errors**: Check supported formats (WAV, MP3, FLAC, etc.)

### Debug Information
- Installation logs are available in Pinokio terminal
- Application logs shown during startup
- Error messages include helpful troubleshooting hints
- Reset option available for clean reinstallation

## Technical Details

### Virtual Environment
- Isolated Python environment in `app/env/`
- All dependencies installed within virtual environment using custom requirements.txt
- No conflicts with system Python installation
- Uses UV package manager for fast installation

### Model Management
- Audio Flamingo 3 model downloaded automatically during first run
- Cached locally using HuggingFace cache system
- Approximately 15GB download during first startup
- Uses HuggingFace transformers and PEFT libraries
- Custom requirements ensure compatibility

### Port Management
- Automatic port detection and assignment
- Default port 7860 with fallback options
- Accessible via localhost and network interfaces

### GPU Support Matrix

| Platform | NVIDIA | AMD | CPU |
|----------|--------|-----|-----|
| Windows | CUDA 12.4 + XFormers | DirectML | CPU-only |
| Linux | CUDA 12.4 + XFormers + SageAttention | ROCm 6.2.4 | CPU-only |
| macOS | N/A | N/A | CPU + Metal |

## Version History

- **v1.0.0**: Initial Pinokio package release
  - Complete installation workflow for Audio Flamingo 3
  - Cross-platform PyTorch support with latest optimizations
  - Dynamic menu system with deduplication support
  - Professional Gradio interface for audio interaction
  - HuggingFace Space-based installation
  - Advanced audio model monitoring and startup detection

## Support

For issues related to:
- **Pinokio Package**: Check this documentation and Pinokio logs
- **Audio Flamingo 3 Model**: Visit [HuggingFace model page](https://huggingface.co/nvidia/audio-flamingo-3)
- **Installation Problems**: Use the Reset option and try reinstalling
- **Performance Issues**: Check system requirements and GPU compatibility
- **Audio Processing**: Ensure supported audio formats and sufficient memory
- **NVIDIA Support**: Check NVIDIA's documentation for model-specific issues

## License

This Pinokio package is provided under the MIT License. The underlying Audio Flamingo 3 model is licensed under NVIDIA Open Model License - please refer to the official model page for details.