import os
from datetime import datetime

class Logger:
    """
    Class that implements custom logging.
    """

    def __init__(self, path: str = "logs", utc: bool = False) -> None:
        self.path = path
        self.utc = utc

    def log(self, text: str = "", p: bool = True) -> str:
        """
        Log a string of text.

        Args:
            text (str, optional): string. Defaults to "".
            p (bool, optional): specify whether to print it or not. Defaults to True.

        Returns:
            str: the string you specified
        """
        if self.utc:
            now = str(datetime.utcnow())
        else:
            now = str(datetime.now())
        with open(os.path.join(self.path, now), "a") as logfile:
            logfile.write(text+"\n")
        if p:
            print(text)
        return text

class AsyncLogger:
    """
    Class that implements custom logging with async.
    """

    def __init__(self, path: str = "logs", utc: bool = False) -> None:
        self.path = path
        self.utc = utc

    async def log(self, text: str = "", p: bool = True) -> str:
        """
        Log a string of text.

        Args:
            text (str, optional): string. Defaults to "".
            p (bool, optional): specify whether to print it or not. Defaults to True.

        Returns:
            str: the string you specified
        """
        if self.utc:
            now = str(datetime.utcnow())
        else:
            now = str(datetime.now())
        async with open(os.path.join(self.path, now), "a") as logfile:
            logfile.write(text+"\n")
        if p:
            print(text)
        return text