"""Project 3: Pull structured data out of an image (receipts, signs, forms, screenshots).

The model is asked to answer in JSON, which is then parsed and pretty-printed.

Examples:
    python extract_text.py receipt.jpg
    python extract_text.py receipt.jpg --out receipt.json
    python extract_text.py card.png --fields name company email phone
"""

import argparse
import json
import sys

from common import VISION_MODEL, ask_about_image, check_image, ensure_model

DEFAULT_PROMPT = (
    "Read all the text in this image. Respond ONLY with JSON in this shape: "
    '{"summary": "<one sentence about what the image shows>", "text": "<all visible text>"}'
)


def build_prompt(fields):
    if not fields:
        return DEFAULT_PROMPT
    keys = ", ".join(f'"{f}"' for f in fields)
    return (
        f"Extract these fields from the image: {keys}. "
        "Respond ONLY with a JSON object using exactly those keys. "
        "Use null for anything you cannot find."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text or fields from an image as JSON.")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--fields", nargs="+", help="Specific fields to extract (e.g. total date vendor)")
    parser.add_argument("--out", help="Optional path to save the JSON result")
    parser.add_argument("--model", default=VISION_MODEL, help=f"Vision model (default: {VISION_MODEL})")
    args = parser.parse_args()

    image = check_image(args.image)
    ensure_model(args.model)

    raw = ask_about_image(image, build_prompt(args.fields), model=args.model, json_mode=True)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("The model did not return valid JSON. Raw reply:\n", file=sys.stderr)
        print(raw)
        sys.exit(1)

    pretty = json.dumps(data, indent=2, ensure_ascii=False)
    print(pretty)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(pretty + "\n")
        print(f"\nSaved to {args.out}")


if __name__ == "__main__":
    main()
