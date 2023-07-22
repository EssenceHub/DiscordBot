import discord

from Factory.WakeUp.data import Data
from Factory.WakeUp.console import Console

class Logic:
    def __init__(self, interaction: discord.Interaction):
        # Inheritance
        self.data = Data(interaction)
        self.console = Console(self.data)
        self.embed = self.console.embed

        # Database Vars
        self.db = self.data.db
        self.cursor = self.data.cursor

        # Button Logic
        self.buttons = Buttons(self.data, self.console)
        self.console.first_option_button.callback = self.buttons.Option_One_Confirmation_Callback
        self.console.second_option_button.callback = self.buttons.Option_Two_Confirmation_Callback
        self.console.third_option_button.callback = self.buttons.Option_Three_Confirmation_Callback
        self.console.fourth_option_button.callback = self.buttons.Option_Four_Confirmation_Callback
        self.console.select_winner_button.callback = self.buttons.Winner_Selection_Callback

        # Modal Logic
        self.modals = Modals(self.data, self.console)
        self.console.bet_creation_modal.on_submit = self.modals.Option_Creation_Callback
        self.console.bet_amount_modal.on_submit = self.modals.Bet_Amount_Callback
        self.console.winning_bet_modal.on_submit = self.modals.Bet_Winning_Callback

class Buttons():
    def __init__(self, data: Data, console: Console):
        self.data = data
        self.console = console
        self.embed = console.embed

    async def Option_One_Confirmation_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if self.data.not_registered(interaction.user):
            self.console.modifiers.Not_Registered_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        if self.data.already_bet(interaction, self.data.bet_name):
            self.console.modifiers.Already_Bet_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        self.data.player_choice = 0
        self.console.bet_amount_modal.title = f"Betting on [{self.data.options[self.data.player_choice]}]"

        await interaction.response.send_modal(self.console.bet_amount_modal)

    async def Option_Two_Confirmation_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if self.data.not_registered(interaction.user):
            self.console.modifiers.Not_Registered_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        if self.data.already_bet(interaction, self.data.bet_name):
            self.console.modifiers.Already_Bet_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        self.data.player_choice = 1
        self.console.bet_amount_modal.title = f"Betting on [{self.data.options[self.data.player_choice]}]"

        await interaction.response.send_modal(self.console.bet_amount_modal)

    async def Option_Three_Confirmation_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if self.data.not_registered(interaction.user):
            self.console.modifiers.Not_Registered_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        if self.data.already_bet(interaction, self.data.bet_name):
            self.console.modifiers.Already_Bet_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        self.data.player_choice = 2
        self.console.bet_amount_modal.title = f"Betting on [{self.data.options[self.data.player_choice]}]"

        await interaction.response.send_modal(self.console.bet_amount_modal)

    async def Option_Four_Confirmation_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if self.data.not_registered(interaction.user):
            self.console.modifiers.Not_Registered_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        if self.data.already_bet(interaction, self.data.bet_name):
            self.console.modifiers.Already_Bet_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        self.data.player_choice = 3
        self.console.bet_amount_modal.title = f"Betting on [{self.data.options[self.data.player_choice]}]"

        await interaction.response.send_modal(self.console.bet_amount_modal)

    async def Winner_Selection_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_modal(self.console.winning_bet_modal)
        else:
            self.console.modifiers.Insufficient_Permissions_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)

