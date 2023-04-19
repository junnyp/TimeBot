import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

class Current(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Displays the current date and time to the user depending on their timezone role
    @app_commands.command(name = "current", description = "Display your assigned timezone's current time")
    async def current(self, interaction: discord.Interaction):
        # boilerplate timezone role objects
        PST = discord.utils.get(interaction.guild.roles, name = 'PST')
        MST = discord.utils.get(interaction.guild.roles, name = 'MST')
        CST = discord.utils.get(interaction.guild.roles, name = 'CST')
        EST = discord.utils.get(interaction.guild.roles, name = 'EST')
        # Initialize the embed with color and thumbnail
        embed = discord.Embed(color=0x00FFF0)
        embed.set_thumbnail(url="https://www.pngitem.com/pimgs/m/578-5784443_somnomed-com-calendar-clipart-png-transparent-png.png")
        # converts time to respective timezone role
        msgTime = datetime.utcnow()
        author = interaction.user
        if (PST in author.roles):
            userTime = msgTime + timedelta(hours = -7)
            time = userTime.strftime("%I:%M %p") + " (PST)"
        elif (MST in author.roles):
            userTime = msgTime + timedelta(hours = -6)
            time = userTime.strftime("%I:%M %p") + " (MST)"
        elif (CST in author.roles):
            userTime = msgTime + timedelta(hours = -5)
            time = userTime.strftime("%I:%M %p") + " (CST)"
        elif (EST in author.roles):
            userTime = msgTime + timedelta(hours = -4)
            time = userTime.strftime("%I:%M %p") + " (EST)"
        else:
            userTime = msgTime
            time = msgTime.strftime("%I:%M %p") + " (UTC)"
        # displays formatted content back to user in an embed
        date = userTime.strftime("%A, %B %e, %Y")
        embed.add_field(name = "Date", value = date, inline = False)
        embed.add_field(name = "Time", value = time, inline = False)
        await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Current(bot))