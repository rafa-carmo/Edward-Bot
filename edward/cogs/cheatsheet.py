import discord
import meilisearch
from discord import app_commands
from discord.ext import commands
from slugify import slugify

from edward.bot import Bot


class CheatSheet(commands.Cog):
    """__Comando para fazer a consulta de cheatsheets__

    ## Como usar?
    ```
    /cheatsheet assunto <assunto> busca <termo de busca>
    ```
    Args:
        assunto: Index do assunto para realizar a busca
        busca: Termo para realizar a busca
    Este comando busca no meilisearch os comandos de acordo com a busca e retorna um embed com os links para a documentação
    """

    def __init__(self, docs_url: str):
        self.client = meilisearch.Client("http://192.168.5.27:7700")
        self.indexes = [index.uid for index in self.client.get_indexes()["results"]]
        self.url = docs_url
        super().__init__()

    @app_commands.command(
        name="cheatsheet", description="Dicas para comandos previamente salvos"
    )
    async def cheatsheet(
        self, interaction: discord.Interaction, assunto: str, busca: str
    ):
        try:
            embed = search(
                subject=assunto,
                search=busca,
                subjects=self.indexes,
                client=self.client,
                doc_url=self.url,
            )
        except SubjectNotFound:
            await interaction.response.send_message(
                f"Assunto inválido, os assuntos disponiveis são: {', '.join(self.indexes)}",
                ephemeral=True,
            )
            return
        except SearchNotFound:
            await interaction.response.send_message("Nada encontrado", ephemeral=True)
            return

        await interaction.response.send_message(embed=embed)


def get_hits(client: meilisearch.Client, subject: str, search: str):
    return client.index(subject).search(search)


def search(
    subject: str,
    search: str,
    subjects: list[str],
    client: meilisearch.Client,
    doc_url: str,
) -> discord.Embed:
    """_Função que faz a busca no Meiliesearch_
    Args:
        subject: _Index para busca no meilisearch_
        search: _Termo de busca_
        subjects: _Lista de assuntos permitidos_
        client: _O Client do meilisearch_
    Raises:
        SubjectNotFound: _Erro quando o assunto não esta na lista de index no meilisearch_
        SearchNotFound: _Erro quando a busca retorna vazia_

    Returns:
        Embed: _Retorna um embed do discord_
    """
    if subject not in subjects:
        raise SubjectNotFound()

    hits = get_hits(client, subject, search)

    embed = discord.Embed()
    embed.title = "Areas Possiveis:"
    if len(hits["hits"]) <= 0:
        raise SearchNotFound()

    for hit in hits["hits"]:
        title = hit["title"]
        slug = slugify(title, "-")

        file_name = f"/{hit['file_name']}/" if hit["file_name"] != "index" else ""
        url = f"{doc_url}/cheatsheets/{subject}{file_name}#{slug}"

        simple = f"{hit['content'][0:50]}..."
        embed.add_field(name=title, value=f"[{simple}]({url})", inline=False)

    return embed


class SubjectNotFound(Exception):
    def __init__(self, message="Subject not found"):
        super().__init__(message)


class SearchNotFound(Exception):
    def __init__(self, message="Not found any relation"):
        super().__init__(message)


async def setup(bot: Bot):
    config = bot.config
    await bot.add_cog(CheatSheet(docs_url=config.docs_url))
    print("✔ - Cog CheatSheet synced")
