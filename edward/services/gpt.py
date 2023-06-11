import os

import openai
from dotenv import load_dotenv

load_dotenv()


def getResponse(question: str) -> str:
    openai.api_key = os.getenv("OPEN_AI_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        temperature=0.7,
        max_tokens=2048,
        n=1,
        stop=None,
    )
    text_response = response["choices"][0]["text"].strip()
    return f"``` {text_response} ```"
