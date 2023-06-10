FROM python:3.11.2
WORKDIR /bot
RUN pip install poetry

COPY . /bot
RUN poetry install

ENTRYPOINT ["poetry", "run", "python",  "edward/bot.py"]