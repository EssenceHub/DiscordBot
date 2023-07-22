import discord
from datetime import datetime

# Type hinting
from Factory.Idle.View.console import ConsoleUI
from Factory.Idle.Model.player import Player

# Other Controllers
from Factory.Idle.Controller.modifiers import ConsoleLogic
from Factory.Idle.Controller.monsters import Monsters

class Callbacks:
    def __init__(self, console: ConsoleUI, player: Player):
        # Inheritance
        self.console = console
        self.player = player
        self.embed = console.embed
        self.interaction = player.interaction

        # Database variables
        self.db = player.db
        self.cursor = player.cursor

        # Console button logic
        self.console.character_info_button.callback = self.Character_Info_Button_Callback
        self.console.dungeon_info_button.callback = self.Dungeon_Info_Button_Callback
        self.console.monster_summon_button.callback = self.Monster_Summon_Button_Callback
        self.console.character_creation_button.callback = self.Character_Creation_Button_Callback
        self.console.dungeon_creation_button.callback = self.Dungeon_Creation_Button_Callback
        self.console.summon_creation_button.callback = self.Summon_Creation_Button_Callback
        
        # Console modal logic
        self.console.character_creation_modal.on_submit = self.Character_Creation_Modal_Callback
        self.console.dungeon_creation_modal.on_submit = self.Dungeon_Creation_Modal_Callback
        self.console.summon_creation_modal.on_submit = self.Summon_Creation_Modal_Callback

        # Console selection logic
        self.console.monster_summon_selection.callback = self.Monster_Summon_Selection_Callback

        # Embed logic
        self.embed.color = 0x800080

        self.monsters = Monsters(player)
        self.console_logic = ConsoleLogic(console, player, self.monsters)

    async def isnt_your_console(self, interaction: discord.Interaction):
        if interaction.user.id != self.player.id:
            warning = discord.Embed(title="This is not your console, do /idle to play.")
            await interaction.response.send_message(embed=warning, ephemeral=True)
            return True
        else:
            return False





    # Buttons -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def Character_Info_Button_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return
        
        self.console_logic.Character_Info_Console()
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    




    async def Dungeon_Info_Button_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return
        
        self.console_logic.Dungeon_Info_Console()
        await interaction.response.edit_message(embed=self.embed, view=self.console)





    async def Monster_Summon_Button_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return

        if self.monsters.monster_options == []:
            self.console_logic.Summon_Creation_Console()
        else:
            self.console_logic.Dungeon_Summon_Console()

        await interaction.response.edit_message(embed=self.embed, view=self.console)





    async def Character_Creation_Button_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return
        
        await interaction.response.send_modal(self.console.character_creation_modal)





    async def Dungeon_Creation_Button_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return
        
        await interaction.response.send_modal(self.console.dungeon_creation_modal)





    async def Summon_Creation_Button_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return
        
        await interaction.response.send_modal(self.console.summon_creation_modal)





    # Modals -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def Character_Creation_Modal_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return
        
        self.player.character_name = interaction.data["components"][0]["components"][0]["value"]
        self.cursor.execute(f"UPDATE EssenceIdleData SET character_name = ?, character_level = ? WHERE member_id = ?", (self.player.character_name, 1, self.player.id))
        self.db.commit()

        self.console_logic.Character_Created_Console()
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    




    async def Dungeon_Creation_Modal_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return

        timestamp = round(datetime.now().timestamp())
        self.dungeon_name = interaction.data["components"][0]["components"][0]["value"]

        self.cursor.execute("UPDATE EssenceIdleData SET dungeon_name = ?, dungeon_power = ?, dungeon_energy = ?, last_assault = ? WHERE member_id = ?", (self.dungeon_name, 0, 10, timestamp, self.player.id))
        self.db.commit()

        self.player.dungeon_name = self.dungeon_name

        self.console_logic.Dungeon_Created_Console()
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    




    async def Summon_Creation_Modal_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return

        timestamp = round(datetime.now().timestamp())
        summon_name = interaction.data["components"][0]["components"][0]["value"]
        summon_strength = interaction.data["components"][1]["components"][0]["value"]

        try:
            summon_strength = int(summon_strength)
            nan = False
        except:
            nan = True

        if nan or len(self.monsters.monster_options) == 25 or summon_strength < 0:
            self.console_logic.Summon_Error_Console()
        else:
            self.monsters.create(summon_name, summon_strength)

            self.cursor.execute("UPDATE EssenceIdleData SET dungeon_monsters = ? WHERE member_id = ?", (self.monsters.monster_str, self.player.id))
            self.db.commit()

            self.console_logic.Summon_Created_Console()

        await interaction.response.edit_message(embed=self.embed, view=self.console)
    




    # Selections -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    async def Monster_Summon_Selection_Callback(self, interaction: discord.Interaction):
        if await self.isnt_your_console(interaction):
            return

        self.summon_price = interaction.data['values'][0]

        self.console_logic.Monster_Summon_Console(self.summon_price)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
