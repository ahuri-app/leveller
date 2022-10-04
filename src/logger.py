import os
from datetime import datetime

class Logger:
    """
    Class that implements custom logging.
    """

    def __init__(self, path: str = "logs", utc: bool = False) -> None:
        self.path = path
        self.utc = utc
        if self.utc:
            self.loggerpath = os.path.join(self.path, str(datetime.utcnow()))
        else:
            self.loggerpath = os.path.join(self.path, str(datetime.now()))

    def log(self, text: str = "", p: bool = True) -> str:
        """
        Log a string of text.

        Args:
            text (str, optional): string. Defaults to "".
            p (bool, optional): specify whether to print it or not. Defaults to True.

        Returns:
            str: the string you specified
        """
        with open(os.path.join(self.path, self.loggerpath), "a") as logfile:
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
        if self.utc:
            self.loggerpath = os.path.join(self.path, str(datetime.utcnow()))
        else:
            self.loggerpath = os.path.join(self.path, str(datetime.now()))

    async def log(self, text: str = "", p: bool = True) -> str:
        """
        Log a string of text.

        Args:
            text (str, optional): string. Defaults to "".
            p (bool, optional): specify whether to print it or not. Defaults to True.

        Returns:
            str: the string you specified
        """
        async with open(self.loggerpath, "a") as logfile:
            logfile.write(text+"\n")
        if p:
            print(text)
        return text