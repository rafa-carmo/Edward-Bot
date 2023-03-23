import configparser
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Ini:
    def __init__(self, filename="config.ini"):
        self.token: str
        self.INI_FILE = BASE_DIR / filename
        self.__load_ini_file()
        self.docs_url: str

    def __load_ini_file(self):
        if not os.path.isfile(self.INI_FILE):
            raise MissingFile()

        config = configparser.ConfigParser()
        config.read(self.INI_FILE)

        self.config = config
        try:
            self.token = config["CREDENTIALS"]["token"]
            self.docs_url = config["CREDENTIALS"]["docs_url"]
        except KeyError:
            raise KeyError(
                "missing paramethers in config file, run with --config para configurar."
            )
        return

    def __create_ini_file(self):
        print("Configuração inicial do bot.")
        token = str(input("Digite o token do bot: "))
        config = configparser.ConfigParser()
        config.read(self.INI_FILE)
        config["CREDENTIALS"] = {"token": token}
        with open(self.INI_FILE, "w") as configfile:
            config.write(configfile)


class MissingFile(Exception):
    def __init__(self, message="Missing config file, run with --config to configure"):
        super().__init__(message)
