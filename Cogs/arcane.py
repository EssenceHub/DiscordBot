import discord
import sqlite3
import random
import Factory.utils as utils
from discord import app_commands
from discord.ext import commands

# -------------------------------------------------------------------------------------------------------------

def guild_embed(guild_name):
    with sqlite3.connect('essence.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT guild_description, guild_invite, guild_leader, verified FROM EssenceArcaneGuildData WHERE guild_name = ?", (guild_name,))
        guild_description, guild_invite, guild_leader, verified = cursor.fetchone()

        if guild_leader == None:
            return discord.Embed(description="This guild doesn't exist, if you're sure it does try changing capitalization or checking the verified guild list.", colour=0x800080)
        else:
            verified = "" if verified == 0 else " ✅"

            guild_embed = discord.Embed(title=f"{guild_name}{verified}", description=guild_description, colour=0x800080)
            guild_embed.add_field(name="Leader:", value=f"<@{guild_leader}>")
            guild_embed.add_field(name="Discord Invite:", value=guild_invite)
            return guild_embed

# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

class Arcane(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Interact with other's in the world of Arcane Odyssey")
    async def arcane(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Arcane Odyssey", description="Interact with others across the world of Arcane Odyssey through Essence", colour=0x800080)
        await interaction.response.send_message(embed=embed, view=Menu(), ephemeral=True)
        
# -------------------------------------------------------------------------------------------------------------

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Duel")
    async def duel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = await utils.duel_queue(interaction)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Missions")
    async def missions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("This will bring up a missions UI", ephemeral=True)

    @discord.ui.button(label="Shops")
    async def shops(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Shops", description="Essence stores user created shops for you to browse through, search for something specific or find a random shop using the buttons below. Looking to sell or trade? Create your own!", colour=0x800080)
        await interaction.response.send_message(embed=embed, view=Shop(), ephemeral=True)
    
    @discord.ui.button(label="Guilds")
    async def tournament(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Guilds", description="Guilds are a key part of Arcane Odyssey, if you're not in a guild you're missing out on some of the best features Arcane Odyssey has to offer.", colour=0x800080)
        await interaction.response.send_message(embed=embed, view=Guilds(), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class Shop(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Random")
    async def random(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = utils.get_random_shop(interaction)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Search")
    async def search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ShopSearch())

    @discord.ui.button(label="Create")
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ShopCreate())

# -------------------------------------------------------------------------------------------------------------

class ShopSearch(discord.ui.Modal, title='Search for a shop'):

    term = discord.ui.TextInput(
        label='Search:',
        placeholder="What you're searching for...",
    )

    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            
            cursor.execute('SELECT member_id, shop_name, shop_details FROM EssenceArcaneUserData')
            shops = cursor.fetchall(); random.shuffle(shops)
            shop = utils.search_shops(shops, self.term.value)

            if shop == None:
                embed = discord.Embed(description=f"No shop exists with search term: {self.term.value}")
            else:
                embed = discord.Embed(title=shop[1], description=shop[2])
                shopkeeper = interaction.guild.get_member(shop[0])
                embed.set_author(name=f"Shopkeeper: {shopkeeper.name}#{shopkeeper.discriminator}")

            await interaction.response.send_message(embed=embed, ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class ShopCreate(discord.ui.Modal, title='Create/Edit your shop'):

    name = discord.ui.TextInput(
        label='Shop name:',
        placeholder='Name of your shop...',
    )

    details = discord.ui.TextInput(
        label='Shop details:',
        placeholder='Details of your shop (supports formatting)...',
        style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        has_shop = False
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            
            cursor.execute('SELECT shop_name, shop_details FROM EssenceArcaneUserData WHERE member_id = ?', (interaction.user.id,))
            shop_name, shop_details = cursor.fetchone() or (None, None)

            if shop_name != None and shop_details != None:
                has_shop = True
            
            shop_check = {
                True: "updated",
                False: "created"
            }
            
            if len(self.name.value) > 30:
                embed = discord.Embed(title="Error", description="Your shop name is too long")
                message = ''
            
            else:
                embed = discord.Embed(title=self.name.value, description=self.details.value)
                message = f"Your shop has been {shop_check[has_shop]}"

                if has_shop:
                    sql = "UPDATE EssenceArcaneUserData SET shop_name = ?, shop_details = ? WHERE member_id = ?"
                    val = (self.name.value, self.details.value, interaction.user.id)

                else:
                    sql = "INSERT INTO EssenceArcaneUserData(member_id, shop_name, shop_details) VALUES (?, ?, ?)"
                    val = (interaction.user.id, self.name.value, self.details.value)
                
                cursor.execute(sql, val)
                db.commit()

                embed.set_author(name=f"Shopkeeper: {interaction.user.name}#{interaction.user.discriminator}")
                await interaction.response.send_message(message, embed=embed, ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class Join():
    def __init__(self):
        super().__init__()

    def guild_archive():
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT guild_name, guild_description, guild_invite, guild_leader FROM EssenceArcaneGuildData WHERE verified = ?', (1,))
            leaderboard_guilds = cursor.fetchall(); random.shuffle(leaderboard_guilds)

            embed = discord.Embed(title="**Verified Guilds**", colour=0x800080)
            
            for leaderboard_guild in leaderboard_guilds:
                guild_name, guild_description, guild_invite, guild_leader = leaderboard_guild

                embed.add_field(name=f"-------------------------------\n{guild_name}", value=f"{guild_description} led by <@{guild_leader}>\n{guild_invite}", inline=False)

            return embed

# -------------------------------------------------------------------------------------------------------------

class Search(discord.ui.Modal, title='Search for a World of Magic Guild'):

    guild_name = discord.ui.TextInput(
        label='Guild name:',
        placeholder='Name of the guild you want to find here (Capital Sensitive)...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=guild_embed(self.guild_name.value), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class Create(discord.ui.Modal, title='Create a new entry in guild archive'):

    guild_name = discord.ui.TextInput(
        label='Guild name:',
        placeholder='Name of your guild... (Capital Sensitive)',
    )

    guild_description = discord.ui.TextInput(
        label='Guild Description:',
        placeholder="Your guild's description...",
    )

    guild_invite = discord.ui.TextInput(
        label='Guild Invite:',
        placeholder="Your guild's invite link...",
    )

    async def on_submit(self, interaction: discord.Interaction):

        guild_name = self.guild_name.value; guild_description = self.guild_description.value; guild_invite = self.guild_invite.value; guild_leader = interaction.user.id

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT guild_name FROM EssenceArcaneGuildData WHERE guild_name = ?', (guild_name,))
            existance_check = cursor.fetchone()
            if existance_check != None:
                await interaction.response.send_message("There is already a guild registered under that name, if that is your guild please message <@491289245974003722> to get it taken down.", ephemeral=True)
            elif len(guild_name) > 32:
                await interaction.response.send_message("Your guild name is unrealistically long", ephemeral=True)
            elif len(guild_description) > 300:
                await interaction.response.send_message("Your guild description is too long", ephemeral=True)
            elif len(guild_invite) > 32:
                await interaction.response.send_message("Your guild invite link is unrealistically long", ephemeral=True)
            else:
                sql = "INSERT INTO EssenceArcaneGuildData(guild_name, guild_description, guild_invite, guild_leader, verified) VALUES (?, ?, ?, ?, ?)"
                val = (guild_name, guild_description, guild_invite, guild_leader, 0)
                cursor.execute(sql, val)

                embed = discord.Embed(title=f"{guild_name} has been created.", description=guild_description, colour=0x800080)
                embed.add_field(name="Leader:", value=f"<@{guild_leader}>")
                embed.add_field(name="Discord Invite:", value=guild_invite)

                await interaction.response.send_message("Your guild has been created, to get it verified send a suggestion to the developer with /contact", embed=embed, ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class Edit(discord.ui.Modal, title='Edit your guild'):

    guild_name = discord.ui.TextInput(
        label='Guild name:',
        placeholder='Name of your guild... (Capital Sensitive)',
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()

            cursor.execute('SELECT guild_leader FROM EssenceArcaneGuildData WHERE guild_name = ?', (self.guild_name.value,))
            leader_check = cursor.fetchone()

            if leader_check == None:
                embed = discord.Embed(description="This guild doesn't exist, if you're sure it does try changing capitalization.", colour=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            elif leader_check[0] == interaction.user.id:
                if interaction.user.id == 491289245974003722:
                    embed = discord.Embed(description="What do you want to edit?", colour=0x800080)
                    await interaction.response.send_message(embed=embed, view=EditOptions(), ephemeral=True)
                else:
                    embed = discord.Embed(description="WIP", colour=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)


            else:
                embed = discord.Embed(description="You don't own this guild.", colour=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class EditOptions(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Name")
    async def name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameEditor())

    @discord.ui.button(label="Description")
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DescriptionEditor())
    
    @discord.ui.button(label="Image")
    async def image(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageEditor())
    
    @discord.ui.button(label="Leader")
    async def leader(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LeaderEditor())

    @discord.ui.button(label="Invite Link")
    async def invite_link(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(InviteEditor())

# -------------------------------------------------------------------------------------------------------------

class NameEditor(discord.ui.Modal, title='Edit your guild'):

    guild_name = discord.ui.TextInput(
        label='Guild Name:',
        placeholder="Your guild's new name... (Capital Sensitive)",
    )

    async def on_submit(self, interaction: discord.Interaction):
        if len(self.guild_name.value) > 32:
            await interaction.response.send_message("Your guild name is too long", ephemeral=True)
        else:
            print(self.guild_name.value, Edit.guild_name.value)
            with sqlite3.connect('essence.db') as db:
                cursor = db.cursor()
                sql = "UPDATE EssenceArcaneGuildData SET guild_name = ? WHERE guild_name = ?"
                val = (self.guild_name.value, Edit.guild_name.value)
                cursor.execute(sql, val)
                db.commit()
            await interaction.response.send_message("Your guild has been edited", embed=guild_embed(self.guild_name.value), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class DescriptionEditor(discord.ui.Modal, title='Edit your guild'):

    guild_description = discord.ui.TextInput(
        label='Guild Description:',
        placeholder="Your guild's new description...",
    )

    async def on_submit(self, interaction: discord.Interaction):
        if len(self.guild_description.value) > 300:
            await interaction.response.send_message("Your guild description is too long", ephemeral=True)
        else:
            with sqlite3.connect('essence.db') as db:
                cursor = db.cursor()
                sql = "UPDATE EssenceArcaneGuildData SET guild_description = ? WHERE guild_name = ?"
                val = (self.guild_description.value, Edit.guild_name.value)
                cursor.execute(sql, val)
                db.commit()
            await interaction.response.send_message("Your guild has been edited", embed=guild_embed(Edit.guild_name.value), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class ImageEditor(discord.ui.Modal, title='Edit your guild'):

    guild_image = discord.ui.TextInput(
        label='Guild Image:',
        placeholder="Your guild's new image... (link)",
    )

    async def on_submit(self, interaction: discord.Interaction):
        if len(self.guild_image.value) > 50:
            await interaction.response.send_message("Your guild image link is too long", ephemeral=True)
        else:
            with sqlite3.connect('essence.db') as db:
                cursor = db.cursor()
                sql = "UPDATE EssenceArcaneGuildData SET guild_image = ? WHERE guild_name = ?"
                val = (self.guild_image.value, Edit.guild_name.value)
                cursor.execute(sql, val)
                db.commit()
            await interaction.response.send_message("Your guild has been edited", embed=guild_embed(Edit.guild_name.value), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class LeaderEditor(discord.ui.Modal, title='Edit your guild'):

    guild_leader = discord.ui.TextInput(
        label='Guild Leader:',
        placeholder="Your guild's new leader... (user id)",
    )

    async def on_submit(self, interaction: discord.Interaction):
        if len(self.guild_leader.value) > 20:
            await interaction.response.send_message("Your guild leader's id is not that long", ephemeral=True)
        else:
            with sqlite3.connect('essence.db') as db:
                cursor = db.cursor()
                sql = "UPDATE EssenceArcaneGuildData SET guild_leader = ? WHERE guild_name = ?"
                val = (self.guild_leader.value, Edit.guild_name.value)
                cursor.execute(sql, val)
                db.commit()
            await interaction.response.send_message("Your guild has been edited, if you made a mistake you have to dm Essence staff. https://discord.gg/Fgyd22sB3g", embed=guild_embed(Edit.guild_name.value), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class InviteEditor(discord.ui.Modal, title='Edit your guild'):

    guild_invite = discord.ui.TextInput(
        label='Guild Invite:',
        placeholder="Your guild's new invite... (link)",
    )

    async def on_submit(self, interaction: discord.Interaction):
        if len(self.guild_invite.value) > 32:
            await interaction.response.send_message("Your guild invite link is too long", ephemeral=True)
        else:
            with sqlite3.connect('essence.db') as db:
                cursor = db.cursor()
                sql = "UPDATE EssenceArcaneGuildData SET guild_invite = ? WHERE guild_name = ?"
                val = (self.guild_invite.value, Edit.guild_name.value)
                cursor.execute(sql, val)
                db.commit()
            await interaction.response.send_message("Your guild has been edited", embed=guild_embed(Edit.guild_name.value), ephemeral=True)

# -------------------------------------------------------------------------------------------------------------

class Missions(discord.ui.View):
    def __init__(self):
        super().__init__()

# -------------------------------------------------------------------------------------------------------------

class Guilds(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=Join.guild_archive(), ephemeral=True)

    @discord.ui.button(label="Search")
    async def search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Search())

    @discord.ui.button(label="Create")
    async def missions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Create())
    
    @discord.ui.button(label="Edit")
    async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Edit())

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

async def setup(bot: commands.Bot):
    print("Arcane Loaded")
    await bot.add_cog(Arcane(bot))