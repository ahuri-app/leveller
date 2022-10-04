import os
import sys
import subprocess
from io import StringIO
from types import NoneType
from config import cogs_dir
from nextcord.ext import commands

def cogload(name: str, bot: commands.Bot) -> list[str, str]:
    """
    Load a cog.

    Args:
        name (str): cog name
        bot (commands.Bot): bot to add cog to

    Returns:
        list[str, str]: whether cog was added or there was an error
    """
    try:
        bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return ["ERROR", e]
    else:
        return ["OK", "OK"]

def cogunload(name: str, bot: commands.Bot) -> list[str, str]:
    """
    Unload a cog.

    Args:
        name (str): cog name
        bot (commands.Bot): bot to remove cog from

    Returns:
        list[str, str]: whether cog was removed or there was an error
    """
    try:
        bot.unload_extension(f"cogs.{name}")
    except Exception as e:
        return ["ERROR", e]
    else:
        return ["OK", "OK"]

def cogreload(name: str, bot: commands.Bot) -> list[str, str]:
    """
    Reload a cog.

    Args:
        name (str): cog name
        bot (commands.Bot): bot to reload cog in

    Returns:
        list[str, str]: whether cog was reloaded or there was an error
    """
    try:
        bot.unload_extension(f"cogs.{name}")
        bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return ["ERROR", e]
    else:
        return ["OK", "OK"]

def loadallcogs(bot: commands.Bot) -> dict:
    """
    Load all cogs.

    Args:
        bot (commands.Bot): bot to load all cogs to

    Returns:
        dict: successful/error messages of cogs
    """
    folderlist = os.listdir(cogs_dir)
    cogs = []
    loadinfo = {}
    for x in folderlist:
        if x.endswith(".py"):
            if x == "config.py":
                continue
            cogs.append(x.replace(".py", ""))
    for cog in cogs:
        coginfo = cogload(cog, bot)
        loadinfo.update({cog: coginfo})
    return loadinfo

def unloadallcogs(bot: commands.Bot) -> dict:
    """
    Unload all cogs.

    Args:
        bot (commands.Bot): bot to unload all cogs from

    Returns:
        dict: successful/error messages of cogs
    """
    folderlist = os.listdir(cogs_dir)
    cogs = []
    unloadinfo = {}
    for x in folderlist:
        if x.endswith(".py"):
            if x == "config.py":
                continue
            cogs.append(x.replace(".py", ""))
    for cog in cogs:
        coginfo = cogunload(cog, bot)
        unloadinfo.update({cog: coginfo})
    return unloadinfo

def reloadallcogs(bot: commands.Bot) -> dict:
    """
    Unload all cogs.

    Args:
        bot (commands.Bot): bot to unload all cogs from

    Returns:
        dict: successful/error messages of cogs
    """
    folderlist = os.listdir(cogs_dir)
    cogs = []
    reloadinfo = {}
    for x in folderlist:
        if x.endswith(".py"):
            if x == "config.py":
                continue
            cogs.append(x.replace(".py", ""))
    for cog in cogs:
        coginfo = cogreload(cog, bot)
        reloadinfo.update({cog: coginfo})
    return reloadinfo

def better_exec(execstr: str, local_variables: dict | NoneType = None) -> str:
    """
    Does exec and gets printed output.

    Args:
        execstr (str): the string
        local_variables (dict | NoneType, optional): Adds variables to globals inside exec. Defaults to None.

    Returns:
        str: Printed output
    """
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    if local_variables == None:
        exec(execstr)
    else:
        exec(execstr, local_variables)
    sys.stdout = old_stdout
    return redirected_output.getvalue()

def system(execstr: str) -> str:
    """
    Like os.system() but returns printed output

    Args:
        execstr (str): the string to execute

    Returns:
        str: printed output
    """
    return subprocess.getoutput(execstr)

def blen(string: str) -> int:
    """
    Returns length in bytes of the string passed.

    Args:
        string (str): the string

    Returns:
        int: length in bytes
    """
    return len(string.encode("utf-8"))