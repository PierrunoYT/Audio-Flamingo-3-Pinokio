import functools
import gc
import gradio as gr
import torch
import os
import sys
import threading
from accelerate import dispatch_model, infer_auto_device_map
from accelerate.utils import get_max_memory
from transformers import AudioFlamingo3ForConditionalGeneration, AutoProcessor
from huggingface_hub import snapshot_download
from peft import PeftModel

# ---------------------------------
# MODEL SETUP
# ---------------------------------
MODEL_ID = "nvidia/audio-flamingo-3-hf"

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

# bf16 halves memory versus fp32 (~15GB instead of ~30GB for 7B params), which
# matters most on CPU and Apple Silicon where the model shares system RAM.
# Set AF3_DTYPE=float32 to trade that memory for full precision.
dtype = torch.float32 if os.environ.get("AF3_DTYPE") == "float32" else torch.bfloat16

# "auto" lets accelerate spread the model over GPU and CPU on CUDA; for MPS
# and CPU it just means "put everything on that one device".
device_map = "auto" if device == "cuda" else device

print(f"Loading Audio Flamingo 3 on {device} ({dtype})...")

try:
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model_single = AudioFlamingo3ForConditionalGeneration.from_pretrained(
        MODEL_ID, dtype=dtype, device_map=device_map
    )
except Exception as e:
    print(f"FATAL: Failed to load Audio Flamingo 3 model: {e}")
    print(
        "If this model is gated on Hugging Face, run 'hf auth login' "
        "(or set the HF_TOKEN environment variable) inside the app's env, then try again."
    )
    sys.exit(1)

print("Model loaded successfully!")


def free_memory():
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()
    elif device == "mps":
        torch.mps.empty_cache()


def input_device(model):
    """Device to put inputs on before generate().

    model.device is the device of the first parameter, and when accelerate
    offloads that parameter to CPU/disk it is a placeholder on "meta", which
    inputs cannot be moved to. accelerate's hooks move activations between
    devices themselves, so the first real accelerator in the map is enough.
    """
    device_map = getattr(model, "hf_device_map", None)
    if device_map:
        for d in device_map.values():
            if d not in ("cpu", "disk"):
                return torch.device(f"cuda:{d}" if isinstance(d, int) else d)
        return torch.device("cpu")
    return model.device


# The Think model is a second full copy of the 7B weights, so it is loaded on
# first use rather than at startup: that keeps the base model usable on GPUs
# that cannot hold both copies, and skips the download/load entirely for users
# who never open the Think tab.
model_think = None
_think_lock = threading.Lock()


def _load_think_model(local_path, non_lora_path):
    # Build the model fully in CPU RAM first. With device_map="auto" any
    # layers that do not fit on the GPU become "meta" placeholders, and
    # load_state_dict() on those fails with "Cannot copy out of meta tensor".
    model = AudioFlamingo3ForConditionalGeneration.from_pretrained(
        MODEL_ID, dtype=dtype
    )
    non_lora_trainables = torch.load(
        non_lora_path, map_location="cpu", weights_only=True
    )
    model.load_state_dict(non_lora_trainables, strict=False)
    del non_lora_trainables

    # Folding the LoRA weights into the base weights gives a plain model that
    # accelerate can dispatch and that generates as fast as the base model.
    model = PeftModel.from_pretrained(model, local_path, subfolder="think")
    model = model.merge_and_unload()

    if device != "cuda":
        return model.to(device)

    # GPU budgets come from the memory free now, i.e. after the base model,
    # minus headroom for activations during generate(). The weights are
    # already in CPU RAM, so layers left there cost nothing extra and the
    # CPU budget must count them, or accelerate would spill to disk.
    max_memory = {
        k: int(v * 0.9) if k != "cpu" else v
        for k, v in get_max_memory().items()
    }
    max_memory["cpu"] = max_memory.get("cpu", 0) + model.get_memory_footprint()
    think_map = infer_auto_device_map(
        model,
        max_memory=max_memory,
        no_split_module_classes=model._get_no_split_modules("auto"),
        dtype=dtype,
    )
    return dispatch_model(model, device_map=think_map)


def get_think_model():
    global model_think
    if model_think is not None:
        return model_think

    with _think_lock:
        if model_think is None:
            print("Checking for Think LoRA adapter...")
            local_path = snapshot_download(MODEL_ID)
            non_lora_path = os.path.join(local_path, "think", "non_lora_trainables.bin")

            if os.path.exists(non_lora_path):
                print("Loading Think model with LoRA adapters...")
                error = None
                try:
                    model_think = _load_think_model(local_path, non_lora_path)
                except Exception as e:
                    error = f"Failed to load the Think model: {e}"
                # Freed outside the except block: the active exception's
                # traceback keeps the half-loaded model alive until then.
                free_memory()
                if error:
                    raise RuntimeError(error)
                print("Think model loaded successfully.")
            else:
                print("Warning: Think LoRA weights not found, using base model for think mode.")
                model_think = model_single

    return model_think


# ---------------------------------
# INFERENCE FUNCTIONS
# ---------------------------------
def _generate(model, inputs, max_new_tokens, empty_message):
    inputs = inputs.to(input_device(model), dtype=model.dtype)
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    decoded = processor.batch_decode(
        outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True
    )
    return decoded[0] if decoded else empty_message


def _handle_errors(fn):
    @functools.wraps(fn)
    def wrapper(*args):
        try:
            return fn(*args)
        except Exception as e:
            if isinstance(e, torch.OutOfMemoryError) or "out of memory" in str(e).lower():
                message = (
                    "❌ Out of memory. Try a shorter audio clip, or restart the "
                    "app to free memory used by the Think model."
                )
            else:
                message = f"❌ Error: {str(e)}"
        # Freed outside the except block: the active exception's traceback
        # keeps the failed call's tensors alive until then.
        free_memory()
        return message

    return wrapper


def _chat_inputs(audio_file, prompt_text):
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text},
                {"type": "audio", "path": audio_file},
            ],
        }
    ]
    return processor.apply_chat_template(
        conversation,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
    )


@_handle_errors
def single_turn_infer(audio_file, prompt_text):
    if audio_file is None:
        return "❌ Please upload an audio file."
    if not prompt_text or not prompt_text.strip():
        return "❌ Please enter a prompt."

    return _generate(
        model_single,
        _chat_inputs(audio_file, prompt_text),
        max_new_tokens=500,
        empty_message="No response generated.",
    )


@_handle_errors
def think_infer(audio_file, prompt_text):
    if audio_file is None:
        return "❌ Please upload an audio file."
    if not prompt_text or not prompt_text.strip():
        return "❌ Please enter a prompt."

    return _generate(
        get_think_model(),
        _chat_inputs(audio_file, prompt_text),
        max_new_tokens=1024,
        empty_message="No response generated.",
    )


@_handle_errors
def transcribe_infer(audio_file):
    if audio_file is None:
        return "❌ Please upload an audio file."

    # Up to 10 minutes of speech is ~1500+ words, well past 500 tokens;
    # generation still stops at EOS for shorter clips.
    return _generate(
        model_single,
        processor.apply_transcription_request(audio=audio_file),
        max_new_tokens=4096,
        empty_message="No transcription generated.",
    )


# ---------------------------------
# GRADIO INTERFACE
# ---------------------------------
# Gradio limits concurrency per event listener, so without a shared
# concurrency_id the three tabs could run generation (or the Think model's
# lazy load) on the GPU at the same time and exhaust VRAM.
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
                concurrency_id="gpu",
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
                concurrency_id="gpu",
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
                concurrency_id="gpu",
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
