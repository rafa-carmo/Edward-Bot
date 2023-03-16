import os

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


def add_index(client, file, name):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read().split("\n")

    sections = get_sections(content)
    sections.pop(0)

    for key, section in enumerate(sections):
        sections[key]["id"] = key + 1

    client.index(name).add_documents(sections)


def run():
    client = meilisearch.Client("http://localhost:7700")

    for root, dirs, files in os.walk(os.path.join("docs", "cheatsheets")):
        path = root.split(os.sep)

        for file in files:
            if ".md" in file:
                add_index(client, f"{root}{os.sep}{file}", path[-1])
