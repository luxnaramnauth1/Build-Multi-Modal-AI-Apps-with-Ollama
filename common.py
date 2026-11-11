"""Shared helpers for the Ollama multi-modal mini-projects."""

import os
import sys
from pathlib import Path

import ollama

# Override these with environment variables, e.g.  OLLAMA_VISION_MODEL=gemma3:4b
VISION_MODEL = os.getenv("OLLAMA_VISION_MODEL", "llava")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}


def ensure_model(model: str) -> None:
    """Exit with a friendly message if Ollama isn't running or the model is missing."""
    try:
        ollama.show(model)
    except ollama.ResponseError:
        sys.exit(f"Model '{model}' is not installed. Run:  ollama pull {model}")
    except Exception:  # noqa: BLE001
        sys.exit("Cannot reach Ollama. Make sure it is running (try:  ollama serve).")


def check_image(path: str) -> str:
    """Validate that a path points to a supported image file and return it."""
    p = Path(path).expanduser()
    if not p.is_file():
        sys.exit(f"Image not found: {p}")
    if p.suffix.lower() not in IMAGE_EXTS:
        sys.exit(f"Unsupported image type '{p.suffix}'. Use one of: {', '.join(sorted(IMAGE_EXTS))}")
    return str(p)


def ask_about_image(
    image_path: str,
    prompt: str,
    model: str = VISION_MODEL,
    stream: bool = False,
    json_mode: bool = False,
) -> str:
    """Send one image plus a prompt to a vision model and return the reply text.

    With stream=True the text is printed as it arrives (and still returned).
    """
    messages = [{"role": "user", "content": prompt, "images": [image_path]}]
    fmt = "json" if json_mode else None

    if not stream:
        response = ollama.chat(model=model, messages=messages, format=fmt)
        return response["message"]["content"]

    parts = []
    for chunk in ollama.chat(model=model, messages=messages, format=fmt, stream=True):
        text = chunk["message"]["content"]
        print(text, end="", flush=True)
        parts.append(text)
    print()
    return "".join(parts)
