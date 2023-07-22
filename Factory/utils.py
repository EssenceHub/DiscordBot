import discord
import sqlite3
import random
import numexpr as calc
from datetime import datetime
from discord.ext import commands

def has_lower_role(member, roles):
    member_roles = [r.position for r in member.roles]
    for role in roles:
        if role.position not in member_roles or min(member_roles) > role.position:
            return False
    return True

async def get_truth_question(message: discord.Message):
    with sqlite3.connect('essence.db') as db:
        cursor = db.cursor()
        truth_questions = open('Extra/truth.txt', 'r').readlines()
        cursor.execute('SELECT tod_truth FROM EssenceGuildData WHERE guild_id = ?', (message.guild.id,))
        line = cursor.fetchone()
        line = line[0] or 0
        
        if line >= len(truth_questions):
            line = 0
        else:
            line += 1
        cursor.execute("UPDATE EssenceGuildData SET tod_truth = ? WHERE guild_id = ?", (line, message.guild.id))

        embed = discord.Embed(title=f"TRUTH | {truth_questions[line]}")
        return embed

async def get_dare_prompt(message: discord.Message):
    with sqlite3.connect('essence.db') as db:
        cursor = db.cursor()
        dare_questions = open('Extra/dare.txt', 'r').readlines()
        cursor.execute('SELECT tod_dare FROM EssenceGuildData WHERE guild_id = ?', (message.guild.id,))
        line = cursor.fetchone()
        line = line[0] or 0
        
        if line >= len(dare_questions):
            line = 0
        else:
            line += 1
        cursor.execute("UPDATE EssenceGuildData SET tod_dare = ? WHERE guild_id = ?", (line, message.guild.id))

        embed = discord.Embed(title=f"DARE | {dare_questions[line]}")
        return embed

def get_users_in_vc(bot: commands.Bot):
    users = []
    for guild in bot.guilds:
        for voice_channel in guild.voice_channels:
            for member in voice_channel.members:
                if not member.voice.self_deaf or member.voice.afk:
                    users.append(member)
    return users

def str_calc(expr: str):
    expr = expr.replace("^", "**")
    return float(calc.evaluate(expr))

