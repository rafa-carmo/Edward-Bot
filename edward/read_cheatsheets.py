import os
import uuid

import meilisearch


def only_codes(content: str) -> str:
    codes = ""
    if content.count("```") == 2:
        for code in content.split("```"):
            if content[content.index(code) - 1] == "`":
                codes += f"{code};"

    return codes


def get_sections(content: list[str]) -> list[dict[str, str]]:
    content_section: list[dict[str, str]] = []
    temp_str: dict[str, str] = {"title": "", "content": "", "codes": ""}
    for line in content:
        if "# " in line:
            temp_str["codes"] = only_codes(temp_str["content"])
            content_section.append(temp_str)
            temp_str = {}
            temp_str["title"] = line.replace("#", "").strip()
            temp_str["content"] = ""
            continue

        temp_str["content"] += line

    return content_section


def delete_index_if_exists(client, index):
    try:
        index_meilisearch = client.get_index(index)
        client.delete_index(index)
    except meilisearch.errors.MeiliSearchApiError as e:
        return


def add_index(client, file_dir, file_name, name):
    with open(file_dir, "r", encoding="utf-8") as f:
        content = f.read().split("\n")

    sections = get_sections(content)
    sections.pop(0)
    if len(sections) <= 0:
        return
    for key, section in enumerate(sections):
        sections[key]["file_name"] = file_name
        sections[key]["id"] = str(uuid.uuid4())
    client.index(name).update_documents(sections)


def clear_meilisearch(url: str):
    client = meilisearch.Client(url)
    while True:
        indexes = client.get_indexes()

        size = len(indexes["results"])
        for index in indexes["results"]:
            client.index(index.uid).delete()
        if len(indexes["results"]) == indexes["total"]:
            break


def run_clear():
    url = str(input("Digite a url do meilisearch para limpar: "))
    clear_meilisearch(url)


def run():
    client = meilisearch.Client("http://192.168.5.27:7700")

    for root, dirs, files in os.walk(os.path.join("docs", "cheatsheets")):
        path = root.split(os.sep)
        for file in files:
            if ".md" in file:
                add_index(client, f"{root}{os.sep}{file}", file[:-3], path[-1])
