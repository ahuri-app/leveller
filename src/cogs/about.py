import nextcord
from config import guilds, sqd
from nextcord.ext import commands
from nextcord import slash_command

# cog
class about(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="about", description="About the bot!", guild_ids=guilds)
    async def about(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="About",
            description=f"""
**Ahuri Leveller** is a levelling bot that calculates how many bytes each message you send is (does not include embeds and attachments!) and stores it in the database.
You can do `/level` to check how much you've chatted.
We will also add custom roles for when you level up! But for now we will check how fast people gain bytes by chatting.

This bot is **open-source**! You can find it's source code [here](https://github.com/ahuri-app/leveller).
Made by <@{sqd}> in Python 3.

View `/help` for a list of commands.
""",
            color=0x2f3136
        ).add_field(
            name="License",
            value="""
**This bot is licensed under the GNU General Public License Version 3, 29 June 2007.**
```
Ahuri Leveller Copyright (C) 2022 Arshdeep Singh
This program comes with ABSOLUTELY NO WARRANTY; for details see (1).
This is free software, and you are welcome to redistribute it under certain conditions; see (2) for details.
```[(1)](https://github.com/ahuri-app/leveller/blob/main/COPYING#:~:text=modification%20follow.-,TERMS%20AND%20CONDITIONS,-0.%20Definitions.), [(2)](https://github.com/ahuri-app/leveller/blob/main/COPYING#:~:text=15.%20Disclaimer%20of%20Warranty.)
"""
        ).set_thumbnail("https://cdn.discordapp.com/attachments/1017855060190965830/1027468832857673738/dwont_shwoot_mwe.png")
        await interaction.response.send_message(embed=embed, ephemeral=False)

def setup(bot):
    bot.add_cog(about(bot))