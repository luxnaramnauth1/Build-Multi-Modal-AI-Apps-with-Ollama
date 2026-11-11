# Multi-Modal AI Mini-Projects with Ollama

Four small command-line projects that send images to a local vision model through [Ollama](https://ollama.com).
Everything runs on your own machine: no API keys, no cloud.

## Projects

| Script | What it does |
| --- | --- |
| `describe_image.py` | Describe an image or ask a question about it (streams the answer) |
| `chat_with_images.py` | Terminal chat where you can attach images with `/image path` and ask follow-ups |
| `extract_text.py` | Read text or specific fields from an image and return clean JSON |
| `batch_caption.py` | Caption every image in a folder and save a CSV (resumable) |
| `common.py` | Shared helpers (model check, image validation, the Ollama call) |

## Setup

1. Install Ollama from https://ollama.com and make sure it is running.
2. Pull a vision model (about 4 GB for the default):

   ```bash
   ollama pull llava
   ```

3. Put all the files in one folder, then install the Python client:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

To use a different vision model, set an environment variable or pass `--model`:

```bash
ollama pull gemma3:4b
export OLLAMA_VISION_MODEL=gemma3:4b      # Windows (PowerShell): $env:OLLAMA_VISION_MODEL="gemma3:4b"
```

## Usage

```bash
# 1. Describe an image or ask about it
python describe_image.py photo.jpg
python describe_image.py photo.jpg --prompt "What colours dominate this picture?"

# 2. Chat with images
python chat_with_images.py
#   You: /image photo.jpg
#   You: What is in this photo?
#   You: And what time of day does it look like?

# 3. Extract structured data
python extract_text.py receipt.jpg
python extract_text.py receipt.jpg --fields vendor date total --out receipt.json

# 4. Caption a whole folder
python batch_caption.py ./photos --out captions.csv
```

## How it works

Ollama's chat API accepts an `images` list on any user message. The scripts build messages like:

```python
{"role": "user", "content": "Describe this image.", "images": ["photo.jpg"]}
```

and call `ollama.chat(model=..., messages=[...])`. Streaming uses `stream=True`, and structured output
uses `format="json"` so the reply can be parsed with `json.loads`.

## Troubleshooting

- **"Cannot reach Ollama"**: start the app, or run `ollama serve` in another terminal.
- **"Model is not installed"**: run `ollama pull <model>` using the name shown in the message.
- **Slow replies**: vision models are heavy. Try a smaller model, and close other GPU-hungry apps.
- **Invalid JSON from `extract_text.py`**: small models sometimes slip. Re-run, or try a larger model.

## Ideas to extend

- Wrap `ask_about_image` in a Gradio or Streamlit page for a drag-and-drop UI.
- Sort photos into folders by asking the model for a one-word category.
- Combine with a text model to summarise a folder of captions.
