import discord
import sqlite3

class Data:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.guild = interaction.guild
        self.user = interaction.user

        self.db = sqlite3.connect("essence.db")
        self.cursor = self.db.cursor()

        self.get_roles()
    
    def get_roles(self):
        self.cursor.execute("SELECT role_id, description FROM EssenceRoleData WHERE guild_id = ? AND self_assignable = ?", (self.guild.id, 1))
        self.roles = self.cursor.fetchall()

        self.role_str = self.get_role_str()
        self.role_options = self.get_role_options()

    def get_role_str(self):
        self.role_str = "**Choices:**"
        for role_id, role_desc in self.roles:
            role = self.guild.get_role(role_id)
            self.role_str = f"{self.role_str}\n{role.mention}: {role_desc}"
        return self.role_str

    def get_role_options(self):
        self.role_options = []
        for role_id, role_desc in self.roles:
            role = self.guild.get_role(role_id)

            option = discord.SelectOption(label=role.name, description=role_desc)
            self.role_options.append(option)
        return self.role_options
