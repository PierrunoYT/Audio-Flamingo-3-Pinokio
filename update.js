module.exports = {
  run: [{
    method: "shell.run",
    params: {
      message: "git pull"
    }
  }, {
    method: "shell.run",
    params: {
      venv: "env",
      path: "app",
      message: "uv pip install -r requirements.txt --upgrade"
    }
  }, {
    // --upgrade also upgrades transitive deps, so accelerate/peft can pull the
    // default PyPI torch (CPU-only on Windows) over the GPU build; restore it.
    method: "script.start",
    params: {
      uri: "torch.js",
      params: {
        venv: "env",
        path: "app",
      }
    }
  }]
}
