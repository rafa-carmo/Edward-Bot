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


def test_receive_raise_if_return_is_empty():
    message_error = "Not found any relation"
    client = meilisearch.Client("http://localhost:7700")
    subjects = [index.uid for index in client.get_indexes()["results"]]

    with raises(SearchNotFound) as error:
        search(
            subject="git",
            search="teste",
            subjects=subjects,
            client=client,
            doc_url="http://teste.com",
        )
    assert error.value.args[0] == message_error


def test_have_to_return_a_discord_embed():
    message_error = "Not found any relation"
    client = meilisearch.Client("http://localhost:7700")
    subjects = [index.uid for index in client.get_indexes()["results"]]

    embed = search(
        subject="docker",
        search="install",
        subjects=subjects,
        client=client,
        doc_url="http://teste.com",
    )

    assert isinstance(embed, Embed)
