import re

from metripy.Application.Config.Config import Config
from metripy.Application.Config.File.ConfigFileReaderFactory import (
    ConfigFileReaderFactory,
)


class Parser:
    def parse(self, argv: list[str]) -> Config:
        config = Config()

        if argv[0] == "metripy.py" or argv[0] == "metripy":
            # TODO, fix when path ends with metripy.py
            pass
        argv.pop(0)

        # check for a config file
        for key, arg in enumerate(argv):
            if matches := re.search(r"^--config=(.+)$", arg):
                fileReader = ConfigFileReaderFactory.createFromFileName(
                    matches.group(1)
                )
                fileReader.read(config)
                argv.pop(key)

        # TODO: add the following
        # arguments with options
        # arguments without options
        # last argument

        return config
