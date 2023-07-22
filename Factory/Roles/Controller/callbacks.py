import discord

from Factory.Roles.View.console import ConsoleUI
from Factory.Roles.Controller.modifiers import ConsoleLogic
from Factory.Roles.Model.data import Data

class Callbacks:
    def __init__(self, console: ConsoleUI, data: Data):
        # UI
        self.console = console
        self.embed = console.embed

        # Member
        self.data = data
        self.interaction = data.interaction

        # Database
        self.db = data.db
        self.cursor = data.cursor

        # Callbacks
        self.console.role_selection.options = self.data.role_options
        self.console.role_selection.callback = self.Role_Selection_Callback

        self.console_logic = ConsoleLogic(console, data)
    
    # Selection
    async def Role_Selection_Callback(self, interaction: discord.Interaction):
        print(interaction.data)