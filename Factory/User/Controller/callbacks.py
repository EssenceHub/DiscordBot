import discord

from Factory.User.View.console import ConsoleUI
from Factory.User.Controller.modifiers import ConsoleLogic
from Factory.User.Model.data import Data

class Callbacks:
    def __init__(self, console: ConsoleUI, data: Data):
        # UI
        self.console = console
        self.embed = console.embed

        # Member
        self.member = data
        self.interaction = data.interaction
        

        # Database
        self.db = data.db
        self.cursor = data.cursor

        # Callbacks
        self.console.profile_button.callback = self.Profile_Button_Callback
        self.console.permissions_button.callback = self.Permissions_Button_Callback
        self.console.party_button.callback = self.Party_Button_Callback

        # Embed logic
        self.embed.color = 0x800080

        self.console_logic = ConsoleLogic(console, data)
    
    # Buttons -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def Profile_Button_Callback(self, interaction: discord.Interaction):
        self.console_logic.Profile_Console()

        await interaction.response.edit_message(embed=self.embed, view=self.console)
    
    async def Permissions_Button_Callback(self, interaction: discord.Interaction):
        self.console_logic.Permissions_Console()

        await interaction.response.edit_message(embed=self.embed, view=self.console)
    
    async def Party_Button_Callback(self, interaction: discord.Interaction):
        self.console_logic.Party_Console()

        await interaction.response.edit_message(embed=self.embed, view=self.console)