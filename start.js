module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        env: {
          GRADIO_SERVER_PORT: "{{port}}",
        },
        message: [
          "python app.py",
        ],
        on: [{
          event: "/(http:\\/\\/[0-9.:]+)/",
          done: true,
        }],
      },
    },
    {
      method: "local.set",
      params: {
        url: "{{input.event[1]}}",
      },
    },
  ],
}
