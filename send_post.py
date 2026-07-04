import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

POSTS_FILE = Path("data/hikam.txt")
STATE_FILE = Path("state.json")


def load_posts():
    if not POSTS_FILE.exists():
        raise FileNotFoundError(f"Missing posts file: {POSTS_FILE}")

    text = POSTS_FILE.read_text(encoding="utf-8").strip()

    # The uploaded file uses lines like --- between posts.
    posts = [p.strip() for p in re.split(r"\n\s*---\s*\n", text) if p.strip()]

    if not posts:
        raise ValueError("No posts found in data/hikam.txt")

    return posts


def load_state():
    if not STATE_FILE.exists():
        return {"next_index": 0}

    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if not isinstance(state.get("next_index"), int):
            return {"next_index": 0}
        return state
    except json.JSONDecodeError:
        return {"next_index": 0}


def save_state(next_index):
    STATE_FILE.write_text(
        json.dumps({"next_index": next_index}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Telegram message text limit is 4096 characters.
    # If a post is longer, split it safely into parts.
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)]

    for chunk in chunks:
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": "true",
        }).encode("utf-8")

        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            result = json.loads(body)
            if not result.get("ok"):
                raise RuntimeError(body)


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN secret")
    if not chat_id:
        raise RuntimeError("Missing TELEGRAM_CHAT_ID secret")

    posts = load_posts()
    state = load_state()

    index = state["next_index"] % len(posts)
    post = posts[index]

    send_telegram_message(token, chat_id, post)

    next_index = (index + 1) % len(posts)
    save_state(next_index)

    print(f"Sent post {index + 1}/{len(posts)}. Next index: {next_index}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
