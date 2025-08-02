# Audio Flamingo 3 Pinokio Package

A complete Pinokio installation package for running NVIDIA's Audio Flamingo 3 locally with a beautiful Gradio web interface.

## 🚀 Features

- **🎵 Audio Flamingo 3 Model**: NVIDIA's state-of-the-art Large Audio-Language Model (LALM)
- **🔊 Multi-Modal Understanding**: Process speech, sound, and music with advanced AI
- **🧠 Audio Intelligence**: Single-turn and thinking mode inference for complex audio analysis
- **⏱️ Long Audio Support**: Comprehend audio up to 10 minutes in length
- **💬 Gradio Interface**: Clean, professional web interface for audio interaction
- **⚡ GPU Acceleration**: Automatic CUDA/DirectML/ROCm support when available
- **🔒 Complete Privacy**: Runs entirely offline, no data sent externally
- **🌐 Cross-Platform**: Windows, macOS, and Linux support

## 📋 Requirements

- **RAM**: 16GB+ (32GB+ recommended for optimal performance)
- **Storage**: ~15GB for model files (downloaded automatically)
- **GPU**: Highly recommended (12GB+ VRAM for best performance)
- **OS**: Windows 10/11, macOS, or Linux
- **Audio**: Microphone or audio files for input

## 🛠️ Installation

### Via Pinokio (Recommended)

1. Install [Pinokio](https://pinokio.computer/)
2. Open Pinokio and navigate to "Discover"
3. Search for "Audio Flamingo 3" or paste this repository URL:
   ```
   https://github.com/PierrunoYT/Audio-Flamingo-3-Pinokio
   ```
4. Click "Install" and wait for the installation to complete
5. Click "Start" to launch Audio Flamingo 3
6. Open the web interface when it becomes available

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PierrunoYT/Audio-Flamingo-3-Pinokio.git
   cd Audio-Flamingo-3-Pinokio
   ```

2. Install Pinokio and run the installation script through the Pinokio interface

## 🎯 Usage

1. **Start the Application**: Click "Start" in Pinokio
2. **Open Web Interface**: Click "Open Web UI" when available
3. **Audio Input**: Upload audio files or use microphone input
4. **Interact**: Ask questions about the audio content
5. **Advanced Features**:
   - Single-turn mode for quick analysis
   - Thinking mode for detailed reasoning
   - Multi-turn conversations about audio content
   - Support for various audio formats (WAV, MP3, FLAC, etc.)

## 🏗️ Project Structure

```
Audio-Flamingo-3-Pinokio/
├── pinokio.js              # Main Pinokio configuration
├── install.js              # Installation workflow
├── start.js                # Application startup
├── update.js               # Update workflow
├── reset.js                # Reset/cleanup workflow
├── link.js                 # Deduplication workflow
├── torch.js                # PyTorch installation
├── app.py                  # Main Gradio application
├── requirements.txt        # Python dependencies
├── icon.png                # Project icon
├── README.md               # This file
└── app/                    # Created during installation
    ├── env/                # Python virtual environment
    └── models/             # Downloaded model files
        └── audio-flamingo-3/
```

## 🔧 Technical Details

### Model Information
- **Model**: nvidia/audio-flamingo-3
- **Type**: Large Audio-Language Model (LALM)
- **Capabilities**: Speech, sound, and music understanding
- **Context**: Up to 10 minutes of audio input
- **License**: NVIDIA Open Model License
- **Precision**: FP16 on GPU, FP32 on CPU

### Dependencies
- PyTorch 2.7.0+ with CUDA 12.4 support
- Transformers 4.46.0+
- Gradio 4.0.0+
- Accelerate, PEFT 0.14.0+
- HuggingFace Hub

### GPU Support Matrix

| Platform | NVIDIA | AMD | CPU |
|----------|--------|-----|-----|
| Windows | CUDA 12.4 + XFormers | DirectML | CPU-only |
| Linux | CUDA 12.4 + XFormers + SageAttention | ROCm 6.2.4 | CPU-only |
| macOS | N/A | N/A | CPU + Metal |

## 🚨 Troubleshooting

### Common Issues

**Slow responses on CPU**
- This is normal - CPU inference is much slower than GPU
- Audio models are particularly compute-intensive
- Consider using a GPU with 12GB+ VRAM for optimal performance

**Out of memory errors**
- Audio models require significant memory
- Close other applications to free RAM/VRAM
- Use shorter audio clips (under 5 minutes)
- Consider CPU mode if GPU memory is insufficient

**Model download fails**
- Check internet connection
- Model files (~15GB) download automatically on first use
- Downloads are cached for future use
- Ensure sufficient disk space

**Audio upload errors**
- Supported formats: WAV, MP3, FLAC, OGG, M4A
- Maximum file size may be limited by available memory
- Try converting to WAV format if issues persist

### Performance Tips

- **GPU Users**: Use NVIDIA GPU with 12GB+ VRAM for best experience
- **CPU Users**: Use shorter audio clips and be patient with processing
- **Memory**: Close unnecessary applications during use
- **Audio Quality**: Higher quality audio may provide better results
- **File Size**: Compress audio files if memory is limited

## 🔄 Updates

The package includes an automatic update system:

1. Click "Update" in the Pinokio interface
2. Wait for dependencies and model updates to complete
3. Restart the application to use the latest version

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Fork this repository
2. Make your changes to the Pinokio scripts or Gradio interface
3. Test thoroughly on your target platform
4. Submit a pull request with a clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The Audio Flamingo 3 model is licensed under NVIDIA Open Model License.

## 🙏 Acknowledgments

- [NVIDIA](https://nvidia.com/) for the Audio Flamingo 3 model
- [Pinokio](https://pinokio.computer/) for the amazing AI package manager
- [Gradio](https://gradio.app/) for the web interface framework
- [HuggingFace](https://huggingface.co/) for model hosting and transformers library
- The open-source AI community for making this possible

## 📞 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and community support
- **Documentation**: Check the [Pinokio documentation](https://docs.pinokio.computer/) for general Pinokio help
- **NVIDIA Support**: Check NVIDIA's documentation for model-specific issues

---

**Made with ❤️ for the AI community**