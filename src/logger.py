"""
 - Ahuri Leveller - Levelling Discord bot for Ahuri's Discord server. 
 - Copyright (C) 2022 Arshdeep Singh
 - 
 - This program is free software: you can redistribute it and/or modify
 - it under the terms of the GNU General Public License as published by
 - the Free Software Foundation; either version 3 of the License, or
 - (at your option) any later version.
 - 
 - This program is distributed in the hope that it will be useful,
 - but WITHOUT ANY WARRANTY; without even the implied warranty of
 - MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 - GNU General Public License for more details.
 - 
 - You should have received a copy of the GNU General Public License
 - along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations
import os
from datetime import datetime

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
        self.loggerpath = os.path.join(self.path, str(self.created_at).replace(":", "-")+".txt")
        self.logs = []

    def __str__(self) -> str:
        return self.path
    
    def __len__(self) -> int:
        return len(self.logs)

    class Log:
        """
        A class that contains info for a log.
        """
        def __init__(self, time: datetime, text: str, rawtext: str, strtime: str, utc: bool, logger: Logger) -> None:
            self.time = time
            self.text = text
            self.rawtext = rawtext
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
            lines = to_log.splitlines(keepends=True)
            line = []
            for x in lines:
                line.append("[" + strnow + "] " + x)
            to_log = "".join(line)
        logfile = open(self.loggerpath, "a")
        logfile.write(to_log)
        logfile.close()
        if p:
            print(to_log)
        log = self.Log(now, to_log, text, strnow, self.utc, self)
        self.logs.append(log)
        return log