import discord


class LinkButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


class GifView(discord.ui.View):
    def __init__(self, game_id: str):
        super().__init__(timeout=300)
        self.game_id = game_id
        self.flipped = False
        # Instantiate the button directly so discord.py assigns a unique custom_id
        # per instance — class-level @ui.button decorators share one custom_id across
        # all instances, which breaks concurrent /gamegif usage.
        button = discord.ui.Button(
            label="Flip Board", style=discord.ButtonStyle.gray, emoji="🔄"
        )
        button.callback = self._flip
        self.add_item(button)

    async def _flip(self, interaction: discord.Interaction):
        self.flipped = not self.flipped
        if self.flipped:
            url = f"https://lichess.org/game/export/gif/black/{self.game_id}.gif"
        else:
            url = f"https://lichess.org/game/export/gif/{self.game_id}.gif"
        await interaction.response.edit_message(content=url)
