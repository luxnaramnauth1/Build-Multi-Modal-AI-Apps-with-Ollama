"""Project 2: A terminal chat that can look at images.

Attach an image with  /image path/to/file.png  and it is sent with your next message.
The model remembers earlier messages, so you can ask follow-up questions.

Commands: /image <path>, /reset, /help, /exit
"""

import argparse

import ollama

from common import VISION_MODEL, check_image, ensure_model

HELP = (
    "Commands:\n"
    "  /image <path>  attach an image to your next message\n"
    "  /reset         clear the conversation\n"
    "  /help          show this help\n"
    "  /exit          quit"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat with a local vision model.")
    parser.add_argument("--model", default=VISION_MODEL, help=f"Vision model (default: {VISION_MODEL})")
    args = parser.parse_args()
    ensure_model(args.model)

    messages = []
    pending_images = []
    print(f"Multi-modal chat using '{args.model}'. Type /help for commands.\n")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not text:
            continue

        if text.startswith("/"):
            cmd, _, arg = text.partition(" ")
            cmd = cmd.lower()
            if cmd == "/exit":
                print("Goodbye!")
                break
            elif cmd == "/help":
                print(HELP)
            elif cmd == "/reset":
                messages.clear()
                pending_images.clear()
                print("Conversation cleared.")
            elif cmd == "/image":
                if not arg.strip():
                    print("Usage: /image <path>")
                else:
                    try:
                        pending_images.append(check_image(arg.strip().strip('"')))
                        print(f"Attached. ({len(pending_images)} image(s) will be sent with your next message.)")
                    except SystemExit as exc:
                        print(exc)
            else:
                print("Unknown command. Type /help.")
            continue

        message = {"role": "user", "content": text}
        if pending_images:
            message["images"] = list(pending_images)
            pending_images.clear()
        messages.append(message)

        print("Bot: ", end="", flush=True)
        reply_parts = []
        try:
            for chunk in ollama.chat(model=args.model, messages=messages, stream=True):
                piece = chunk["message"]["content"]
                print(piece, end="", flush=True)
                reply_parts.append(piece)
        except Exception as exc:  # noqa: BLE001
            messages.pop()
            print(f"\nError: {exc}\n")
            continue
        print("\n")
        messages.append({"role": "assistant", "content": "".join(reply_parts)})


if __name__ == "__main__":
    main()
