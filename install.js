module.exports = {
  run: [
    // Clone the Audio Flamingo 3 repository from HuggingFace
    {
      method: "shell.run",
      params: {
        message: "git clone https://huggingface.co/spaces/PierrunoYT/audio-flamingo-3 app"
      }
    },
    // Delete this step if your project does not use torch
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",                // Edit this to customize the venv folder path
          path: "app",                // Use same path as main install to ensure single environment
          // xformers: true   // uncomment this line if your project requires xformers
          // triton: true   // Triton disabled on Windows for stability (use on Linux only)
          // sageattention: true   // uncomment this line if your project requires sageattention
        }
      }
    },
    // Install DeepSpeed - Windows needs special wheel, Linux/macOS use pip
    {
      when: "{{platform === 'win32'}}",
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install https://github.com/6Morpheus6/deepspeed-windows-wheels/releases/download/v0.17.5/deepspeed-0.17.5+e1560d84-2.8torch+cu128-cp310-cp310-win_amd64.whl"
      }
    },
    {
      when: "{{platform !== 'win32'}}",
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "uv pip install deepspeed"
      }
    },
    // Install other requirements
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "uv pip install -r ../requirements.txt"
        ]
      }
    },
  ]
}
