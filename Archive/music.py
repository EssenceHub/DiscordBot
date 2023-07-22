from operator import truediv
import discord
import Factory.lfm_utils as lastfm
from discord import app_commands
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Search an album')
    async def album(self, interaction: discord.Interaction, album: str, artist: str):
        album_info = lastfm.album_search(album, artist)
        embed = discord.Embed(title=album_info['name'], description=album_info['url'])
        embed.add_field(name="Tracks", value=lastfm.get_album_tracks(album, artist), inline=True)
        embed.add_field(name="Tags", value=lastfm.get_album_tags(album, artist), inline=True)
        embed.set_author(name=album_info['artist'])
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        embed.set_thumbnail(url=album_info['image'][len(album_info['image']) - 1]['#text'])
        await interaction.response.send_message(embed=embed, ephemeral=True)
            
            
    @app_commands.command(description='Search an artist')
    async def artist(self, interaction: discord.Interaction, artist: str):
        artist_info = lastfm.artist_search(artist)
        description = artist_info['bio']['summary']
        top_song = lastfm.get_artist_top_songs(artist)
        top_album = lastfm.get_artist_top_albums(artist)
        embed = discord.Embed(title=artist_info['name'], description=description.split('<', 1)[0], url=artist_info['url'])
        embed.add_field(name="Top Song", value=top_song[0]['name'], inline=True)
        embed.add_field(name="Top Album", value=top_album[0]['name'], inline=True)
        embed.set_author(name=artist_info['name'])
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        # embed.set_thumbnail(url=lastfm.get_artist_image(artist))
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    guild = discord.Client.get_guild(bot, 1025800326223237200)
    print("Music Loaded")
    await bot.add_cog(Music(bot), guild=guild)