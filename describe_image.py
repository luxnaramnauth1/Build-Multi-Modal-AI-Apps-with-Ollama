"""Project 1: Describe an image (or ask a question about it).

Examples:
    python describe_image.py photo.jpg
    python describe_image.py photo.jpg --prompt "How many people are in this picture?"
"""

import argparse

from common import VISION_MODEL, ask_about_image, check_image, ensure_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Describe an image with a local vision model.")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument(
        "--prompt",
        default="Describe this image in detail.",
        help="What to ask about the image",
    )
    parser.add_argument("--model", default=VISION_MODEL, help=f"Vision model (default: {VISION_MODEL})")
    args = parser.parse_args()

    image = check_image(args.image)
    ensure_model(args.model)
    ask_about_image(image, args.prompt, model=args.model, stream=True)


if __name__ == "__main__":
    main()
