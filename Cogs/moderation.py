# This file will be for staff configuration
import discord
import sqlite3
from discord import app_commands, ui
from discord.ext import commands
from datetime import datetime
from datetime import timedelta

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Command cog class
class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(description="Moderation Options")
    async def moderation(self, interaction: discord.Interaction):
        permissions = interaction.user.guild_permissions
        if permissions.manage_channels or permissions.manage_roles or permissions.view_audit_log or permissions.view_guild_insights or permissions.manage_guild or permissions.manage_nicknames or permissions.kick_members or permissions.ban_members or permissions.moderate_members or permissions.mention_everyone or permissions.manage_messages or permissions.manage_threads or permissions.mute_members or permissions.deafen_members or permissions.manage_events or permissions.administrator:
            embed = discord.Embed(title="Moderation", description="""
            **Purge**\n
            Removes a specific amount of messages from the channel where the moderation 
            command was sent. Can also specify a certain member's messages.\n
            -------------------------------------------------------------------------------\n
            **Punish**\n
            A stored number is applied to every user which will dictate how harsh their punishment will be: 
            1 infraction -> warn. 2 infractions -> warn. 3 infractions -> timeout for 3 days. 4 infractions -> timeout for 1 week. 5 infractions -> ban\n
            -------------------------------------------------------------------------------\n
            **Pardon**\n
            Lowers the users stored punishment value by 1 if they do something good or appeal!""", color=0x800080)
            await interaction.response.send_message(embed=embed, view=ModerationCommands(), ephemeral=True)
        else:
            embed = discord.Embed(title="Moderation", description="You do not have permission to moderate this server", color=0x800080)
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(description="Contact staff")
    async def contact(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Contact", description=f"Contact the Staff in {interaction.guild.name} or the Developer of <@920471516817260564>", color=0x800080)
        await interaction.response.send_message(embed=embed, view=Contact(self.bot), ephemeral=True)
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

class ModerationCommands(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Purge", style=discord.ButtonStyle.blurple)
    async def purge_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Purge())

    @discord.ui.button(label="Punish", style=discord.ButtonStyle.danger)
    async def punish_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Punish())

    @discord.ui.button(label="Pardon", style=discord.ButtonStyle.green)
    async def pardon_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Pardon())

