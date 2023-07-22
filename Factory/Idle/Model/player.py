import discord
import sqlite3

from datetime import datetime

class Player:
    def __init__(self, interaction: discord.Interaction):
        self.timestamp = round(datetime.now().timestamp())
        self.interaction = interaction
        self.id = interaction.user.id
        self.db = sqlite3.connect("essence.db")
        self.cursor = self.db.cursor()

        self.update_player_data()

    def update_player_data(self):

        # SQL
        default = (None, None, None, 1, None, 10, 0, self.timestamp)
        self.cursor.execute(f"SELECT member_id, character_name, dungeon_name, character_level, dungeon_monsters, dungeon_energy, dungeon_power, last_assault FROM EssenceIdleData WHERE member_id = {self.interaction.user.id}")
        self.stored_id, self.character_name, self.dungeon_name, self.character_level, self.dungeon_monsters, self.dungeon_energy, self.dungeon_power, self.last_assault = self.cursor.fetchone() or default

        self.dungeons = self.count_dungeons()

    def update_dungeon(self):
        if self.dungeon_power == 0:
            return

        # Logic
        recent_assault = round(datetime.now().timestamp())
        time_elapsed = (recent_assault - self.last_assault)
        assault_damage = time_elapsed * self.character_level

        if assault_damage > self.dungeon_power:
            assault_damage = self.dungeon_power

        reward = assault_damage * 2

        # Update dungeon values in player object
        self.dungeon_energy = round(self.dungeon_energy + reward)
        self.dungeon_power = round(self.dungeon_power - assault_damage)
        self.last_assault = recent_assault

        # SQL
        sql = "UPDATE EssenceIdleData SET dungeon_energy = ?, dungeon_power = ?, last_assault = ? WHERE member_id = ?"
        val = (self.dungeon_energy, self.dungeon_power, recent_assault, self.id)
        self.cursor.execute(sql, val)
        self.db.commit()
    
    def increase_dungeon_power(self, amount: str):
        amount = int(amount)
        if self.dungeon_energy < amount:
            return "Insufficient Energy"
        
        # Logic
        self.dungeon_energy = self.dungeon_energy - amount
        self.dungeon_power = self.dungeon_power + amount

        # SQL
        sql = "UPDATE EssenceIdleData SET dungeon_energy = ?, dungeon_power = ? WHERE member_id = ?"
        val = (self.dungeon_energy, self.dungeon_power, self.id)
        self.cursor.execute(sql, val)
        self.db.commit()
        return f"Summon increased power by {amount}"
    
    def count_dungeons(self):
        if self.dungeon_name is None:
            return 0
        else:
            return 1