from unittest import mock

import meilisearch
from discord import Embed
from pytest import raises

from edward.cogs.cheatsheet import SearchNotFound, SubjectNotFound, search


def test_receive_raise_if_subject_not_in_list():
    message_error = "Subject not found"

    with raises(SubjectNotFound) as error:
        search(
            subject="teste",
            search="teste",
            subjects=["outro"],
            client="",
            doc_url="http://teste.com",
        )
    assert error.value.args[0] == message_error


@mock.patch("edward.cogs.cheatsheet.get_hits")
def test_receive_raise_if_return_is_empty(mock_get_hits):
    mock_get_hits.return_value = {
        "hits": [],
        "query": "branch",
        "processingTimeMs": 0,
        "limit": 20,
        "offset": 0,
        "estimatedTotalHits": 3,
    }

    message_error = "Not found any relation"
    client = ""
    subjects = ["git", "docker"]

    with raises(SearchNotFound) as error:
        search(
            subject="git",
            search="teste",
            subjects=subjects,
            client=client,
            doc_url="http://teste.com",
        )
    assert error.value.args[0] == message_error


@mock.patch("edward.cogs.cheatsheet.get_hits")
def test_have_to_return_a_discord_embed(mock_get_hits):
    mock_get_hits.return_value = {
        "hits": [
            {
                "title": "Branches",
                "content": "Criar branch e trocar para ela ```",
                "codes": "",
                "file_name": "index",
                "id": "187104cd-5e02-4037-b534-ddf3f5176166",
            }
        ],
    }
    message_error = "Not found any relation"
    client = ""
    subjects = ["git", "docker"]

    embed = search(
        subject="git",
        search="branches",
        subjects=subjects,
        client=client,
        doc_url="http://teste.com",
    )

    assert isinstance(embed, Embed)