class Purge(discord.ui.Modal, title='Punishment'):

    amount = discord.ui.TextInput(
        label='Amount:',
        placeholder='Number of messages to delete...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Deleted", description=f"{self.amount.value} messages have been deleted in this channel", color=0x800080)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.channel.purge(limit=int(self.amount.value))

class Punish(discord.ui.Modal, title='Punishment'):

    user = discord.ui.TextInput(
        label="User's ID:",
        placeholder='ID...',
    )

    reason = discord.ui.TextInput(
        label='Reason:',
        placeholder='reason...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect("essence.db") as db:
            cursor = db.cursor()
            member = interaction.guild.get_member(int(self.user.value))
            guild = interaction.guild

            cursor.execute("SELECT user_punishments FROM EssenceUserData WHERE member_id = ? AND guild_id = ?", (self.user.value, guild.id))
            punishment_number = cursor.fetchone()
            if punishment_number is None:
                punishment_number = 1
            else:
                punishment_number = punishment_number[0] + 1

            cursor.execute("SELECT punishment1, punishment2, punishment3, punishment4, punishment5 FROM EssenceGuildData WHERE guild_id = ?", (interaction.guild.id,))
            stored_punishments = cursor.fetchall(); stored_punishments = stored_punishments[0]

            punishment = {
                1: stored_punishments[0] or "warn",
                2: stored_punishments[1] or "warn",
                3: stored_punishments[2] or "timeout3d",
                4: stored_punishments[3] or "timeout1w",
                5: stored_punishments[4] or "ban"
            }

            punishment = punishment[punishment_number]

            if punishment == "warn":
                if interaction.user.guild_permissions.kick_members:
                    embed = discord.Embed(title="Warned", description=f"<@{self.user.value}> has been warned for {self.reason.value} ({punishment_number} punishments)", color=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    sql = "UPDATE EssenceUserData SET user_punishments = ? WHERE member_id = ? AND guild_id = ?"
                    val = (punishment_number, self.user.value, guild.id)
                    cursor.execute(sql, val)
                    db.commit()
                else:
                    embed = discord.Embed(title="Insufficient Authority", description=f"You do not have the ability to warn members, you need atleast 'kick members' permissions to do this.", color=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            elif str.startswith(punishment, "timeout"):
                punishment_time = str.split(punishment, "t"); punishment_time = punishment_time[2]
                number = ''
                letter = ''
                for character in punishment_time:
                    if str.isdigit(character):
                        number = number + character
                    else:
                        letter = character
                punishment_time = int(number)

                if interaction.user.guild_permissions.moderate_members:
                    try:
                        if letter == "h":
                            await member.timeout(timedelta(hours=punishment_time), reason=f"{self.reason.value} ({punishment_number} punishments)")
                        elif letter == "d":
                            await member.timeout(timedelta(days=punishment_time), reason=f"{self.reason.value} ({punishment_number} punishments)")
                        elif letter == "w":
                            await member.timeout(timedelta(weeks=punishment_time), reason=f"{self.reason.value} ({punishment_number} punishments)")
                        else:
                            await interaction.response.send_message(f"THERES A PROBLEM WITH YOUR PUNISHMENT FOR PUNISHMENT {punishment_number}")
                    except discord.errors.Forbidden:
                        embed = discord.Embed(title="This user is unpunishable", description=f"<@{self.user.value}> has caused an issue during punishment, likely means they have a higher authority than me.", color=0x800080)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return


                    embed = discord.Embed(title="Punished", description=f"<@{self.user.value}> has been given a {punishment_time}{letter} timeout for {self.reason.value}", color=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    sql = "UPDATE EssenceUserData SET user_punishments = ? WHERE member_id = ? AND guild_id = ?"
                    val = (punishment_number, self.user.value, guild.id)
                    cursor.execute(sql, val)
                    db.commit()
                else:
                    embed = discord.Embed(title="Insufficient Authority", description=f"You do not have the ability to timeout members.", color=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            elif punishment == "ban":
                if interaction.user.guild_permissions.ban_members:
                    await member.ban(reason=f"{self.reason.value} ({punishment_number} punishments)")
                    embed = discord.Embed(title="Timeout", description=f"<@{self.user.value}> has banned for {self.reason.value}", color=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="Insufficient Authority", description=f"You do not have the ability to ban members.", color=0x800080)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            embed_placeholder_string = str.split(embed.description, "has")
            embed_placeholder_string = embed_placeholder_string[1]
            embed.description = "You have" + embed_placeholder_string + " in " + interaction.guild.name
            dm_channel = await member.create_dm()
            await dm_channel.send(embed=embed)

class Pardon(discord.ui.Modal, title='Pardon'):

    user = discord.ui.TextInput(
        label='User:',
        placeholder='ID...',
    )

    reason = discord.ui.TextInput(
        label='Reason:',
        placeholder='reason...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect("essence.db") as db:
            cursor = db.cursor()
            member = interaction.guild.get_member(int(self.user.value))
            guild = interaction.guild
            cursor.execute("SELECT user_punishments FROM EssenceUserData WHERE member_id = ? AND guild_id = ?", (self.user.value, guild.id))
            punishments = cursor.fetchone(); punishments = punishments[0]
            if punishments == None or punishments == 0:
                embed = discord.Embed(title="Innocent", description=f"That user is innocent", color=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                sql = "UPDATE EssenceUserData SET user_punishments = ? WHERE member_id = ? AND guild_id = ?"
                val = (punishments - 1, self.user.value, guild.id)
                cursor.execute(sql, val)
                db.commit()
                embed = discord.Embed(title="Pardoned", description=f"Pardoned <@{self.user.value}>, they have {punishments - 1} strikes now.", color=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                dm_channel = await member.create_dm()
                embed = discord.Embed(title="Pardoned", description=f"You have been pardoned of 1 strike for {self.reason.value}", color=0x800080)
                await dm_channel.send(embed=embed)

class Contact(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @discord.ui.button(label="Staff", style=discord.ButtonStyle.blurple)
    async def staff_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT mail_id FROM EssenceGuildData WHERE guild_id = ?', (interaction.guild.id,))
            mail_id = cursor.fetchone()
            if mail_id == None:
                embed = discord.Embed(title=f"Contact {interaction.guild.name} Staff", description="This server doesn't have an inbox", color=0x800080)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title=f"Contact {interaction.guild.name} Staff", description="Suggest an addition to the server or report a malicious user.", color=0x800080)
                await interaction.response.send_message(embed=embed, view=StaffContact(), ephemeral=True)

    @discord.ui.button(label="Developer", style=discord.ButtonStyle.danger)
    async def developer_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f"Contact the Bot Developer", description="Suggest an addition to the Essence bot, report a bug or join the Essence bot's discord server.", color=0x800080)
        await interaction.response.send_message(embed=embed, view=DeveloperContact(self.bot), ephemeral=True)

class StaffContact(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Suggest", style=discord.ButtonStyle.blurple)
    async def staff_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffSuggest())

    @discord.ui.button(label="Report User", style=discord.ButtonStyle.danger)
    async def developer_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffReport())

class StaffSuggest(discord.ui.Modal, title="Suggest"):

    suggestion = discord.ui.TextInput(
        label='Suggestion:',
        placeholder= '...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT mail_id FROM EssenceGuildData WHERE guild_id = ?', (interaction.guild.id,))
            mail_id = cursor.fetchone(); mail_id = mail_id[0]
            inbox = await interaction.guild.fetch_channel(mail_id)
            embed = discord.Embed(title="Suggestion", description=self.suggestion.value + " **suggested by** " + interaction.user.mention, color=0x800080)
            await inbox.send(embed=embed)
            embed.description = "Successfully Submitted!"
            await interaction.response.send_message(embed=embed, ephemeral=True)

class StaffReport(discord.ui.Modal, title="Report"):

    user = discord.ui.TextInput(
        label='User:',
        placeholder='ID...',
    )

    reason = discord.ui.TextInput(
        label='Reason:',
        placeholder='reason...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT mail_id FROM EssenceGuildData WHERE guild_id = ?', (interaction.guild.id,))
            mail_id = cursor.fetchone(); mail_id = mail_id[0]
            inbox = await interaction.guild.fetch_channel(mail_id)
            embed = discord.Embed(title="Report", description=f"<@{self.user.value}> **reported for** {self.reason.value} **reported by** {interaction.user.mention}", color=0x800080)
            await inbox.send(embed=embed)
            embed.description = "Successfully Submitted!"
            await interaction.response.send_message(embed=embed, ephemeral=True)

class DeveloperContact(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @discord.ui.button(label="Suggest", style=discord.ButtonStyle.blurple)
    async def staff_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeveloperSuggest(self.bot))

    @discord.ui.button(label="Report Bug", style=discord.ButtonStyle.danger)
    async def developer_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeveloperBugReport(self.bot))

    @discord.ui.button(label="Support", style=discord.ButtonStyle.green)
    async def support_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("discord.gg/Fgyd22sB3g", ephemeral=True)

class DeveloperSuggest(discord.ui.Modal, title="Suggest"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    suggestion = discord.ui.TextInput(
        label='Suggestion:',
        placeholder= '...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        inbox = self.bot.get_channel(927368289821294612)
        embed = discord.Embed(title="Suggestion", description=self.suggestion.value + " **suggested by** " + interaction.user.mention, color=0x800080)
        await inbox.send(embed=embed)
        embed.description = "Successfully Submitted!"
        await interaction.response.send_message(embed=embed, ephemeral=True)

class DeveloperBugReport(discord.ui.Modal, title="Bug Report"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    bug = discord.ui.TextInput(
        label='Bug:',
        placeholder='...',
    )

    details = discord.ui.TextInput(
        label='Details:',
        placeholder='...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        inbox = self.bot.get_channel(927368289821294612)
        embed = discord.Embed(title="Bug Report", description=self.bug.value + " **caused by** " + self.details.value + " **reported by** " + interaction.user.mention, color=0x800080)
        await inbox.send(embed=embed)
        embed.description = "Successfully Submitted!"
        await interaction.response.send_message(embed=embed, ephemeral=True)


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Setup function
async def setup(bot: commands.Bot):
    print("Moderation Loaded")
    await bot.add_cog(Moderation(bot))