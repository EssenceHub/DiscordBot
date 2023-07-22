import discord

from Factory.User.View.console import ConsoleUI
from Factory.User.Model.data import Data

class ConsoleLogic:
    def __init__(self, console: ConsoleUI, data: Data):
        # UI
        self.console = console
        self.embed = console.embed
        # Data
        self.data = data
        self.interaction = data.interaction

        self.Starter_Console()

    # Console Logic
    def Starter_Console(self):
        self.embed.title = ""
        self.embed.description = ""

        if self.data.activity_points is None: 
            self.New_User_Console()
            return

        self.Profile_Console()

    def New_User_Console(self):
        self.embed.title = "No Data"
        self.embed.description = "This user has never interacted with Essence"

    def Profile_Console(self):
        self.embed.title = "Profile"
        self.embed.description = f"{self.data.activity_str}\n\n**Roles:** {self.data.roles}"

        self.console.clear_items()
        if self.data.party is not None:
            self.console.add_item(self.console.party_button)
        self.console.add_item(self.console.permissions_button)

    def Party_Console(self):
        self.embed.title = "Party Information"
        self.embed.description = f"**Party Name:** {self.data.party}\n\n**Party Rank:** {self.data.party_rank}\n\n**Party Points** {self.data.party_points}"

        self.console.clear_items()
        self.console.add_item(self.console.profile_button)

    def Permissions_Console(self):
        self.embed.title = f"Permissions"
        self.embed.description = f"{self.data.permissions}"

        self.console.clear_items()
        self.console.add_item(self.console.profile_button)
    
