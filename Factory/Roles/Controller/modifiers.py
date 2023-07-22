import discord

from Factory.Roles.View.console import ConsoleUI
from Factory.Roles.Model.data import Data

class ConsoleLogic:
    def __init__(self, console: ConsoleUI, data: Data):
        # UI
        self.console = console
        self.embed = console.embed
        # Data
        self.data = data
        self.user = data.user
        self.guild = data.guild
        self.interaction = data.interaction

        self.Role_Selection_Console()

    # Console Logic
    def Role_Selection_Console(self):
        self.embed.title = "Self Assignable Roles"

        if self.data.role_str == "**Choices:**":
            self.embed.description = "This server has no self assignable roles"
        else:
            self.embed.description = self.data.role_str
            self.console.add_item(self.console.role_selection)

