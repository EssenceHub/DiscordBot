import discord

from Factory.WakeUp.data import Data

class Console(discord.ui.View):
    def __init__(self, data: Data):
        self.data = data
        super().__init__(timeout = None)

        # Embed
        self.embed = discord.Embed()

        # Buttons
        self.first_option_button = discord.ui.Button(label="ERROR 101", disabled=True, style=discord.ButtonStyle.blurple, row=1)
        self.second_option_button = discord.ui.Button(label="ERROR 101", disabled=True, style=discord.ButtonStyle.blurple, row=1)
        self.third_option_button = discord.ui.Button(label="ERROR 101", disabled=True, style=discord.ButtonStyle.blurple, row=1)
        self.fourth_option_button = discord.ui.Button(label="ERROR 101", disabled=True, style=discord.ButtonStyle.blurple, row=1)
        self.option_buttons = [self.first_option_button, self.second_option_button, self.third_option_button, self.fourth_option_button]

        self.select_winner_button = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji="⭐", row=1)

        # Modal
        self.modals = Modals(data)
        self.bet_creation_modal = self.modals.Bet_Creation_Modal()
        self.bet_amount_modal = self.modals.Bet_Amount_Modal()
        self.winning_bet_modal = self.modals.Winning_Bet_Modal()

        # Modifiers
        self.modifiers = Modifiers(self.embed, self.data)

class Modifiers:
    def __init__(self, embed: discord.Embed, data: Data):
        self.data = data
        self.embed = embed
        self.embed.color = 0x800080

    def Not_Registered_Console(self):
        self.embed.title = "Not registered"
        self.embed.description = "Please use the /profile command to register, thank you."

    def Already_Bet_Console(self):
        self.embed.title = "Already participated in this bet"
        self.embed.description = "Once bets are made, there are no refunds and you can't increase or decrease the amount. Sorry for the inconvenience."

    def Input_Error_Console(self):
        self.embed.title = "Input Error"
        self.embed.description = "Something has gone wrong, please double check your inputs."

    def Bet_Created_Console(self):
        self.embed.title = self.data.bet_name

        # Description logic for betting options
        betting_contestants = ""
        for option in self.data.options:
            betting_contestants = betting_contestants + f" • {option}\n"

        self.embed.description = f"***Contestants***\n{betting_contestants}\nHosted by {self.data.host.mention}, place your bets now! ⬇️⬇️⬇️"

    def Bet_Confirmaiton_Console(self):
        self.embed.title = "Bet Created"

        self.embed.description = f"Your bet can be found in the bets channel, happy gambling!"

    def Option_Confirmation_Console(self):
        self.embed.title = f"You've bet {self.data.player_bet_amount} galleons on"
        self.embed.description = f"**{self.data.options[self.data.player_choice]}** winning the **{self.data.bet_name}.**"

    def Winning_Bet_Console(self):
        self.embed.title = "Betting Over"

        self.embed.description = f"The winner has been decided, congratulations to everyone who bet for **{self.data.winner}**!"

    def Winning_Bet_Incorrect_Input_Console(self):
        self.embed.title = "Bet Doesn't Exist"
        
        options = "Existing Bets: (if you need to copy)"
        for option in self.data.options:
            options = f"{options}\n{option}"

        self.embed.description = options 

    def Insufficient_Permissions_Console(self):
        self.embed.title = "Insufficient Permissions"
        self.embed.description = "You need Administrator to use this feature."
    
    def Insufficient_Galleons_Console(self):
        self.embed.title = "Insufficient Galleons"
        self.embed.description = "You can't bet more galleons than you have"

class Modals:
    def __init__(self, data: Data):
        self.data = data

    def Bet_Creation_Modal(self):
        modal = discord.ui.Modal(title="Bet Creation")

        modal.add_item(discord.ui.TextInput(label="Name of the bet", required=True, max_length=80))
        modal.add_item(discord.ui.TextInput(label="Contestant #1", required=True, max_length=32))
        modal.add_item(discord.ui.TextInput(label="Contestant #2", required=True, max_length=32))
        modal.add_item(discord.ui.TextInput(label="Contestant #3", required=False, max_length=32))
        modal.add_item(discord.ui.TextInput(label="Contestant #4", required=False, max_length=32))

        return modal
    
    def Bet_Amount_Modal(self):
        modal = discord.ui.Modal(title=f"Betting on ERROR")

        modal.add_item(discord.ui.TextInput(label="Amount:", required=True, min_length=1, max_length=5))

        return modal
    
    def Winning_Bet_Modal(self):
        modal = discord.ui.Modal(title=f"Winning Bet")

        modal.add_item(discord.ui.TextInput(label="Winning Bet Name:"))

        return modal