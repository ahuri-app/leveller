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

import nextcord
from config import guilds
import asyncio
from nextcord.ext import commands
from nextcord import slash_command

# commands dropdown
class cmdsDrop(nextcord.ui.Select):
    def __init__(self, user: nextcord.User, bot: commands.Bot, inter: nextcord.Interaction, disable: bool) -> None:
        menus = [
            nextcord.SelectOption(label="Info", description="Bot related commands", emoji="⚙️"),
            nextcord.SelectOption(label="Levelling", description="Level related commands", emoji="📈")
        ]
        if disable:
            super().__init__(placeholder="This dropdown has been expired", min_values=1, max_values=1, options=menus, disabled=True)
        elif disable == False:
            super().__init__(placeholder="Select help category", min_values=1, max_values=1, options=menus)
        self.user = user
        self.color = nextcord.Color.blue()
        self.bot = bot
        self.inter = inter
        try:
            self.cavatar = bot.user.avatar.url
        except:
            self.cavatar = bot.user.default_avatar.url
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        if interaction.user == self.user:
            self.embed = nextcord.Embed(title="Commands", description="**`/help`** - List all commands", color=self.color)
            self.embed.set_author(name=self.bot.user.name, icon_url=self.cavatar)
            menuName = self.values[0]
            menu = menuName.lower()
            if menu =="info":
                self.embed.color = nextcord.Color.green()
                self.embed.add_field(name=menuName, value=f"""
**`/about`** - About the bot
**`/ping`**/**`/latency`** - Check the latency of the bot
""", inline=False)
            elif menu == "levelling":
                self.embed.color = nextcord.Color.red()
                self.embed.add_field(name=menuName, value=f"""
**`/level`** - Show your bytes
""", inline=False)
            await self.inter.edit_original_message(embed=self.embed)
        else:
            await interaction.response.send_message(f"**This is not your help menu. This is `{self.user.name}`'s help menu.**", ephemeral=True)

# commmands dropdown view
class cmdsDropView(nextcord.ui.View):
    def __init__(self, user: nextcord.User, bot: commands.Bot, inter: nextcord.Interaction, disable: bool = False) -> None:
        super().__init__()
        self.add_item(cmdsDrop(user, bot, inter, disable))

# cog
class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @slash_command(name="help", description="List all commands", guild_ids=guilds)
    async def help(self, interaction: nextcord.Interaction) -> None:
        bot = self.bot
        try:
            cavatar = bot.user.avatar.url
        except:
            cavatar = bot.user.default_avatar.url
        embed = nextcord.Embed(title="Commands", description="**`/help`** - List all commands", color=nextcord.Colour.blue())
        embed.set_author(name=bot.user.name, icon_url=cavatar)
        view = cmdsDropView(interaction.user, bot, interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
        await asyncio.sleep(60)
        view = cmdsDropView(interaction.user, bot, interaction, disable=True)
        try:
            await interaction.edit_original_message(view=view)
        except:
            pass

def setup(bot: commands.Bot, **kwargs) -> None:
    bot.add_cog(help(bot, **kwargs))