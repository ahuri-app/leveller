import os
from datetime import datetime
from __future__ import annotations

class Logger:
    """
    Class that implements custom logging.
    """
    def __init__(self, path: str = "logs", utc: bool = False, log_time: bool = True) -> None:
        self.path = path
        self.utc = utc
        self.log_time = log_time
        if self.utc:
            self.created_at = datetime.utcnow()
        else:
            self.created_at = datetime.now()
        self.loggerpath = os.path.join(self.path, str(self.created_at)+".txt")
        self.logs = []

    def __str__(self) -> str:
        return self.path
    
    def __len__(self) -> int:
        return len(self.logs)

    class Log:
        """
        A class that contains info for a log.
        """
        def __init__(self, time: datetime, text: str, strtime: str, utc: bool, logger: Logger) -> None:
            self.time = time
            self.text = text
            self.strtime = strtime
            self.utc = utc
            self.logger = logger

    def log(self, text: str = "", p: bool = True) -> Logger.Log:
        """
        Log a string of text.

        Args:
            text (str, optional): string. Defaults to "".
            p (bool, optional): specify whether to print it or not. Defaults to True.

        Returns:
            Logger.Log: log class that contains info for a log
        """
        to_log = text + "\n"
        if self.log_time:
            if self.utc:
                now = datetime.utcnow()
                strnow = str(now)
            else:
                now = datetime.now()
                strnow = str(now)
            to_log = strnow + to_log
        logfile = open(self.loggerpath, "a")
        logfile.write(to_log)
        logfile.close()
        if p:
            print(text)
        log = self.Log(now, text, strnow, self.utc, self)
        self.logs.append(log)
        return log