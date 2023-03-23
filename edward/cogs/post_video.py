from enum import Enum
from urllib.parse import parse_qs, urlparse

import discord
from discord import app_commands
from discord.ext import commands


class Colors(Enum):
    javascript = 16776960
    typescript = 3447003
    php = 10181046
    other = 9807270


class AddVideo(commands.Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(name="add-video", description="Add video with info")
    @app_commands.choices(
        type=[
            app_commands.Choice(name="Frontend", value="Frontend"),
            app_commands.Choice(name="Backend", value="Backend"),
            app_commands.Choice(name="DevOps", value="DevOps"),
        ],
        language=[
            app_commands.Choice(name="Javascript", value="javascript"),
            app_commands.Choice(name="Typescript", value="typescript"),
            app_commands.Choice(name="PHP", value="php"),
            app_commands.Choice(name="Outra", value="other"),
        ],
    )
    @app_commands.describe(
        url="Url from video",
        title="Title from video",
        language="Language Subject from video",
        type="Type from video",
    )
    async def add_video(
        self,
        interaction: discord.Interaction,
        url: str,
        title: str | None,
        language: app_commands.Choice[str],
        type: app_commands.Choice[str],
    ):
        await interaction.response.send_message("...", ephemeral=True)
        parsed = urlparse(url)
        values = parse_qs(parsed.query)
        thumbnail = ""

        if "v" in values:
            thumbnail = f"https://i.ytimg.com/vi/{values['v'][0]}/maxresdefault.jpg"

        embed = discord.Embed(colour=Colors[language.value].value)
        embed.title = title
        embed.url = url
        embed.set_image(url=thumbnail)

        for text_channel in interaction.guild.text_channels:
            if "video" in text_channel.name:
                await text_channel.send(
                    content=f"Adicionado por <@{interaction.user.id}> - {url}",
                    embed=embed,
                )
        # "https://i.ytimg.com/vi/BPrNuZRnTfU/maxresdefault.jpg"

        # await interaction.guild.text_channels[0].send(embed=embed)
        ...


async def setup(bot: commands.Bot):
    await bot.add_cog(AddVideo())
    print("✔ - cog add video synced")
