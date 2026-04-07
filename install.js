module.exports = {
  run: [
    // Install PyTorch with CUDA support
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",
        }
      }
    },
    // Install requirements
    {
      method: "shell.run",
      params: {
        venv: "env",
        message: [
          "uv pip install -r app/requirements.txt"
        ]
      }
    },
  ]
}
