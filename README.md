# Patzer Bot
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fdhawal-arora%2FPatzer&count_bg=%23FD9801&title_bg=%23270A0A&icon=&icon_color=%23A64141&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

A Discord chess bot that retrieves live data from **Lichess** and **Chess.com** via slash commands. Originally built in 2020, it ran across 75+ servers with thousands of members. Posted here for reference — the bot is no longer online.

---

## Features

**Lichess**
- Player profiles and variant ratings
- Head-to-head score between two players
- Game GIFs with board-flip button
- Swiss, Arena, and Team Arena tournament rankings
- Tournament and game downloads (PGN / TRF)
- Upcoming arenas created by a user

**Chess.com**
- Player profiles with time-control stats
- Club info
- Game downloads by month (PGN)
- Live leaderboards (Bullet, Blitz, Rapid, Daily, Tactics, Lessons)

---

## Commands

### Lichess

| Command | Description |
|---|---|
| `/score <player1> <player2>` | Head-to-head score between two players |
| `/userinfo <username>` | Player profile and standard ratings |
| `/variantratings <username>` | Variant ratings (960, Crazyhouse, etc.) |
| `/gamegif <gamelink>` | Animated GIF of a game (with flip button) |
| `/swissrankings <tournamentlink>` | Top 10 + TRF and PGN download links |
| `/arenarankings <tournamentlink>` | Top 10 + PGN download link |
| `/teamrankings <tournamentlink>` | Top 10 teams + PGN download link |
| `/arenabyuser <username>` | Upcoming arenas created by a user |
| `/downloadgames <username>` | Download all games in PGN |

### Chess.com

| Command | Description |
|---|---|
| `/chesscomuserinfo <username>` | Player profile with ratings and records |
| `/chesscomclub <clubname>` | Club details and join link |
| `/chesscomdownload <username> <year> <month>` | Download games from a specific month in PGN |
| `/chesscomleaderboard <format>` | Top 10 leaderboard — formats: `daily`, `rapid`, `blitz`, `bullet`, `lessons`, `tactics` |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/dhawal-arora/Patzer.git
cd Patzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your tokens:

```bash
cp .env.example .env
```

```env
DISCORD_TOKEN=your_discord_bot_token_here
LICHESS_TOKEN=your_lichess_api_token_here   # optional, reserved for future use
```

### 4. Run the bot

```bash
python main.py
```

---

## Project Structure

```
Patzer/
├── main.py           # Bot entry point — loads extensions and starts the bot
├── config.py         # Environment variables and shared constants
├── views.py          # Discord UI components (link buttons, GIF flip view)
├── cogs/
│   ├── general.py    # /help command
│   ├── lichess.py    # All Lichess commands
│   └── chesscom.py   # All Chess.com commands
├── legacy/
│   └── advertising.py  # Original prefix-based advertising commands (archived)
├── .env.example
├── requirements.txt
└── README.md
```

---

## Notes

- Slash commands are synced globally on startup — changes may take up to an hour to appear in Discord.
- The Chess.com API is public and requires no authentication. The Lichess API key is optional for the commands currently implemented.
- HTTP calls use the `requests` library (synchronous). For a production bot under high load, these should be replaced with `aiohttp` to avoid blocking the async event loop.
- The bot was originally built with prefix commands (`p.`/`Ptz.`) and a separate event-advertising module. That legacy code is preserved in `legacy/`.
