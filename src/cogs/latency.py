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

import time
import nextcord
from config import guilds
from nextcord.ext import commands
from nextcord import slash_command

# cog
class latency(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @slash_command(name="latency", description="Latency of the bot", guild_ids=guilds)
    async def latency(self, interaction: nextcord.Interaction) -> None:
        bot = self.bot
        t1 = time.monotonic()
        embed = nextcord.Embed(
            title = "Bot Latency",
            description = f"""
**Latency:** Checking...
**API Latency:** {bot.latency}
""",
            color = nextcord.Color.blue()
        )
        msg = await interaction.response.send_message(embed=embed, ephemeral=False)
        t2 = time.monotonic()
        t = t2 - t1
        tms = t * 1000
        tmsr = round(tms, 1)
        bott = bot.latency
        bottms = bott * 1000
        bottmsr = round(bottms, 1)
        avgtmsr = (tmsr + bottmsr) / 2
        embed.description = f"""
**Latency:** {tmsr} ms
**API Latency:** {bottmsr} ms
"""
        embed.color = nextcord.Color.green() if avgtmsr <= 100 else nextcord.Color.dark_green() if avgtmsr <= 250 else nextcord.Color.yellow() if avgtmsr <= 500 else nextcord.Color.red() if avgtmsr <= 700 else nextcord.Color.dark_red()
        await msg.edit(embed=embed)
    
    @slash_command(name="ping", description="Latency of the bot", guild_ids=guilds)
    async def ping(self, interaction: nextcord.Interaction) -> None:
        await self.latency(interaction)

def setup(bot: commands.Bot, **kwargs) -> None:
    bot.add_cog(latency(bot, **kwargs))