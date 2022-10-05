# ahuri helper
from re import I
from logger import Logger
mlog = Logger("logs/main")
falog = Logger("logs/full_access")
if __name__ == "__main__":
    mlog.log("Loading...")
import os
import nextcord
import config
import textwrap
import time
import functools
import datetime
import utils
import database
import logger
from traceback import format_exception
from nextcord.ext import commands
from dotenv import load_dotenv
from errors import errors
from utils import *
from config import *
from database import Database
db = Database(log=True, log_path="logs/dblog")
errors = errors()
p = prefix

load_dotenv()

bot = commands.Bot(
    intents=nextcord.Intents.all(),
    activity=nextcord.Activity(
        type=nextcord.ActivityType.watching,
        name="messages"
    )
)
token = os.getenv("BOT_TOKEN", "env variable not set")

@bot.event
async def on_ready() -> None:
    """
    This is called when the bot is ready.
    """
    mlog.log(f"Connected to Discord!\nLogged in as {bot.user}.")

@bot.event
async def on_message(message: nextcord.Message) -> None:
    """
    This is called when the bot receives a message.

    Args:
        message (nextcord.Message): the message

    Raises:
        errors.BotTokenDetected: when bot token is detected in eval, exec or system commands 
    """
    if message.author == bot.user:
        return
    
    if message.guild == None:
        return
    
    db.auto(message.content, message.author.id, message.guild.id)

    if message.content == p+"bytes":
        bytes = db.check_bytes(message.author.id, message.guild.id)
        cbytes = db.auto_calc(bytes)
        await message.reply(f"You currently have chatted {bytes} bytes worth. (That's {cbytes[0]} {cbytes[1]}!)")

    if message.author.id in config.full_access:
        if message.content.startswith(p):
            falog.log(f"{message.author} ({message.author.id}) used a command: ~```{message.content}```~)")
        if message.content.startswith(p+"reload "):
            cog = message.content.split(p+"reload ", 1)[1]
            info = cogreload(cog, bot)
            await message.reply(info[0]+": "+repr(info[1]))
        elif message.content.startswith(p+"load "):
            cog = message.content.split(p+"load ", 1)[1]
            info = cogload(cog, bot)
            await message.reply(info[0]+": "+repr(info[1]))
        elif message.content.startswith(p+"unload "):
            cog = message.content.split(p+"unload ", 1)[1]
            info = cogunload(cog, bot)
            await message.reply(info[0]+": "+repr(info[1]))
        elif message.content == p+"reloadallcogs":
            info = reloadallcogs(bot)
            t = ""
            for x in info:
                t = t + f"{x}: {info[x][0]}\n"
                if info[x][0] == "ERROR":
                    t = t + f" - Reason: {repr(info[x][1])}\n"
            await message.reply(t)
        elif message.content == p+"loadallcogs":
            info = loadallcogs(bot)
            t = ""
            for x in info:
                t = t + f"{x}: {info[x][0]}\n"
                if info[x][0] == "ERROR":
                    t = t + f" - Reason: {repr(info[x][1])}\n"
            await message.reply(t)
        elif message.content == p+"unloadallcogs":
            info = unloadallcogs(bot)
            t = ""
            for x in info:
                t = t + f"{x}: {info[x][0]}\n"
                if info[x][0] == "ERROR":
                    t = t + f" - Reason: {repr(info[x][1])}\n"
            await message.reply(t)
        elif message.content.startswith(p+"eval "):
            evalstr = message.content.split(p+"eval ", 1)[1]
            main_message = await message.channel.send("Working on it...")
            t = time.monotonic()
            try:
                returned = await bot.loop.run_in_executor(None, functools.partial(eval, evalstr, globals(), locals()))
                returned_as_str = str(returned)
                if token.lower() in returned_as_str.lower():
                    raise errors.BotTokenDetected
            except Exception as e:
                returned = exc(e)
                returned_as_str = str(returned)
            tt = time.monotonic() - t
            mstaken = round(tt*1000, 2)
            staken = round(tt, 2)
            try:
                await main_message.edit("Done!", embed=nextcord.Embed(title=f"Eval by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```py\n{evalstr}\n```").add_field(name="📤 Output:", value=f"```py\n{returned if ''.join(''.join(returned_as_str.strip().splitlines()).split()) != '' else 'No output.'}\n```**Return type:** {type(returned)}\n**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"Python {sys.version}"))
            except nextcord.errors.HTTPException:
                try:
                    await main_message.edit("Done!", embeds=[nextcord.Embed(title=f"Eval by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```py\n{evalstr}\n```").add_field(name="📤 Output:", value=f"```\nCannot fit the output in this field. Check the embed below.\n```**Return type:** {type(returned)}\n**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"Python {sys.version}"), nextcord.Embed(title="📤 Output:", description=f"```py\n{returned if ''.join(''.join(returned_as_str.strip().splitlines()).split()) != '' else 'No output.'}\n```", color = nextcord.Colour.green())])
                except nextcord.errors.HTTPException:
                    filename = str(datetime.datetime.now())+".txt"
                    filename = filename.replace(":", "-")
                    with open("./outputs/"+filename, "w", encoding="utf-8") as outputfile:
                        outputfile.write(returned_as_str)
                    await main_message.edit("Done!", embed=nextcord.Embed(title=f"Eval by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```py\n{evalstr}\n```").add_field(name="📤 Output:", value=f"```\nCannot fit the output in this field or in a new embed. Output is saved in './outputs/{filename}`\n```**Return type:** {type(returned)}\n**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"Python {sys.version}"))
        elif message.content.startswith(p+"exec "):
            execstr = message.content.split(p+"exec ", 1)[1]
            main_message = await message.channel.send("Working on it...")
            t = time.monotonic()
            local_variables = {
                "os": os,
                "nextcord": nextcord,
                "config": config,
                "commands": commands,
                "bot": bot,
                "message": message,
                "main_message": main_message,
                "blen": blen,
                "utils": utils,
                "database": database,
                "logger": logger,
                "config": config,
                "_locals_": locals(),
                "_globals_": globals()
            }
            try:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                await bot.loop.run_in_executor(None, functools.partial(exec, f"async def execfunc():\n{textwrap.indent(execstr, '    ')}", local_variables))
                obj = await local_variables["execfunc"]()
                sys.stdout = old_stdout
                returned = f"{redirected_output.getvalue()}\n-- {obj}\n"
                returned_as_str = str(returned)
                if token.lower() in returned_as_str.lower():
                    raise errors.BotTokenDetected
            except Exception as e:
                obj = e
                returned = exc(e)
                returned_as_str = str(returned)
            tt = time.monotonic() - t
            mstaken = round(tt*1000, 2)
            staken = round(tt, 2)
            try:
                await main_message.edit("Done!", embed=nextcord.Embed(title=f"Exec by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```py\n{execstr}\n```").add_field(name="📤 Output:", value=f"```py\n{returned if ''.join(''.join(returned_as_str.strip().splitlines()).split()) != '' else 'No output.'}\n```**Return type:** {type(obj)}\n**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"Python {sys.version}"))
            except nextcord.errors.HTTPException:
                try:
                    await main_message.edit("Done!", embeds=[nextcord.Embed(title=f"Exec by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```py\n{execstr}\n```").add_field(name="📤 Output:", value=f"```\nCannot fit the output in this field. Check the embed below.\n```**Return type:** {type(obj)}\n**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"Python {sys.version}"), nextcord.Embed(title="📤 Output:", description=f"```py\n{returned if ''.join(''.join(returned_as_str.strip().splitlines()).split()) != '' else 'No output.'}\n```", color = nextcord.Colour.green())])
                except nextcord.errors.HTTPException:
                    filename = str(datetime.datetime.now())+".txt"
                    filename = filename.replace(":", "-")
                    with open("./outputs/"+filename, "w", encoding="utf-8") as outputfile:
                        outputfile.write(returned_as_str)
                    await main_message.edit("Done!", embed=nextcord.Embed(title=f"Exec by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```py\n{execstr}\n```").add_field(name="📤 Output:", value=f"```\nCannot fit the output in this field or in a new embed. Output is saved in './outputs/{filename}`\n```**Return type:** {type(obj)}\n**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"Python {sys.version}"))
        elif message.content.startswith(p+"system "):
            execstr = message.content.split(p+"system ", 1)[1]
            main_message = await message.channel.send("Working on it...")
            t = time.monotonic()
            try:
                returned = await bot.loop.run_in_executor(None, functools.partial(system, execstr))
                returned_as_str = str(returned)
                if token.lower() in returned_as_str.lower():
                    raise errors.BotTokenDetected
            except Exception as e:
                obj = e
                returned = exc(e)
                returned_as_str = str(returned)
            tt = time.monotonic() - t
            mstaken = round(tt*1000, 2)
            staken = round(tt, 2)
            shell_path = system("which $SHELL")
            shell_version = system(f"{shell_path} --version")
            try:
                await main_message.edit("Done!", embed=nextcord.Embed(title=f"Execute System Command by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```sh\n{execstr}\n```").add_field(name="📤 Output:", value=f"```sh\n{returned if ''.join(''.join(returned_as_str.strip().splitlines()).split()) != '' else 'No output.'}\n```**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"{shell_path}: {shell_version.splitlines()[0]}"))
            except nextcord.errors.HTTPException:
                try:
                    await main_message.edit("Done!", embeds=[nextcord.Embed(title=f"Execute System Command by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```sh\n{execstr}\n```").add_field(name="📤 Output:", value=f"```\nCannot fit the output in this field. Check the embed below.\n```**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"{shell_path}: {shell_version.splitlines()[0]}"), nextcord.Embed(title="📤 Output:", description=f"```sh\n{returned if ''.join(''.join(returned_as_str.strip().splitlines()).split()) != '' else 'No output.'}\n```", color = nextcord.Colour.green())])
                except nextcord.errors.HTTPException:
                    filename = str(datetime.datetime.now())+".txt"
                    filename = filename.replace(":", "-")
                    with open("./outputs/"+filename, "w", encoding="utf-8") as outputfile:
                        outputfile.write(returned_as_str)
                    await main_message.edit("Done!", embed=nextcord.Embed(title=f"Execute System Command by {message.author}", color=nextcord.Colour.green()).add_field(name="📥 Input:", value=f"```sh\n{execstr}\n```").add_field(name="📤 Output:", value=f"```\nCannot fit the output in this field or in a new embed. Output is saved in './outputs/{filename}`\n```**Time Taken:** {mstaken}ms ({staken}s)").set_footer(text=f"{shell_path}: {shell_version.splitlines()[0]}"))

if __name__ == "__main__":
    mlog.log("\nLoading all cogs...")
    cogsinfo = loadallcogs(bot)
    for x in cogsinfo:
        mlog.log(f"{x}: {cogsinfo[x][0]}")
        if cogsinfo[x][0] == "ERROR":
            mlog.log(f" - Reason: {repr(cogsinfo[x][1])}")
    mlog.log("Loaded.\n")
    
    mlog.log("Logging in...")
    try:
        bot.run(token)
    except nextcord.errors.LoginFailure:
        mlog.log("Improper token passed.")
        mlog.log(f"Token: '{token}'")