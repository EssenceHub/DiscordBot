import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class PartyMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="Join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PartyJoin())

    @discord.ui.button(label="Create")
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PartyCreation())

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class PartyInfo(discord.ui.View):
    def __init__(self):
        super().__init__()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    @discord.ui.button(label="Daily")
    async def daily(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        current_timestamp = round(datetime.now().timestamp())

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT party_points FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party_points = cursor.fetchone()

            if party_points != None:
                party_points = party_points[0]
            else:
                party_points = 0

            cursor.execute('SELECT last_point FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            last_point = cursor.fetchone()

            if last_point != None:
                last_point = last_point[0]
            else:
                last_point = 0

            if last_point + 86400 < current_timestamp:
                sql = "UPDATE EssenceUserData SET party_points = ?, last_point = ? WHERE member_id = ? AND guild_id = ?"
                val = (party_points + 1, current_timestamp, member.id, interaction.guild.id)
                cursor.execute(sql, val)
                embed = discord.Embed(title=f"Party Daily", description=f"You've collected your daily party point.", color=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = discord.Embed(title=f"Cooldown", description=f"You've done enough partying today!", color=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    @discord.ui.button(label="Members")
    async def members(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        members = ''

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT party FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party = cursor.fetchone()
            if party != None:
                party = party[0]

            cursor.execute('SELECT member_id FROM EssenceUserData WHERE guild_id = ? AND party = ?', (interaction.guild.id, party))
            party_members = cursor.fetchall(); party_members = party_members[0]
            for member in party_members:
                members = members + f"<@{member}>\n"
            embed = discord.Embed(title=f"Members of {party}", description=members, color=0x800080)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    @discord.ui.button(label="Leave")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT party FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party = cursor.fetchone()
            if party != None:
                party = party[0]
            cursor.execute('SELECT party_rank FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party_rank = cursor.fetchone()
            if party_rank != None:
                party_rank = party_rank[0]
            if party == None:
                embed = discord.Embed(title=f"Loneliness detected", description=f"You can't leave a party without first joining one!")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if party_rank != 5:
                    sql = "UPDATE EssenceUserData SET party = ?, party_rank = ? WHERE member_id = ? AND guild_id = ?"
                    val = (None, None, member.id, interaction.guild.id)
                    cursor.execute(sql, val)
                    embed = discord.Embed(title=f"Loneliness achieved", description=f"You've left party {party}.")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    sql = "UPDATE EssenceUserData SET party = ?, party_rank = ? WHERE party = ? AND guild_id = ?"
                    val = (None, None, party, interaction.guild.id)
                    cursor.execute(sql, val)
                    cursor.execute('DELETE FROM EssencePartyData WHERE guild_id = ? AND name = ?', (interaction.guild.id, party))
                    embed = discord.Embed(title=f"Loneliness achieved", description=f"You've left party {party}. You were the party leader so now everyone is lonely.")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

    @discord.ui.button(label="Settings")
    async def settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT party_rank FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party_rank = cursor.fetchone()
            if party_rank != None:
                party_rank = party_rank[0]
            if party_rank == 4 or 5:
                embed = discord.Embed(title=f"Settings:")
                await interaction.response.send_message(embed=embed, view=LeaderSettings(), ephemeral=True)
            else:
                embed = discord.Embed(title=f"WIP")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                # embed = discord.Embed(title=f"Settings:", description=f"-")
                # await interaction.response.send_message(embed=embed, view=MemberSettings(), ephemeral=True)
            


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class LeaderSettings(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Configure")
    async def configure(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user

    @discord.ui.button(label="Promote")
    async def promote(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
    
    @discord.ui.button(label="Demote")
    async def demote(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
    
    @discord.ui.button(label="Kick")
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class MemberSettings(discord.ui.View):
    def __init__(self):
        super().__init__()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class Shop(discord.ui.View):
    pass

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class PartyCreation(discord.ui.Modal, title='Party Creation'):
    name = discord.ui.TextInput(
        label='Party name:',
        placeholder='Your party name here...',
    )

    description = discord.ui.TextInput(
        label='Party Description:',
        style=discord.TextStyle.long,
        placeholder='Type your party description here...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.user
        party_taken = False

        # PREVENT LONG PARTY NAMES
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT name FROM EssencePartyData WHERE guild_id = ?', (interaction.guild.id,))
            party_name_stored = cursor.fetchall()
            cursor.execute('SELECT party FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party = cursor.fetchone()
            if party != None:
                party = party[0]
            if party == None:
                for stored_party in party_name_stored:
                    if str.lower(stored_party[0]) == str.lower(self.name.value):
                        party_taken = True
                if party_name_stored == None or not party_taken:
                    sql = "UPDATE EssenceUserData SET party = ?, party_rank = ? WHERE member_id = ? AND guild_id = ?"
                    val = (self.name.value, 5, member.id, interaction.guild.id)
                    cursor.execute(sql, val)
                    
                    sql = "INSERT INTO EssencePartyData(guild_id, name, description, leader_id, rank_5, rank_4, rank_3, rank_2, rank_1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    val = (interaction.guild.id, self.name.value, self.description.value, member.id, "Leader", "Officer", "Honorary Member", "Member", "Recruit")
                    cursor.execute(sql, val)
                    db.commit()

                    embed = discord.Embed(title=f"Party __{self.name.value}__ created", description=f"{self.name.value} is now registered as a party under your leadership, good luck!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"Party {self.name.value}", description=f"{self.name.value} is taken by a different user on this server.")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
            else:
                embed = discord.Embed(title=f"Want to leave your party?", description="You can't create a party while in another party!")
                await interaction.response.send_message(embed=embed, ephemeral=True)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class PartyJoin(discord.ui.Modal, title='Join a party'):
    name = discord.ui.TextInput(
        label='Party name:',
        placeholder='Name of the party you want to join here (Capital Sensitive)...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        member = interaction.user

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT party FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party = cursor.fetchone()
            if party != None:
                party = party[0]
            if party == None:
                cursor.execute('SELECT name FROM EssencePartyData WHERE name = ? and guild_id = ?', (self.name.value, interaction.guild.id))
                stored_party_name = cursor.fetchone()
                if stored_party_name != None:
                    stored_party_name = stored_party_name[0]
                
                if stored_party_name == self.name.value:
                    sql = "UPDATE EssenceUserData SET party = ?, party_rank = ? WHERE member_id = ? AND guild_id = ?"
                    val = (stored_party_name, 1, member.id, interaction.guild.id)
                    cursor.execute(sql, val)
                    embed = discord.Embed(title=f"Welcome to the party", description=f"You've joined {stored_party_name}!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"Party not found", description=f"There is no party in this server named {self.name.value}!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                embed = discord.Embed(title=f"Leave party?")
                embed.add_field(value="You can't join a party while in another party!")
                await interaction.response.send_message(embed=embed, ephemeral=True)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class Party(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    @app_commands.command(description="Interact with other users and work together to build a party")
    async def party(self, interaction: discord.Interaction):
        member = interaction.user

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT party FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (interaction.guild.id, member.id))
            party = cursor.fetchone()

            if party[0] == None:
                embed = discord.Embed(title="Parties", description="Parties are groups of members that band together during server events and create something awesome.")
                await interaction.response.send_message(embed=embed, view=PartyMenu(), ephemeral=True)
            else:
                party = party[0]
                cursor.execute('SELECT description FROM EssencePartyData WHERE guild_id = ? AND name = ?', (interaction.guild.id, party))
                description = cursor.fetchone()
                if description != None:
                    description = description[0]

                embed = discord.Embed(title=f"Party: {party}", description=f"Description: {description}")
                await interaction.response.send_message(embed=embed, view=PartyInfo(), ephemeral=True)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

async def setup(bot: commands.Bot):
    print("Party Loaded")
    await bot.add_cog(Party(bot))