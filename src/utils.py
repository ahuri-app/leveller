import os
import sys
from io import StringIO
from config import cogs_dir

def cogload(name, bot):
    try:
        bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return ["ERROR", e]
    else:
        return ["OK", "OK"]

def cogunload(name, bot):
    try:
        bot.unload_extension(f"cogs.{name}")
    except Exception as e:
        return ["ERROR", e]
    else:
        return ["OK", "OK"]

def cogreload(name, bot):
    try:
        bot.unload_extension(f"cogs.{name}")
        bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return ["ERROR", e]
    else:
        return ["OK", "OK"]

def loadallcogs(bot):
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

def unloadallcogs(bot):
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

def reloadallcogs(bot):
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

def better_exec(execstr, local_variables=None):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    if local_variables == None:
        exec(execstr)
    else:
        exec(execstr, local_variables)
    sys.stdout = old_stdout
    return redirected_output.getvalue()