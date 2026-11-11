"""Project 4: Caption every image in a folder and save the results to a CSV.

Already-captioned files are skipped, so you can stop and resume safely.

Examples:
    python batch_caption.py ./photos
    python batch_caption.py ./photos --out captions.csv --prompt "Write a short alt-text for this image."
"""

import argparse
import csv
from pathlib import Path

from common import IMAGE_EXTS, VISION_MODEL, ask_about_image, ensure_model

DEFAULT_PROMPT = "Write one short sentence that captions this image."


def load_done(csv_path: Path) -> set:
    if not csv_path.exists():
        return set()
    with open(csv_path, newline="", encoding="utf-8") as f:
        return {row["filename"] for row in csv.DictReader(f)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Caption all images in a folder.")
    parser.add_argument("folder", help="Folder containing images")
    parser.add_argument("--out", default="captions.csv", help="CSV file to write (default: captions.csv)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt used for each image")
    parser.add_argument("--model", default=VISION_MODEL, help=f"Vision model (default: {VISION_MODEL})")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        raise SystemExit(f"Folder not found: {folder}")

    images = sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS)
    if not images:
        raise SystemExit(f"No images found in {folder}")

    ensure_model(args.model)

    out = Path(args.out)
    done = load_done(out)
    is_new = not out.exists()

    with open(out, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "caption"])
        if is_new:
            writer.writeheader()

        for i, img in enumerate(images, start=1):
            if img.name in done:
                print(f"[{i}/{len(images)}] {img.name}: skipped (already captioned)")
                continue
            try:
                caption = ask_about_image(str(img), args.prompt, model=args.model).strip().replace("\n", " ")
            except Exception as exc:  # noqa: BLE001
                print(f"[{i}/{len(images)}] {img.name}: failed ({exc})")
                continue
            writer.writerow({"filename": img.name, "caption": caption})
            f.flush()
            print(f"[{i}/{len(images)}] {img.name}: {caption}")

    print(f"\nDone. Captions saved to {out}")


if __name__ == "__main__":
    main()
