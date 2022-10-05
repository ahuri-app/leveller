import os
from utils import exc, blen, read, write
from traceback import format_exception
from logger import Logger

class Database:
    """
    A custom database for peoples level data.
    """
    def __init__(self, path: str = "database", log: bool = False, log_path: str = "dblog", log_in_utc: bool = False, print_logs: bool = False, log_time: bool = True) -> None:
        self.path = path
        self.log_enabled = log
        if self.log_enabled:
            self.log_path = log_path
            self.log_in_utc = log_in_utc
            self.log_time = log_time
            self.logger = Logger(self.log_path, self.log_in_utc, self.log_time)
            self.print_logs = print_logs
            self.log("Ready.\n")

    def __str__(self) -> str:
        return self.path
    
    def __len__(self) -> int:
        return len(os.listdir(self.path))

    def log(self, text: str = "") -> Logger.Log | None:
        """
        Log a string of text.

        Args:
            text (str, optional): string. Defaults to "".

        Returns:
            Logger.Log | None: if logs are enabled returns log 
                               class containing log details else returns none
        """
        if self.log_enabled:
            if self.print_logs:
                return self.logger.log(text)
            else:
                return self.logger.log(text, False)

    def get_logs(self) -> list[Logger.Log]:
        """
        Get all logs logged

        Returns:
            list[Logger.Log]: list of logs
        """
        if self.log_enabled:
            return self.logger.logs
        else:
            return []

    def add_guild(self, id: int | str) -> bool:
        """
        Add a guild to database

        Args:
            id (int | str): id of the guild

        Returns:
            bool: whether guild was added or not
        """
        self.log(f"Adding guild with ID: {id}")
        id = str(id)
        if id in os.listdir(self.path):
            self.log(f"Guild with ID `{id}` is already added")
            return False
        else:
            try:
                os.mkdir(os.path.join(self.path, id))
            except Exception as e:
                exception = exc(e)
                self.log(f"Failed to add guild with ID `{id}` due to the following exception:\n{exception}")
            else:
                self.log(f"Added guild with ID `{id}`")
            return True
    
    def add_user(self, id: int | str, guild: int | str) -> bool:
        """
        Add a user to database of a guild

        Args:
            id (int | str): id of the user
            guild (int | str): id of the guild

        Returns:
            bool: whether the user was added to guild database or not
        """
        id = str(id)
        guild = str(guild)
        self.log(f"Adding user with ID `{id}` in guild `{guild}`")
        if id in os.listdir(os.path.join(self.path, guild)):
            self.log(f"User with ID `{id}` is already added in guild `{guild}`")
            return False
        else:
            try:
                write(0, os.path.join(self.path, guild, id))
            except Exception as e:
                exception = exc(e)
                self.log(f"Failed to add user with ID `{id}` in guild `{guild}` due to the following exception:\n{exception}")
                return False
            else:
                self.log(f"Added user with ID `{id}` in guild `{guild}`")
                return True
    
    def add_bytes(self, bytes: int, id: int | str, guild: int | str) -> int:
        """
        Add some bytes to user's database

        Args:
            bytes (int): amount of bytes to add
            id (int | str): id of the user
            guild (int | str): id of the guild

        Returns:
            int: total amount of bytes the user has now
        """
        id = str(id)
        guild = str(guild)
        self.log(f"Adding {bytes} bytes to user with ID `{id}` in guild `{id}`")
        path = os.path.join(self.path, guild, id)
        self.log(f"Reading user with ID `{id}` in guild `{guild}`'s bytes")
        try:
            current_bytes = read(path)
        except Exception as e:
            exception = exc(e)
            self.log(f"An error occured while reading user with ID `{id}` in guild `{guild}`'s bytes! Exception:\n{exception}")
            return 0
        else:
            self.log(f"User with ID `{id}` in guild `{guild}` currently has {current_bytes} bytes")
            total = current_bytes + bytes
            self.log(f"Writing {total} bytes to user with ID `{id}` in guild `{guild}`")
            try:
                write(total, path)
            except Exception as e:
                exception = exc(e)
                self.log(f"An error occured while writing user with ID `{id}` in guild `{guild}`'s bytes! Exception:\n{exception}")
                return 0
            else:
                self.log(f"Added {bytes} bytes to user with ID `{id}` in guild `{id}`")
                self.log(f"User with ID `{id}` in guild `{guild}` currently has {total} bytes")
                return total
    
    def check_bytes(self, id: int | str, guild: int | str) -> int:
        """
        Check the amount of bytes the user has now

        Args:
            id (int | str): if of the user
            guild (int | str): id of the guild

        Returns:
            int: amount of bytes user has now
        """
        id = str(id)
        guild = str(guild)
        self.log(f"Reading user with ID `{id}` in guild `{guild}`'s bytes")
        try:
            bytes = read(os.path.join(self.path, guild, id))
        except Exception as e:
            exception = exc(e)
            self.log(f"An error occured while reading user with ID `{id}` in guild `{guild}`'s bytes! Exception:\n{exception}")
            return 0
        else:
            self.log(f"User with ID `{id}` in guild `{guild}` currently has {bytes} bytes")
            return bytes

    def calc_KiB(self, bytes: int) -> int:
        """
        Calculate the size of bytes in KiB

        Args:
            bytes (int): amount of bytes to calculate to KiB

        Returns:
            int: KiB
        """
        return bytes / 1024

    def calc_MiB(self, bytes: int) -> int:
        """
        Calculate the size of bytes in MiB

        Args:
            bytes (int): amount of bytes to calculate to MiB

        Returns:
            int: MiB
        """
        return (bytes / 1024) / 1024
    
    def calc_GiB(self, bytes: int) -> int:
        """
        Calculate the size of bytes in GiB

        Args:
            bytes (int): amount of bytes to calculate to GiB

        Returns:
            int: GiB
        """
        return ((bytes / 1024) / 1024) / 1024
    
    def auto_calc(self, bytes: int) -> list[int, str]:
        """
        Automatically calculate the size of bytes specified

        Args:
            bytes (int): bytes to calculate

        Returns:
            list[int, str]: list with amount of B, KiB, MiB or GiB units
        """
        KiB = bytes / 1024
        MiB = KiB / 1024
        GiB = MiB / 1024
        if KiB < 1:
            return [bytes, "B"]
        elif MiB < 1:
            return [KiB, "KiB"]
        elif GiB < 1:
            return [MiB, "MiB"]
        else:
            return [GiB, "GiB"]

    def auto(self, msg: str, user: int | str, guild: int | str) -> int:
        """
        Automatically add guilds if not in database, add user
        if not in database of the guild and add bytes to the
        user

        Args:
            msg (str): the message to calculate to bytes
            user (int | str): id of the user
            guild (int | str): id of the guild

        Returns:
            int: total amount of bytes the user has now
        """
        bytes = blen(msg)
        user = str(user)
        guild = str(guild)
        self.log(f"Auto logging {bytes} bytes in user `{user}` in guild `{guild}`")
        if guild not in os.listdir(self.path):
            self.add_guild(guild)
        if user not in os.listdir(os.path.join(self.path, guild)):
            self.add_user(user, guild)
        return self.add_bytes(bytes, user, guild)