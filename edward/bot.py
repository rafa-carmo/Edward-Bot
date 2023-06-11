import discord
from discord.ext import commands

from edward.config import BASE_DIR, Ini
from edward.services.gpt import getResponse

COGS_DIR = BASE_DIR / "cogs"


class Bot(commands.Bot):
    """
    Classe para iniciar o bot.

    Extende de [discord.ext.commands.Bot](https://discordpy.readthedocs.io/en/stable/ext/commands/index.html)
    Args:
        servers: Lista opcional de servidores, vem diretamente do arquivo config.ini, deixando em branco ira aplicar a todos os servidores em que este bot for adicionado

    """

    def __init__(self, config: Ini, servers: list[int] = []):
        intents = discord.Intents.default()
        intents.message_content = True
        self.config = config
        self.sync = False
        self.servers = (
            [discord.Object(id=server) for server in servers]
            if len(servers) > 0
            else None
        )
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        """
        Função setup para forçar a sincronização de todos os commandos.
        """
        if not self.sync:
            for command in COGS_DIR.glob("*.py"):
                if command.name != "__init__.py":
                    await self.load_extension(f"edward.cogs.{command.name[:-3]}")

            await self.tree.sync(guild=self.servers)

        print("BOT Started")

    async def on_message(self, message: discord.Message):
        """
        Função para interceptar todas as mensagens que o bot tem acesso para aplicar os comandos.
        """
        if message.author == self.user:
            return
        if message.author.id == 966359640029933588:
            ctx = await self.get_context(message)
            if ctx.valid:
                await self.invoke(ctx)

        if not hasattr(message.channel, "threads"):
            if "GPT" in message.channel.name:
                if message.content.isprintable:
                    await message.reply(getResponse(message.content))
                    return

        await self.process_commands(message)


def start():
    config = Ini()
    bot = Bot(config=config)
    bot.run(token=config.token)


if __name__ == "__main__":
    start()
