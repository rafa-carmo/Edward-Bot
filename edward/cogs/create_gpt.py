import discord
from discord import app_commands, ui
from discord.ext import commands

from edward.services.gpt import getResponse


class CreateGptModal(ui.Modal, title="Criar uma thread para GPT"):
    name = ui.TextInput(label="Nome da thread")
    question = ui.TextInput(label="Pergunta", style=discord.TextStyle.paragraph)

    def __init__(self, bot: commands.bot):
        self.bot = bot
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = interaction.channel_id
        if not guild_id:
            await interaction.response.send_message("Erro, tente novamente")
            return
        guild = self.bot.get_channel(guild_id)

        thread = await guild.create_thread(
            name=f"GPT - {self.name}",
            auto_archive_duration=4320,
            type=discord.ChannelType.public_thread,
        )

        firstQuestion = await thread.send(f"Questão inicial: {self.question}")

        response = getResponse(str(self.question))
        await firstQuestion.reply(response)
        await interaction.response.send_message(f"Thread criada: {thread.mention}")
        return


class GPTChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="create-chat", description="Add new chat from gpt")
    async def create_chat(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(CreateGptModal(self.bot))
        return
        # guild_id = interaction.channel_id
        # if(not guild_id):
        #     await interaction.response.send_message("Erro, tente novamente")
        #     return

        # guild = self.bot.get_channel(guild_id)
        # thread = await guild.create_thread(name=f"GPT - {title}", auto_archive_duration=4320, type=discord.ChannelType.public_thread)
        # return await interaction.response.send_message(f"Thread criada: {thread.mention}")


async def setup(bot: commands.Bot):
    await bot.add_cog(GPTChat(bot))
    print("✔ - cog add create gpt")
