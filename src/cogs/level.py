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
import database
from config import guilds
from nextcord.ext import commands
from nextcord import slash_command
from nextcord import SlashOption

# cog
class level(commands.Cog):
    def __init__(self, bot, db: database.Database) -> None:
        self.bot = bot
        self.db = db
    
    @slash_command(name="level", description="Get stats!", guild_ids=guilds)
    async def level(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.User = SlashOption(
            description = "Choose a member to check stats of.",
            required = False,
        )
    ) -> None:
        db = self.db
        bytes = db.check_bytes(interaction.user.id if user == None else user.id, interaction.guild.id)
        cbytes = db.auto_calc(bytes)
        if user != None:
            name = str(user) if user.nick == None else user.nick
            pfp = user.display_avatar.url
        else:
            name = str(interaction.user) if interaction.user.nick == None else interaction.user.nick
            pfp = interaction.user.display_avatar.url
        embed = nextcord.Embed(
            description = f"{'You have' if user == None else '`' + name + '` has'} chatted worth **{round(cbytes[0], 2)} {cbytes[1]}**!",
            color = nextcord.Color.blue()
        )
        embed.set_thumbnail(pfp)
        embed.set_author(
            name = f"Stats of {name}",
            icon_url = pfp
        )
        embed.set_footer(text = f"That's {bytes} bytes!")
        await interaction.response.send_message(embed=embed, ephemeral=False)

def setup(bot: commands.Bot, **kwargs) -> None:
    bot.add_cog(level(bot, **kwargs))