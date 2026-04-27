import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

EXTENSIONS = [
    "cogs.general",
    "cogs.lichess",
    "cogs.chesscom",
]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["Ptz.", "ptz.", "p.", "P."], intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.wait_until_ready()
    await bot.tree.sync()
    print("Slash commands synced.")


async def main():
    async with bot:
        for ext in EXTENSIONS:
            await bot.load_extension(ext)
        await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
