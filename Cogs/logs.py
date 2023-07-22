import discord
import sqlite3
import asyncio
import Factory.utils as utils

from Factory.utils import ResponseButton

from Factory.WakeUp.logic import Logic

from datetime import datetime
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.vc_reward())
        # self.bot.loop.create_task(self.good_morning())
    
    async def good_morning(self):
        wake_up_prompts = open("Factory\WakeUp\prompts.txt", "r")
        day_of_year = datetime.now().timetuple().tm_yday


        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            pass
    
    async def vc_reward(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            # Activity Point Rewards for VC
            vc_members = utils.get_users_in_vc(self.bot)
            for member in vc_members:
                if not member.voice.self_deaf or member.voice.afk:
                    await utils.activity_reward(member, member.guild)

            await asyncio.sleep(60)
    
    @commands.Cog.listener() # Message edited
    async def on_message_edit(self, before, after):
        if before.guild == None or before.author.bot: # Makes sure the message wasn't sent in dms | Makes sure the message wasn't sent by a bot
            return

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
        
            # Guild Logs
            cursor.execute('SELECT logs_id FROM EssenceGuildData WHERE guild_id = ?', (before.guild.id,))
            logs_id = cursor.fetchone(); logs_id = logs_id[0]
            
            if logs_id != None:
                embed = discord.Embed(description=f"**Message edited\nBy: {before.author.mention}**", colour=0x00FF00)
                await self.bot.get_channel(logs_id).send(embed=embed)
    
    @commands.Cog.listener() # Message deleted
    async def on_message_delete(self, message: discord.Message):
        if message.guild == None or message.author.bot: # Makes sure the message wasn't sent in dms | Makes sure the message wasn't sent by a bot
            return
        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
        
            # Guild Logs
            cursor.execute('SELECT logs_id FROM EssenceGuildData WHERE guild_id = ?', (message.guild.id,))
            logs_id = cursor.fetchone(); logs_id = logs_id[0]

            if logs_id is not None:
                embed = discord.Embed(description=f"**Message deleted in <#{message.channel.id}> | {message.guild.name}\n```{message.content}```\nBy: {message.author.mention}**", colour=0xFF0000)
                await self.bot.get_channel(logs_id).send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        member = message.author
        guild = message.guild
        channel = message.channel

        if guild == None or member.bot: # Makes sure the message wasn't sent in dms, and is not a bot
            return

        with sqlite3.connect('essence.db') as db:
            cursor = db.cursor()
            
            cursor.execute('SELECT tws_id, counting_id, tod_id, logs_id FROM EssenceGuildData WHERE guild_id = ?', (guild.id,))
            tws_id, counting_id, tod_id, logs_id = cursor.fetchone() or (None, None, None, None)

            # Activity points tracker and reward
            activity_points = await utils.activity_reward(message.author, guild)
            
            # Guild Tracker
            cursor.execute('SELECT * FROM EssenceGuildData WHERE guild_id = ?', (guild.id,))
            guild_info = cursor.fetchone()
            
            if guild_info is None:
                sql = "INSERT INTO EssenceGuildData(guild_id) VALUES (?)"
                val = (guild.id,)
                cursor.execute(sql, val)
                db.commit()
            
            # Two word story
            if tws_id is not None:
                cursor.execute('SELECT tws_author, tws_state FROM EssenceGuildData WHERE guild_id = ?', (guild.id,))
                tws_author, tws_state = cursor.fetchone() or (None, None)

                if channel.id == tws_id:
                    sql, val = None, None

                    if tws_author == member.id: # If the user tries to send another two words it won't allow them
                        embed = discord.Embed(description=f"**{member} tried to hog the story**")
                        await message.delete()
                        await channel.send(embed=embed, delete_after=3)

                    elif message.content.lower() == 'the end': # Ends the story
                        await channel.purge(limit=2)
                        sql = "UPDATE EssenceGuildData SET tws_state = ?, tws_author = ? WHERE guild_id = ?"
                        val = (None, member.id, guild.id)
                        embed = discord.Embed(description=f'**"THE END", sent by {member}**\n```{tws_state}```\n\nIf you want to save the story, please copy it now!')
                        await channel.send(embed=embed)

                    elif not len(message.content.split()) == 2 or len(message.content) > 24: # If a user sends more than two words or a ridiculously long message it won't add to the story
                        await message.delete()
                        embed = discord.Embed(description=f"**{member} didn't say 2 words**")
                        await channel.send(embed=embed, delete_after=3)

                    else: # Adds the two words to the story
                        if tws_state == None:
                            tws_state = message.content
                        else:
                            tws_state = tws_state + ' ' + message.content
                        sql = "UPDATE EssenceGuildData SET tws_state = ?, tws_author = ? WHERE guild_id = ?"
                        val = (tws_state, member.id, guild.id)
                        await channel.purge(limit=2)
                        embed = discord.Embed(description=f"**Two word story:**```\n{tws_state}```\n**Last author: <@{member.id}>**")
                        await channel.send(embed=embed)

                    try:
                        cursor.execute(sql, val)
                        db.commit()
                    except TypeError:
                        pass

            # Counting
            if counting_id is not None:
                cursor.execute('SELECT counting_author, counting_state FROM EssenceGuildData WHERE guild_id = ?', (guild.id,))
                counting_author, counting_state = cursor.fetchone() or (None, None)
                
                if channel.id == counting_id:
                    counting_state = counting_state or 0
                    sql, val = None, None
                    syntax_error, nerd_check = False, False

                    for character in message.content:
                        if not str.isalnum(character):
                            nerd_check = True
                    
                    try:
                        count = utils.str_calc(message.content)
                    except:
                        syntax_error = True

                    if syntax_error:
                        await message.delete()

                    elif counting_author == member.id:
                        sql = "UPDATE EssenceGuildData SET counting_state = ? WHERE guild_id = ?"
                        val = (0, guild.id)
                        
                        embed = discord.Embed(description=f"**Double input from {member.mention}:\nTHE COUNT HAS BEEN RESET**")
                        await channel.send(embed=embed)

                    elif count != counting_state + 1:
                        sql = "UPDATE EssenceGuildData SET counting_state = ? WHERE guild_id = ?"
                        val = (0, guild.id)

                        embed = discord.Embed(description=f"**Wrong Number from {member.mention}:\nTHE COUNT HAS BEEN RESET**")
                        await channel.send(embed=embed)

                    else:
                        sql = "UPDATE EssenceGuildData SET counting_state = ?, counting_author = ? WHERE guild_id = ?"
                        val = (counting_state + 1, member.id, guild.id)

                        reactions = {
                            100: "⭐",
                            1_000: "🌟",
                            10_000: "☄️",
                            100_000: "👑"
                        }

                        reaction = reactions.get(count, "✅")
                        await message.add_reaction(reaction)

                        if nerd_check:
                            await message.add_reaction("🧠")
                    
                    try:
                        cursor.execute(sql, val)
                        db.commit()
                    except TypeError:
                        pass
            
            # Truth or dare
            if tod_id is not None and channel.id == tod_id:
                if str.lower(message.content) == "truth":
                    truth_question = await utils.get_truth_question(message)
                    await channel.send(embed=truth_question, view=ResponseButton())

                elif str.lower(message.content) == "dare":
                    dare_question = await utils.get_dare_prompt(message)
                    await channel.send(embed=dare_question, view=ResponseButton())

                else:
                    embed = discord.Embed(title="Truth or Dare", description="To use this channel, say 'truth' for a truth prompt or 'dare' for a dare prompt. You can respond to a prompt by pressing the blue button!")
                    await channel.send(embed=embed, delete_after=5)
                
                await message.delete()
                    
            if logs_id is not None:
                logs_channel = self.bot.get_channel(logs_id)
                await utils.log_message(logs_channel, message)
    
async def setup(bot: commands.Bot):
    print("Logs Loaded")
    await bot.add_cog(Logs(bot))