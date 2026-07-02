import gradio as gr
import torch
import os
import tempfile
from transformers import AudioFlamingo3ForConditionalGeneration, AutoProcessor
from huggingface_hub import snapshot_download
from peft import PeftModel

# ---------------------------------
# MODEL SETUP
# ---------------------------------
MODEL_ID = "nvidia/audio-flamingo-3-hf"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32

print(f"Loading Audio Flamingo 3 on {device}...")

processor = AutoProcessor.from_pretrained(MODEL_ID)
model_single = AudioFlamingo3ForConditionalGeneration.from_pretrained(
    MODEL_ID, dtype=dtype, device_map="auto"
)

# Check for a Think LoRA adapter before loading a second full copy of the
# base model, so we don't double VRAM usage when there is nothing to attach.
print("Checking for Think LoRA adapter...")
local_path = snapshot_download(MODEL_ID)
think_dir = os.path.join(local_path, "think")
non_lora_path = os.path.join(think_dir, "non_lora_trainables.bin")

if os.path.exists(non_lora_path):
    print("Loading Think model with LoRA adapters...")
    model_think = AudioFlamingo3ForConditionalGeneration.from_pretrained(
        MODEL_ID, dtype=dtype, device_map="auto"
    )
    non_lora_trainables = torch.load(non_lora_path, map_location="cpu", weights_only=False)
    model_think.load_state_dict(non_lora_trainables, strict=False)
    model_think = PeftModel.from_pretrained(model_think, local_path, subfolder="think")
    print("Think model loaded successfully.")
else:
    print("Warning: Think LoRA weights not found, using base model for think mode.")
    model_think = model_single

print("Models loaded successfully!")

# ---------------------------------
# INFERENCE FUNCTIONS
# ---------------------------------
def single_turn_infer(audio_file, prompt_text):
    if audio_file is None:
        return "❌ Please upload an audio file."
    if not prompt_text or not prompt_text.strip():
        return "❌ Please enter a prompt."

    try:
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "audio", "path": audio_file},
                ],
            }
        ]

        inputs = processor.apply_chat_template(
            conversation,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
        ).to(model_single.device, dtype=model_single.dtype)

        outputs = model_single.generate(**inputs, max_new_tokens=500)
        decoded = processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True
        )
        return decoded[0] if decoded else "No response generated."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def think_infer(audio_file, prompt_text):
    if audio_file is None:
        return "❌ Please upload an audio file."
    if not prompt_text or not prompt_text.strip():
        return "❌ Please enter a prompt."

    try:
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "audio", "path": audio_file},
                ],
            }
        ]

        inputs = processor.apply_chat_template(
            conversation,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
        ).to(model_think.device, dtype=model_think.dtype)

        outputs = model_think.generate(**inputs, max_new_tokens=1024)
        decoded = processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True
        )
        return decoded[0] if decoded else "No response generated."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def transcribe_infer(audio_file):
    if audio_file is None:
        return "❌ Please upload an audio file."

    try:
        inputs = processor.apply_transcription_request(audio=audio_file).to(
            model_single.device, dtype=model_single.dtype
        )
        outputs = model_single.generate(**inputs, max_new_tokens=500)
        decoded = processor.batch_decode(
            outputs[:, inputs.input_ids.shape[1]:],
            skip_special_tokens=True,
            strip_prefix=True,
        )
        return decoded[0] if decoded else "No transcription generated."
    except Exception as e:
        return f"❌ Error: {str(e)}"


# ---------------------------------
# GRADIO INTERFACE
# ---------------------------------
with gr.Blocks(
    title="Audio Flamingo 3",
) as demo:

    gr.Markdown(
        """
        # 🎧 Audio Flamingo 3
        ### Advancing Audio Intelligence with Fully Open Large Audio-Language Models
        **NVIDIA** — Speech, Sound & Music Understanding | Up to 10 minutes of audio | Chain-of-Thought Reasoning
        """
    )

    with gr.Tabs():
        # ---------------- SINGLE-TURN ----------------
        with gr.Tab("🎯 Single-Turn Inference"):
            with gr.Row():
                with gr.Column():
                    audio_input_single = gr.Audio(
                        type="filepath", label="Upload Audio"
                    )
                    prompt_input_single = gr.Textbox(
                        label="Prompt",
                        placeholder="Ask a question about the audio...",
                        lines=5,
                    )
                    btn_single = gr.Button("Generate Answer", variant="primary")
                with gr.Column():
                    output_single = gr.Textbox(label="Model Response", lines=15)

            btn_single.click(
                fn=single_turn_infer,
                inputs=[audio_input_single, prompt_input_single],
                outputs=output_single,
            )

        # ---------------- TRANSCRIPTION ----------------
        with gr.Tab("📝 Transcription"):
            with gr.Row():
                with gr.Column():
                    audio_input_transcribe = gr.Audio(
                        type="filepath", label="Upload Audio"
                    )
                    btn_transcribe = gr.Button("Transcribe", variant="primary")
                with gr.Column():
                    output_transcribe = gr.Textbox(label="Transcription", lines=15)

            btn_transcribe.click(
                fn=transcribe_infer,
                inputs=[audio_input_transcribe],
                outputs=output_transcribe,
            )

        # ---------------- THINK / LONG ----------------
        with gr.Tab("🤔 Think / Long Audio"):
            with gr.Row():
                with gr.Column():
                    audio_input_think = gr.Audio(
                        type="filepath", label="Upload Audio"
                    )
                    prompt_input_think = gr.Textbox(
                        label="Prompt",
                        placeholder="Add '\\nPlease think and reason about the input before you respond.' to enable CoT reasoning.",
                        lines=5,
                    )
                    btn_think = gr.Button("Generate Answer", variant="primary")
                with gr.Column():
                    output_think = gr.Textbox(label="Model Response", lines=20)

            btn_think.click(
                fn=think_infer,
                inputs=[audio_input_think, prompt_input_think],
                outputs=output_think,
            )

        # ---------------- ABOUT ----------------
        with gr.Tab("📄 About"):
            gr.Markdown(
                """
### 📚 Overview

**Audio Flamingo 3 (AF3)** is a fully open state-of-the-art large audio-language model by NVIDIA
that advances reasoning and understanding across speech, sound, and music.

**Key Features:**
- 🎙️ **Unified audio encoder** (AF-Whisper) for speech, sound, and music
- 🧠 **On-demand chain-of-thought reasoning** (Think mode with LoRA adapter)
- ⏱️ **Long audio support** — up to 10 minutes (30s windows × 20)
- 💬 **Multi-turn, multi-audio chat** (AF3-Chat variant)
- 🗣️ **Voice-to-voice interaction**
- 📝 **Built-in transcription** shortcut

**Model:** [`nvidia/audio-flamingo-3-hf`](https://huggingface.co/nvidia/audio-flamingo-3-hf)
**Paper:** [arXiv:2507.08128](https://arxiv.org/abs/2507.08128)
**Project:** [NVIDIA ADLR](https://research.nvidia.com/labs/adlr/AF3/)

⚠️ **Non-commercial research use only** (NVIDIA OneWay Noncommercial License)
            """
            )

    gr.Markdown("© 2025 NVIDIA | Built with Gradio + 🤗 Transformers")

# -----------------------
# Launch App
# -----------------------
if __name__ == "__main__":
    _port = int(os.environ.get("GRADIO_SERVER_PORT", os.environ.get("PORT", "7860")))
    demo.launch(
        server_name="127.0.0.1",
        server_port=_port,
        share=False,
        css=".gradio-container { max-width: 1200px !important; margin: auto !important; }",
    )
