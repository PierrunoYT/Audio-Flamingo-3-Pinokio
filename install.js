module.exports = {
  run: [
    // Install PyTorch with CUDA support
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",
          path: ".",
        }
      }
    },
    // Install requirements
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: ".",
        message: [
          "uv pip install -r requirements.txt"
        ]
      }
    },
  ]
}
