import os
from utils import blen

class Database:
    """
    A custom database for peoples level data.
    """
    def __init__(self, path: str = "database") -> None:
        self.path = path
    
    def __str__(self) -> str:
        return self.path
    
    def __len__(self) -> int:
        return len(os.listdir(self.path))

    def add_guild(self, id: int | str) -> bool:
        """
        Add a guild to database

        Args:
            id (int | str): id of the guild

        Returns:
            bool: whether guild was added or not
        """
        id = str(id)
        if id in os.listdir(self.path):
            return False
        else:
            os.mkdir(os.path.join(self.path, id))
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
        if id in os.listdir(os.path.join(self.path, guild)):
            return False
        else:
            open(os.path.join(self.path, guild, id), "w").write("0")
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
        user = open(os.path.join(self.path, guild, id), "w+")
        current_bytes = int(user.read())
        total = current_bytes + bytes
        user.write(str(total))
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
        return int(open(os.path.join(self.path, guild, id), "r").read())
    
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
        if guild not in os.listdir(self.path):
            self.add_guild(guild)
        if user not in os.listdir(os.path.join(self.path, guild)):
            self.add_user(user, guild)
        return self.add_bytes(bytes, user, guild)