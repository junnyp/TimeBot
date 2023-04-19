import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import platform
from datetime import datetime
# Unique token for bot, should be kept hidden
TOKEN = 'OTg4NjE3NTczMjI4NzU3MDg1.GE-0ze._7Xg6p9wa5bEJPDIVKHCkhym8YfOyOMqKBZxE8'

# 100 possible events at once
eventIDs = list(range(1, 101))
# dictionary to store event embed data
embedDict = {}

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('!'), description = "Event Bot", intents = intents)
        self.cogslist = ["cogs.Shutdown", "cogs.Current", "cogs.Set", "cogs.Create"]
    
    # Load all cogs (commands)
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
        
    # Prints start-up information to console.
    async def on_ready(self):
        # Sync slash commands to tree
        synced = await bot.tree.sync()
        # Stylistic elements for console messages
        pre = (Back.BLACK + Fore.GREEN + datetime.now().strftime("%I:%M:%S%p") + Back.RESET + Fore.WHITE + Style.BRIGHT)
        post = (Style.RESET_ALL)
        # Information on startup that is printed to console
        print(f'{pre} Logged in as {bot.user} (ID: {bot.user.id}) {post}')
        print(f'{pre} Discord Version: {discord.__version__} {post}')
        print(f'{pre} Python Version: {platform.python_version()} {post}')
        print(f'{pre} Synced {str(len(synced))} command(s) {post}')
        print('------------------------------------------------------------')
        
bot = Bot()
bot.run(TOKEN)