async def activity_reward(user: discord.User, guild: discord.Guild):
    with sqlite3.connect('essence.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT activity_points FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (guild.id, user.id))
        activity_points = cursor.fetchone()

        if activity_points == None:
            activity_points = 1
            sql = "INSERT INTO EssenceUserData(guild_id, member_id, activity_points) VALUES (?, ?, ?)"
            val = (guild.id, user.id, 1)

        else:
            activity_points = activity_points[0] + 1
            sql = "UPDATE EssenceUserData SET activity_points = ? WHERE member_id = ? AND guild_id = ?"
            val = (activity_points, user.id, guild.id)

        cursor.execute(sql, val)
        db.commit()

        await reward_roles(guild, user, activity_points)
        return activity_points

async def duel_queue(interaction: discord.Interaction):
    with open('Extra/duel.txt', 'r+') as file:
        contents = file.read()

        if contents == '':
            file.write(str(interaction.user.id))
            desc = "You've been added to the duel queue, please wait for someone else to queue."
            embed = discord.Embed(title="DUEL", description=desc)

        elif contents == str(interaction.user.id):
            embed = discord.Embed(title="DUEL", description="You are already queued for a duel, please wait for someone else to queue.")

        else:
            file.write('')
            queued_user = interaction.client.get_user(int(contents))
            dm_channel = await queued_user.create_dm()
            embed = discord.Embed(title="DUEL", description=f"You have been queued for a duel with <@{queued_user.id}>")
            await dm_channel.send(f"You have been queued for a duel with <@{interaction.user.id}>")

    return embed

def get_random_shop(interaction: discord.Interaction):
    with sqlite3.connect('essence.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT member_id, shop_name, shop_details FROM EssenceArcaneUserData")
        shops = cursor.fetchall()
        shop_number = random.randint(0, len(shops) - 1); shop_info = shops[shop_number]

        shopkeeper, shop_name, shop_details = shop_info
        shopkeeper = interaction.guild.get_member(shopkeeper)

        embed = discord.Embed(title=shop_name, description=shop_details)
        embed.set_author(name=f"Shopkeeper: {shopkeeper.name}#{shopkeeper.discriminator}")

    return embed

def search_shops(shops: list, term: str):
    lower_term = str.lower(term)
    for shop in shops:
        for info in shop:
            if not type(info) == int:
                lower_info = str.lower(info)
                if not str.find(lower_info, lower_term) == -1:
                    return shop
    
    return None

async def reload_response_buttons(bot):
    with sqlite3.connect('essence.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT tod_id, guild_id FROM EssenceGuildData')
        guild_info = cursor.fetchall()

        # Truth or Dare Update
        for info in guild_info:
            guild_tod_id = info[0]

            if guild_tod_id is not None:
                tod_channel = bot.get_channel(guild_tod_id)

                if tod_channel:
                    async for message in tod_channel.history(limit=10):
                        bot.add_view(ResponseButton(), message_id=message.id)

class Response(discord.ui.Modal, title="Truth"):
    
    response = discord.ui.TextInput(
        label='Response:',
        placeholder='...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        message = interaction.message
        embeds = message.embeds
        responded = False
        for field in embeds[0].fields:
            response_id = str.split(field.value, "- <@"); response_id = response_id[1]
            response_id = str.split(response_id, ">"); response_id = int(response_id[0])
            if response_id == interaction.user.id:
                responded = True
        if responded:
            embed = discord.Embed(title="Responded", description="You already responded to that prompt, if you'd like to keep participating please say 'truth' or 'dare' to create a new prompt")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            response = str.replace(self.response.value, "`", "")
            embeds[0].add_field(name="Response:", value=f"{response}\n- {interaction.user.mention}")
            await interaction.response.edit_message(embed=embeds[0], view=ResponseButton())

class ResponseButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Respond", style=discord.ButtonStyle.blurple, custom_id="response")
    async def purge_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Response())

def capitalize_words(string):
    return ' '.join(word.capitalize() for word in string.split())

async def reward_roles(guild: discord.Guild, member: discord.Member, activity_points: int):
    db = sqlite3.connect('essence.db')
    cursor = db.cursor()
    # Activity Rewards
    rewards = {}

    # Retrieve reward roles from the database
    sql = "SELECT role_id, requirement FROM EssenceRoleData WHERE guild_id = ? AND self_assignable != ?"
    val = (guild.id, 1)
    cursor.execute(sql, val)
    reward_roles = cursor.fetchall()

    # Create a dictionary of reward roles and their requirements
    for role_info in reward_roles:
        role = guild.get_role(role_info[0])
        rewards[role_info[0]] = [role, role_info[1]]

    # removal reasons
    remove_reason = "Removing old reward role"
    add_reason = "Adding new reward role"

    # Variable Init
    highest_role = None
    highest_requirement = -1

    # Iterate through the rewards dictionary
    for _, role_info in rewards.items():
        role, requirement = role_info
        
        # Check if the user meets the requirement for the role
        if activity_points >= requirement and requirement >= highest_requirement:
            highest_role = role
            highest_requirement = requirement
            
        # Prevents adding a smaller role if you already have a bigger one
        elif requirement > highest_requirement and role in member.roles:
            highest_role = role
            highest_requirement = requirement

    # Assign the highest role to the user and remove any older roles
    if highest_role:
        for _, role_info in rewards.items():
            role, requirement = role_info

            # Removes all lower requirement roles
            if requirement < highest_requirement and role in member.roles:
                await member.remove_roles(role, reason=remove_reason)

        # Adds the highest role a user should have if they don't have it
        if highest_role not in member.roles:
            await member.add_roles(highest_role, reason=add_reason)

async def log_message(channel: discord.TextChannel, message: discord.Message):
    cursor = sqlite3.connect('essence.db').cursor

    embed = discord.Embed(description=f"**Message sent in <#{message.channel.id}> | {message.guild.name}**\n{message.content}\nBy: {message.author.mention}", colour=0x0000FF)

    image_urls = [attachment.url for attachment in message.attachments if str.lower(attachment.url).endswith(('jpg', 'jpeg', 'png', 'gif'))]

    if image_urls:
        embed.set_image(url=image_urls[0])
        if len(image_urls) > 1:
            embed.add_field(name="Other images", value='\n'.join(image_urls[1:]))

    try:
        await channel.send(embed=embed)
    except discord.errors.Forbidden:
        print('No access to ' + channel.name + "\n Message if you're curious:\n\n" + message)