class Modals():
    def __init__(self, data: Data, console: Console):
        self.data = data
        self.console = console
        self.embed = console.embed

    async def Option_Creation_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        self.data.bet_name = interaction.data["components"][0]["components"][0]["value"]

        self.data.cursor.execute("SELECT * FROM bets WHERE name = ?", (self.data.bet_name,))
        info = self.data.cursor.fetchone()
        
        if not info == None:
            self.console.modifiers.Input_Error_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return

        option_1 = interaction.data["components"][1]["components"][0]["value"]
        option_2 = interaction.data["components"][2]["components"][0]["value"]
        option_3 = interaction.data["components"][3]["components"][0]["value"]
        option_4 = interaction.data["components"][4]["components"][0]["value"]

        options_input = [option_1, option_2, option_3, option_4]

        # Adds the non empty options to a list of options
        for option in options_input:
            if option != "":
                self.data.options.append(option)

        # Adds the bet to the database
        sql = "INSERT INTO bets(name) VALUES (?)"
        val = (self.data.bet_name,)
        self.data.cursor.execute(sql, val)
        
        # Updates the bet with the information
        for i, option in enumerate(self.data.options):
            # this is a list of the str options that's being appended to
            self.data.cursor.execute(f"UPDATE bets SET option_{i+1} = ? WHERE name = ?", (option, self.data.bet_name))
            self.data.db.commit()

            # using the option, modify the buttons to display the option name
            option_button = self.console.option_buttons[i]
            option_button.label = option
            option_button.disabled = False

            # Add the button to the console
            self.console.add_item(option_button)

        self.data.db.commit()

        # Sends the bet into the defined channel
        self.data.cursor.execute("SELECT bets_channel_id FROM settings WHERE guild_id = ?", (interaction.guild.id,))
        bets_channel_id = self.data.cursor.fetchone()

        if bets_channel_id == None:
            self.console.modifiers.Request_Failed()
            await interaction.response.send_message(embed=self.embed, view=self.console)
            return
        else:
            bets_channel_id = bets_channel_id[0]
            bets_channel = discord.utils.get(interaction.guild.channels, id=bets_channel_id)

            self.console.modifiers.Bet_Created_Console()
            self.console.add_item(self.console.select_winner_button)
            await bets_channel.send(embed=self.embed, view=self.console)
            
        # Modifies the console to a confirmation telling you that the bet has been created
        self.console.clear_items()
        self.console.modifiers.Bet_Confirmaiton_Console()

        await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)

    async def Bet_Amount_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        self.data.player_bet_amount = interaction.data["components"][0]["components"][0]["value"]

        try:
            int(self.data.player_bet_amount)
        except ValueError:
            self.console.modifiers.Input_Error_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return
        
        # Update the user's coin with their bet amount
        sql = "SELECT galleons FROM players WHERE id = ?"
        val = (interaction.user.id,)
        self.data.cursor.execute(sql, val)
        galleons = self.data.cursor.fetchone(); galleons = galleons[0]

        # Prevent overdrawing your galleons
        if int(self.data.player_bet_amount) > int(galleons):
            self.console.modifiers.Insufficient_Galleons_Console()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
            return

        # Update the bet string with their bet information
        new_bet_string = f"{interaction.user.id}-{self.data.player_bet_amount}-{self.data.player_choice}|"
        
        sql = "SELECT bets_made FROM bets WHERE name = ?"
        val = (self.data.bet_name,)
        self.data.cursor.execute(sql, val)
        
        old_bets_made = self.data.cursor.fetchone(); old_bets_made = old_bets_made[0] or ""
        new_bets_made = f"{old_bets_made}{new_bet_string}"
        
        sql = "UPDATE bets SET bets_made = ? WHERE name = ?"
        val = (new_bets_made, self.data.bet_name)
        self.data.cursor.execute(sql, val)
        
        bet_amount = int(self.data.player_bet_amount)
        
        sql = "UPDATE players SET galleons = ? WHERE id = ?"
        val = (int(galleons) - bet_amount, interaction.user.id)
        self.data.cursor.execute(sql, val)

        self.data.db.commit()

        self.console.modifiers.Option_Confirmation_Console()
        await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)

    async def Bet_Winning_Callback(self, interaction: discord.Interaction):
        bet_name = self.data.bet_name
        cursor = self.data.cursor
        db = self.data.db

        winning_choice_name = interaction.data["components"][0]["components"][0]["value"]; self.data.winner = winning_choice_name

        cursor.execute("SELECT option_1, option_2, option_3, option_4, bets_made FROM bets WHERE name = ?", (bet_name,))
        option_1_name, option_2_name, option_3_name, option_4_name, bets_made = cursor.fetchone()

        # Betting reward logic

        # Create a dictionary to store information about each betting option
        options = {
            "0": {"name": option_1_name, "participants": []},
            "1": {"name": option_2_name, "participants": []},
            "2": {"name": option_3_name, "participants": []},
            "3": {"name": option_4_name, "participants": []}
        }

        # Convert the winning_choice_name to its corresponding index in the options dictionary
        winning_choice = None
        for option_index, option in options.items():
            if option['name'] == winning_choice_name:
                winning_choice = option_index
                break

        if winning_choice is None:
            print(f"Error: Winning choice {winning_choice_name} not found.")

        # Parse the bet information string and add the bets to the appropriate option in the dictionary
        for bet_info in bets_made.split("|"):
            if "-" in bet_info:
                id, amount, choice = bet_info.split("-")
                options[choice]["participants"].append({"id": id, "amount": amount})

        # Calculate the total amount bet on the winning option
        total_winning_bets = 0

        for bet in options[winning_choice]["participants"]:
            if "payout" in bet:
                total_winning_bets += float(bet["payout"])
            else:
                total_winning_bets += float(bet["amount"])


        # Calculate the payout percentage for each non-winning option
        for option_choice in options:
            
            if option_choice != winning_choice:
                total_option_bets = 0

                for bet in options[option_choice]["participants"]:
                    total_option_bets += float(bet["amount"])
                    
                if total_winning_bets == 0:
                    payout_percentage = 0
                else:
                    payout_percentage = total_option_bets / (total_winning_bets + total_option_bets)

                for bet in options[option_choice]["participants"]:
                    bet["payout"] = float(bet["amount"]) * payout_percentage

        # Calculate the payout for each winning bet
        for bet in options[winning_choice]["participants"]:
            total_payout = float(bet["amount"])

            for option in options.values():

                if option["participants"] and option["participants"][0]["id"] == bet["id"]:
                    if "payout" in bet:
                        total_payout += sum([float(bet["payout"]) for bet in option["participants"] if "payout" in bet])
                    break

            bet["payout"] = total_payout


        # Print out the winning bets and their payouts
        print(f"Winning bets for option {winning_choice} ({options[winning_choice]['name']}):")
        for bet in options[winning_choice]["participants"]:
            print(f"- Participant {bet['id']} wins {bet['payout']} with a {bet['amount']} bet and a payout percentage of {payout_percentage}")
            cursor.execute("SELECT galleons FROM players WHERE id = ?", (bet['id'],))
            galleons = cursor.fetchone(); galleons = int(galleons[0])

            cursor.execute("UPDATE players SET galleons = ? WHERE id = ?", (galleons + bet['payout'], bet['id']))

        cursor.execute("DELETE FROM bets WHERE name = ?", (bet_name,))
        print("bet deleted from db")
        db.commit()
        # End of betting reward logic

        self.console.clear_items()
        self.console.modifiers.Winning_Bet_Console()
        await interaction.response.edit_message(embed=self.embed, view=self.console)