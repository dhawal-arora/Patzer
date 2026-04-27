import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import CHESSCOM_HEADERS, COLOR_CHESSCOM
from views import LinkButtons

VALID_FORMATS = ("daily", "rapid", "blitz", "bullet", "lessons", "tactics")


class ChessCom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chesscomclub", description="Chess.com club info")
    async def chesscomclub(self, interaction: discord.Interaction, clubname: str):
        club_id = clubname.replace(" ", "-")
        response = requests.get(f"https://api.chess.com/pub/club/{club_id}", headers=CHESSCOM_HEADERS)
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="Club not found.", color=COLOR_CHESSCOM)
            await interaction.response.send_message(embed=embed)
            return

        data = response.json()
        description = (
            f"**Club Name:** {data.get('name')}\n"
            f"**Members:** {data.get('members_count')}\n"
            f"**Visibility:** {data.get('visibility')}\n"
            f"**Location:** {data.get('location')}"
        )
        embed = discord.Embed(title="Patzer Bot", description=description, color=COLOR_CHESSCOM)
        if data.get("icon"):
            embed.set_thumbnail(url=data["icon"])
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(
            label="Join Club",
            style=discord.ButtonStyle.link,
            url=data.get("join_request"),
        ))
        await interaction.response.send_message(embed=embed, view=buttons)

    @app_commands.command(name="chesscomuserinfo", description="Chess.com player profile")
    async def chesscomuserinfo(self, interaction: discord.Interaction, username: str):
        response = requests.get(f"https://api.chess.com/pub/player/{username}", headers=CHESSCOM_HEADERS)
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="User not found.", color=COLOR_CHESSCOM)
            await interaction.response.send_message(embed=embed)
            return

        profile = response.json()
        stats = requests.get(
            f"https://api.chess.com/pub/player/{username}/stats", headers=CHESSCOM_HEADERS
        ).json()
        online = requests.get(
            f"https://api.chess.com/pub/player/{username}/is-online", headers=CHESSCOM_HEADERS
        ).json()

        description = (
            f"Username: {profile.get('username')}\n"
            f"Profile: {profile.get('url')}\n"
            f"Status: {profile.get('status')}\n"
            f"Followers: {profile.get('followers')}\n"
            f"Streamer: {profile.get('is_streamer')}\n"
            f"Online: {online.get('online')}"
        )
        embed = discord.Embed(title="Patzer Bot", description=description, color=COLOR_CHESSCOM)
        if profile.get("avatar"):
            embed.set_thumbnail(url=profile["avatar"])

        def add_time_control(label: str, key: str):
            stat = stats.get(key)
            if not stat:
                return
            value = (
                f"Rating: {stat['last']['rating']}\n"
                f"Highest: {stat['best']['rating']}\n"
                f"Best Win: {stat['best']['game']}\n"
                f"W/D/L: {stat['record']['win']}/{stat['record']['draw']}/{stat['record']['loss']}"
            )
            embed.add_field(name=label, value=value, inline=True)

        add_time_control("Bullet", "chess_bullet")
        add_time_control("Blitz", "chess_blitz")
        add_time_control("Rapid", "chess_rapid")

        if stats.get("tactics"):
            embed.add_field(
                name="Tactics",
                value=(
                    f"Highest: {stats['tactics']['highest']['rating']}\n"
                    f"Lowest: {stats['tactics']['lowest']['rating']}"
                ),
                inline=True,
            )
        if stats.get("puzzle_rush"):
            embed.add_field(
                name="Puzzle Rush",
                value=(
                    f"Attempts: {stats['puzzle_rush']['best']['total_attempts']}\n"
                    f"Score: {stats['puzzle_rush']['best']['score']}"
                ),
                inline=True,
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="chesscomdownload", description="Download Chess.com games of a player in PGN")
    async def chesscomdownload(
        self,
        interaction: discord.Interaction,
        username: str,
        year: str,
        monthnumber: str,
    ):
        response = requests.get(f"https://api.chess.com/pub/player/{username}", headers=CHESSCOM_HEADERS)
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="User not found.", color=COLOR_CHESSCOM)
            await interaction.response.send_message(embed=embed)
            return

        url = f"https://api.chess.com/pub/player/{username}/games/{year}/{monthnumber}/pgn"
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(label="Download PGN", style=discord.ButtonStyle.link, url=url))
        embed = discord.Embed(
            title="Patzer Bot",
            description=f"Click below to download **{username}**'s games from **{monthnumber}/{year}** in PGN",
            color=COLOR_CHESSCOM,
        )
        embed.add_field(
            name="​",
            value="Note: If no games were played in this period, the downloaded file will be empty.",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, view=buttons)

    @app_commands.command(
        name="chesscomleaderboard",
        description="Chess.com leaderboard (formats: daily, rapid, blitz, bullet, lessons, tactics)",
    )
    async def chesscomleaderboard(self, interaction: discord.Interaction, gameformat: str):
        if gameformat not in VALID_FORMATS:
            embed = discord.Embed(
                title="Patzer Bot",
                description=f"Invalid format `{gameformat}`. Choose from: {', '.join(VALID_FORMATS)}",
                color=COLOR_CHESSCOM,
            )
            await interaction.response.send_message(embed=embed)
            return

        api_key = "live_" + gameformat if gameformat in ("rapid", "blitz", "bullet") else gameformat
        data = requests.get("https://api.chess.com/pub/leaderboards", headers=CHESSCOM_HEADERS).json()

        embed = discord.Embed(
            title="Patzer Bot",
            description=f"{gameformat.title()} Leaderboard",
            color=COLOR_CHESSCOM,
        )
        lines = ""
        for i, player in enumerate(data.get(api_key, [])[:10], start=1):
            username = player["username"]
            url = player["url"]
            title = f"{player['title']} " if "title" in player else ""
            lines += f"{i}. {title}[{username}]({url})\n"

        embed.add_field(name="​", value=lines or "No data available.", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ChessCom(bot))
