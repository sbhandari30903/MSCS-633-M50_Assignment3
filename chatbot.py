#!/usr/bin/env python
"""
chatbot.py — Single-file Django + ChatterBot terminal client.

Why Django here?
- The assignment asks for Django; we configure Django *programmatically* so we don't need a project tree.
- We don't create views/models—Django just provides a clean, standard runtime env.

Usage:
    python chatbot.py --fresh-train   # one-time (safe to re-run)
    python chatbot.py                 # chat session

Dependencies:
    pip install "Django>=4.2,<5.1" ChatterBot==1.2.8 chatterbot-corpus==1.2.2 "sqlalchemy<2.0"
"""

from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

# --- 1) Minimal Django bootstrap (no project tree required) -------------------
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent
# Keep the bot's learned data separate so it's easy to reset
BOT_DB_PATH = BASE_DIR / "bot_db.sqlite3"
DJANGO_DB_PATH = BASE_DIR / "db.sqlite3"

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="dev-not-for-production",
        ALLOWED_HOSTS=[],
        INSTALLED_APPS=[],  # No apps needed; we aren't using ORM/models
        MIDDLEWARE=[],
        ROOT_URLCONF=__name__,  # no urls, but Django wants a string
        TEMPLATES=[],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": str(DJANGO_DB_PATH),
            }
        },
        TIME_ZONE="UTC",
        USE_TZ=True,
    )

# Set up Django (no migrations/models required)
import django  # noqa: E402
django.setup()

# --- 2) ChatterBot setup ------------------------------------------------------
from chatterbot import ChatBot  # noqa: E402
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer  # noqa: E402


def build_bot() -> ChatBot:
    """
    Create a ChatBot with a local SQLite store so it can remember between runs.
    """
    return ChatBot(
        "TerminalBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{BOT_DB_PATH}",
        read_only=False,
        logic_adapters=[
            {"import_path": "chatterbot.logic.BestMatch"},
            {"import_path": "chatterbot.logic.TimeLogicAdapter"},
            {"import_path": "chatterbot.logic.MathematicalEvaluation"},
        ],
    )


def initial_train(bot: ChatBot) -> None:
    """
    Seed the bot with a small English corpus + a tiny custom list so it has
    immediate, assignment-friendly behavior.
    Safe to re-run; the SQL store de-duplicates learned pairs.
    """
    print("[trainer] Loading English greetings & conversations corpus…")
    corpus_trainer = ChatterBotCorpusTrainer(bot)
    corpus_trainer.train("chatterbot.corpus.english.greetings")
    corpus_trainer.train("chatterbot.corpus.english.conversations")

    print("[trainer] Adding minimal custom pairs…")
    custom = ListTrainer(bot)
    custom.train(
        [
            "Who built you?",
            "I was set up with Django and ChatterBot.",
            "What is this assignment?",
            "A terminal chat client powered by a machine-learning dialog engine.",
            "How do I exit?",
            "Type /quit and press Enter.",
        ]
    )
    print("[trainer] Training complete.\n")


# --- 3) Simple terminal REPL --------------------------------------------------
def chat_loop(bot: ChatBot) -> None:
    print("Starting TerminalBot. Type your message; use /quit to exit.\n")
    while True:
        try:
            user_text = input("user: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbot: Goodbye!")
            break

        if not user_text:
            continue
        if user_text.lower() in {"/quit", "quit", "exit", "/exit"}:
            print("bot: Goodbye!")
            break

        response = bot.get_response(user_text)
        print(f"bot: {response}")


# --- 4) CLI -------------------------------------------------------------------
def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Single-file Django + ChatterBot terminal client")
    p.add_argument(
        "--fresh-train",
        action="store_true",
        help="Run initial corpus + custom training before chatting (safe to re-run).",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    print("Initializing bot…")
    bot = build_bot()

    if args.fresh_train:
        initial_train(bot)

    chat_loop(bot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
