import json

import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import COLOR_LICHESS
from views import GifView, LinkButtons


def _perf_field(perfs: dict, key: str) -> str:
    p = perfs[key]
    return f"Games: {p['games']}\nRating: {p['rating']}\n\n"


class Lichess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="score", description="Score between two Lichess players")
    async def score(self, interaction: discord.Interaction, player1: str, player2: str):
        if player1.lower() == player2.lower():
            embed = discord.Embed(
                title="Patzer Bot",
                description="Same player entered twice, please try again.",
                color=COLOR_LICHESS,
            )
        else:
            data = requests.get(
                f"https://lichess.org/api/crosstable/{player1}/{player2}"
            ).json()
            users = data.get("users", {})
            if not users or data.get("nbGames", 0) == 0:
                embed = discord.Embed(
                    title="Patzer Bot",
                    description="These players have never played each other.",
                    color=COLOR_LICHESS,
                )
            else:
                names = list(users.keys())
                scores = list(users.values())
                description = (
                    f"Current Scores:\n\n"
                    f"**{names[0]}** {scores[0]}–{scores[1]} **{names[1]}**\n\n"
                    f"Total Games Played: {data['nbGames']}"
                )
                embed = discord.Embed(title="Patzer Bot", description=description, color=COLOR_LICHESS)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Lichess player profile")
    async def userinfo(self, interaction: discord.Interaction, username: str):
        data = requests.get(f"https://lichess.org/api/user/{username}").json()
        if data.get("error") == "Not found":
            embed = discord.Embed(title="Patzer Bot", description="User not found.", color=COLOR_LICHESS)
            await interaction.response.send_message(embed=embed)
            return

        count = data.get("count", {})
        description = (
            f"Username: {data.get('username')}\n"
            f"Title: {data.get('title')}\n"
            f"Lichess Patron: {data.get('patron')}\n"
            f"Profile Link: {data.get('url')}\n"
            f"Online: {data.get('online')}\n\n"
            f"All Games: {count.get('all')}\n"
            f"Rated: {count.get('rated')}\n"
            f"Wins: {count.get('win')}\n"
            f"Draws: {count.get('draw')}\n"
            f"Losses: {count.get('loss')}\n"
            f"Playing Now: {count.get('playing')}"
        )
        embed = discord.Embed(title="Patzer Bot", description=description, color=COLOR_LICHESS)

        perfs = data.get("perfs", {})
        standard_formats = {
            "ultraBullet": "UltraBullet",
            "bullet": "Bullet",
            "blitz": "Blitz",
            "rapid": "Rapid",
            "classical": "Classical",
            "correspondence": "Correspondence",
        }
        for key, label in standard_formats.items():
            if key in perfs:
                embed.add_field(name=label, value=_perf_field(perfs, key), inline=True)

        if "puzzle" in perfs:
            embed.add_field(
                name="Puzzles",
                value=f"Puzzles: {perfs['puzzle']['games']}\nRating: {perfs['puzzle']['rating']}\n\n",
                inline=True,
            )
        if "storm" in perfs:
            embed.add_field(
                name="Puzzle Storm",
                value=f"Runs: {perfs['storm']['runs']}\nScore: {perfs['storm']['score']}",
                inline=True,
            )
        embed.set_footer(text="For variant ratings use /variantratings")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="variantratings", description="Lichess variant ratings of a player")
    async def variantratings(self, interaction: discord.Interaction, username: str):
        data = requests.get(f"https://lichess.org/api/user/{username}").json()
        if data.get("error") == "Not found":
            embed = discord.Embed(title="Patzer Bot", description="User not found.", color=COLOR_LICHESS)
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="Patzer Bot",
            description="User variant ratings (if any)",
            color=COLOR_LICHESS,
        )
        perfs = data.get("perfs", {})
        variants = {
            "chess960": "Chess960",
            "crazyhouse": "Crazyhouse",
            "antichess": "AntiChess",
            "atomic": "Atomic",
            "horde": "Horde",
            "kingOfTheHill": "King of the Hill",
            "racingKings": "Racing Kings",
            "threeCheck": "3-Check",
        }
        for key, label in variants.items():
            if key in perfs:
                embed.add_field(name=label, value=_perf_field(perfs, key), inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gamegif", description="Generate a GIF of a Lichess game")
    async def gamegif(self, interaction: discord.Interaction, gamelink: str):
        game_id = (
            gamelink
            .replace("https://lichess.org/", "")
            .replace("/black", "")
            .replace("/white", "")
            .split("?")[0]
            .strip("/")
        )
        response = requests.get(f"https://lichess.org/game/export/gif/{game_id}.gif")
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="Game not found.", color=COLOR_LICHESS)
            await interaction.response.send_message(embed=embed)
        else:
            gif_url = f"https://lichess.org/game/export/gif/{game_id}.gif"
            await interaction.response.send_message(gif_url, view=GifView(game_id))

    @app_commands.command(
        name="swissrankings",
        description="Lichess swiss tournament: top 10 rankings, game and TRF downloads",
    )
    async def swissrankings(self, interaction: discord.Interaction, tournamentlink: str):
        await interaction.response.defer()
        tournament_id = tournamentlink.replace("https://lichess.org/swiss/", "")
        response = requests.get(f"https://lichess.org/api/swiss/{tournament_id}/results")
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="Swiss tournament not found.", color=COLOR_LICHESS)
            await interaction.followup.send(embed=embed)
            return

        embed = discord.Embed(
            title="Patzer Bot",
            description="Swiss Tournament Database\n​",
            color=COLOR_LICHESS,
        )
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(
            label="Download TRF",
            style=discord.ButtonStyle.link,
            url=f"https://lichess.org/swiss/{tournament_id}.trf",
        ))
        buttons.add_item(discord.ui.Button(
            label="Download Games",
            style=discord.ButtonStyle.link,
            url=f"https://lichess.org/api/swiss/{tournament_id}/games",
        ))

        display = ""
        for i, line in enumerate(response.text.strip().split("\n")):
            if i >= 10:
                break
            entry = json.loads(line)
            title = f"{entry['title']} " if entry.get("title") else ""
            display += (
                f"{entry['rank']}. {title}{entry['username']} "
                f"({entry['rating']}) Performance: {entry.get('performance')}\n"
            )

        embed.add_field(name="Top 10:", value=display, inline=False)
        await interaction.followup.send(embed=embed, view=buttons)

    @app_commands.command(
        name="arenarankings",
        description="Lichess arena tournament: top 10 rankings and game downloads",
    )
    async def arenarankings(self, interaction: discord.Interaction, tournamentlink: str):
        await interaction.response.defer()
        tournament_id = tournamentlink.replace("https://lichess.org/tournament/", "")
        response = requests.get(f"https://lichess.org/api/tournament/{tournament_id}/results")
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="Arena tournament not found.", color=COLOR_LICHESS)
            await interaction.followup.send(embed=embed)
            return

        embed = discord.Embed(
            title="Patzer Bot",
            description="Arena Tournament Database\n​",
            color=COLOR_LICHESS,
        )
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(
            label="Download Games",
            style=discord.ButtonStyle.link,
            url=f"https://lichess.org/api/tournament/{tournament_id}/games",
        ))

        display = ""
        for i, line in enumerate(response.text.strip().split("\n")):
            if i >= 10:
                break
            entry = json.loads(line)
            title = f"{entry['title']} " if entry.get("title") else ""
            display += (
                f"{entry['rank']}. {title}{entry['username']} ({entry['rating']})\n"
                f"**Points:** {entry.get('score')}  **Performance:** {entry.get('performance')}\n\n"
            )

        embed.add_field(name="Top 10:", value=display, inline=False)
        await interaction.followup.send(embed=embed, view=buttons)

    @app_commands.command(
        name="teamrankings",
        description="Lichess team arena tournament: top 10 rankings and game downloads",
    )
    async def teamrankings(self, interaction: discord.Interaction, tournamentlink: str):
        await interaction.response.defer()
        tournament_id = tournamentlink.replace("https://lichess.org/tournament/", "")
        response = requests.get(f"https://lichess.org/api/tournament/{tournament_id}/teams")
        if response.status_code == 404:
            embed = discord.Embed(
                title="Patzer Bot",
                description="Team arena tournament not found.",
                color=COLOR_LICHESS,
            )
            await interaction.followup.send(embed=embed)
            return

        embed = discord.Embed(
            title="Patzer Bot",
            description="Team Arena Tournament Database\n​",
            color=COLOR_LICHESS,
        )
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(
            label="Download Games",
            style=discord.ButtonStyle.link,
            url=f"https://lichess.org/api/tournament/{tournament_id}/games",
        ))

        teams = response.json().get("teams", [])
        display = ""
        for team in teams[:10]:
            display += f"{team['rank']}. Team {team['id']} (Score: {team['score']})\n"

        embed.add_field(name="Top 10:", value=display, inline=False)
        await interaction.followup.send(embed=embed, view=buttons)

    @app_commands.command(
        name="arenabyuser",
        description="Upcoming Lichess arena tournaments created by a user",
    )
    async def arenabyuser(self, interaction: discord.Interaction, username: str):
        response = requests.get(f"https://lichess.org/api/user/{username}/tournament/created")
        if response.status_code == 404:
            embed = discord.Embed(title="Patzer Bot", description="User not found.", color=COLOR_LICHESS)
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="Patzer Bot",
            description="Tournaments created by this user:\n",
            color=COLOR_LICHESS,
        )
        for line in response.text.strip().split("\n"):
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("status") == 30:
                continue
            clock = entry.get("clock", {})
            limit = clock.get("limit", 0)
            time_control = (
                f"{limit}sec+{clock.get('increment', 0)}"
                if limit < 60
                else f"{limit // 60}+{clock.get('increment', 0)}"
            )
            link = f"https://lichess.org/tournament/{entry['id']}"
            value = f"{entry['fullName']}\n{time_control} for {entry.get('minutes')} min\n{link}"
            embed.add_field(name="​", value=value, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="downloadgames",
        description="Download all Lichess games of a player in PGN",
    )
    async def downloadgames(self, interaction: discord.Interaction, username: str):
        url = f"https://lichess.org/api/games/user/{username}"
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(label="Download PGN", style=discord.ButtonStyle.link, url=url))
        embed = discord.Embed(
            title="Patzer Bot",
            description=f"Click below to download all games of **{username}** in PGN\nSpeed: ~20 games per second",
            color=COLOR_LICHESS,
        )
        embed.add_field(
            name="​",
            value="Note: If the user does not exist or has no games, the downloaded file will be empty.",
            inline=False,
        )
        await interaction.response.send_message(embed=embed, view=buttons)


async def setup(bot: commands.Bot):
    await bot.add_cog(Lichess(bot))
