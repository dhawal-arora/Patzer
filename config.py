import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LICHESS_TOKEN = os.getenv("LICHESS_TOKEN", "")

CHESSCOM_HEADERS = {"User-Agent": "patzer-bot"}

COLOR_LICHESS = 0x00FF00
COLOR_CHESSCOM = 15548997
