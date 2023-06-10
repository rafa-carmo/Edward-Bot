import discord
from discord import app_commands
from discord.ext import commands


class GPTChat(commands.Cog):
    def __init__(self):
        super().__init__()
    
    @app_commands.command(name="create-chat", description="Add new chat from gpt")
    async def create_chat(self, interaction: discord.interaction, title: str) -> None:
        print(interaction)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(GPTChat())
    print("✔ - cog add create gpt")
