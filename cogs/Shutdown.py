import discord
from discord.ext import commands
from discord import app_commands

class Shutdown(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Manually shut down the bot
    @app_commands.command(name = "shutdown", description = "Shutdown the bot")
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.send_message(content = "Moment shutting down.")
        await self.bot.close()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Shutdown(bot))
