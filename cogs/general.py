import discord
from discord import app_commands
from discord.ext import commands

from config import COLOR_LICHESS
from views import LinkButtons


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="List of all available commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Patzer Bot",
            description=(
                "Your One-Stop Chess Data Retrieval Tool\n\n"
                "**Lichess:**\n"
                "`/score` — Score between two players\n"
                "`/userinfo` — Player profile\n"
                "`/variantratings` — Player variant ratings\n"
                "`/gamegif` — GIF of a game\n"
                "`/swissrankings` — Swiss tournament results\n"
                "`/arenarankings` — Arena tournament results\n"
                "`/teamrankings` — Team arena results\n"
                "`/arenabyuser` — Upcoming arenas created by a user\n"
                "`/downloadgames` — Download a player's games in PGN\n\n"
                "**Chess.com:**\n"
                "`/chesscomclub` — Club details\n"
                "`/chesscomuserinfo` — Player profile\n"
                "`/chesscomdownload` — Download games in PGN\n"
                "`/chesscomleaderboard` — All-time leaderboards"
            ),
            color=COLOR_LICHESS,
        )
        buttons = LinkButtons()
        buttons.add_item(discord.ui.Button(
            label="Invite Bot",
            style=discord.ButtonStyle.link,
            url="https://discord.com/api/oauth2/authorize?client_id=803120439550279690&permissions=519233&scope=bot",
        ))
        buttons.add_item(discord.ui.Button(
            label="Support Server",
            style=discord.ButtonStyle.link,
            url="https://discord.gg/cdfUp5Zqs7",
        ))
        buttons.add_item(discord.ui.Button(
            label="Write a Review",
            style=discord.ButtonStyle.link,
            url="https://top.gg/bot/803120439550279690",
        ))
        await interaction.response.send_message(embed=embed, view=buttons)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
