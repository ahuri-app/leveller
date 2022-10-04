import nextcord
from config import guilds
import asyncio
from nextcord.ext import commands
from nextcord import slash_command

# commands dropdown
class cmdsDrop(nextcord.ui.Select):
    def __init__(self, user, bot, inter, disable):
        menus = [
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
    
    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user == self.user:
            self.embed = nextcord.Embed(title="Commands", description="**`/help`** - List all commands", color=self.color)
            self.embed.set_author(name=self.bot.user.name, icon_url=self.cavatar)
            menuName = self.values[0]
            menu = menuName.lower()
            if menu == "levelling":
                self.embed.add_field(name=menuName, value=f"""

""", inline=False)
            await self.inter.edit_original_message(embed=self.embed)
        else:
            await interaction.response.send_message(f"**This is not your help menu. This is `{self.user.name}`'s help menu.**", ephemeral=True)

# commmands dropdown view
class cmdsDropView(nextcord.ui.View):
    def __init__(self, user, bot, inter, disable=False):
        super().__init__()
        self.add_item(cmdsDrop(user, bot, inter, disable))

# cog
class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="help", description="List all commands", guild_ids=guilds)
    async def help(self, interaction: nextcord.Interaction):
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

def setup(bot):
    bot.add_cog(help(bot))