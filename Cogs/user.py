import discord

from discord import app_commands
from discord.ext import commands

from Factory.User.Controller.callbacks import Callbacks as ProfileCallbacks
from Factory.User.View.console import ConsoleUI as ProfileConsoleUI
from Factory.User.Model.data import Data as ProfileData

from Factory.Guild.Controller.callbacks import Callbacks as GuildCallbacks
from Factory.Guild.View.console import ConsoleUI as GuildConsoleUI
from Factory.Guild.Model.guild import Guild as GuildInfo

from Factory.Roles.Controller.callbacks import Callbacks as RolesCallbacks
from Factory.Roles.View.console import ConsoleUI as RolesConsoleUI
from Factory.Roles.Model.data import Data as RolesData


class User(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot    

    # Shows the guild's information
    @app_commands.command(description="Guild information!")
    async def guild(self, interaction: discord.Interaction):

        guild_logic = GuildCallbacks(GuildConsoleUI(), GuildInfo(interaction))

        await interaction.response.send_message(embed=guild_logic.embed, view=guild_logic.console, ephemeral=True)



    # Shows your activity points in that guild
    @app_commands.command(description="Check a user's profile!")
    async def profile(self, interaction: discord.Interaction, user: discord.Member = None): # Gets profile logic

        profile_logic = ProfileCallbacks(ProfileConsoleUI(), ProfileData(interaction, user))

        await interaction.response.send_message(embed=profile_logic.embed, view=profile_logic.console, ephemeral=True)


    
    # Displays all self assignable roles in that guild
    @app_commands.command(description='Self Assignable Roles!')
    async def roles(self, interaction: discord.Interaction):

        roles_logic = RolesCallbacks(RolesConsoleUI(), RolesData(interaction))

        await interaction.response.send_message(embed=roles_logic.embed, view=roles_logic.console, ephemeral=True)
    


    # Help command, gotta put more time into this after getting feedback
    @app_commands.command(description='Get help using the bot!')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Help", description="""
        **/profile**: Shows a user's information: Activity\n
        **/arcane**: Interact with arcane related functions: Duels, Missions, Shops and Guilds\n
        **/contact**: Contact server moderation and the bot developer: Bug and User reports, Suggestions\n
        **/moderation**: Punish, pardon and purge messages: MODERATOR ONLY\n
        **/settings**: Configure the server's data: Activity Rewards and Punishments\n
        **/party**: Fun little side project that allows users to create groups: Create, Join and Dailies\n
        **/idle**: Fun little side project that allows users to play an idle game: WIP\n
        **/roles**: Self assignable roles set by staff of that server
        **/help**: Brings up this menu and gives you the option to start the tutorial: :D
        """, color=0x800080)
        await interaction.response.send_message(embed=embed, ephemeral=True) # Need to add a way to log commands aswell.

async def setup(bot: commands.Bot):
    print("User Loaded")
    await bot.add_cog(User(bot))