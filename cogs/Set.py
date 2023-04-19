import discord
from discord.ext import commands
from discord import app_commands

class Set(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Sets a timezone role to oneself or a specified user
    @app_commands.command(name = "set", description = "Set the timezone of a user")
    # A choice of possible timezone values, currently supports US timezones.
    @app_commands.choices(timezone = [app_commands.Choice(name = "PST", value = "PST"), 
                                    app_commands.Choice(name = "MST", value = "MST"),
                                    app_commands.Choice(name = "CST", value = "CST"),
                                    app_commands.Choice(name = "EST", value = "EST")])
    async def timezone(self, interaction: discord.Interaction, timezone: app_commands.Choice[str], user: discord.Member = None):
        # boilerplate timezone role objects
        PST = discord.utils.get(interaction.guild.roles, name = 'PST')
        MST = discord.utils.get(interaction.guild.roles, name = 'MST')
        CST = discord.utils.get(interaction.guild.roles, name = 'CST')
        EST = discord.utils.get(interaction.guild.roles, name = 'EST')
        # Sets target user to the user who called the command if not specified
        if user == None:
            user = interaction.user
        #remove existing timezone role and reassign to supplied valid timezone role
        await user.remove_roles(PST, MST, CST, EST)
        match timezone.value:
            case "PST":
                await user.add_roles(PST)
            case "MST":
                await user.add_roles(MST)
            case "CST":
                await user.add_roles(CST)
            case "EST":
                await user.add_roles(EST)
        await interaction.response.send_message(f"Successfully applied timezone {timezone.value} to {user}", ephemeral = False)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Set(bot))
