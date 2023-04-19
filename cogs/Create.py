import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

# 100 possible events at once
eventIDs = list(range(1, 101))
# dictionary to store event embed data
embedDict = {}

class Create(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Create a new event
    @app_commands.command(name = "create", description = "Create a new event")
    @app_commands.describe(title = "Title of the created event. (Example: Birthday Party!)")
    @app_commands.describe(date = "Date of event in mm/dd/yy format. (Example: 3/27/23)")
    @app_commands.describe(time = "Time of event in hh:mm (AM/PM) format. (Example: 4:30 PM)")
    @app_commands.describe(count = "Number of participants (max 25)")
    async def create(self, interaction: discord.Interaction, title: str, date: str, time:str, count:int):
        author = interaction.user
        description = convert(interaction, date, time)
        RSVP_object = RSVP_Embed(author, title, description, count, [])
        id = addToDict(RSVP_object)
        if id is not None:
            embed = discord.Embed(title = title, description = description)
            embed.set_author(name = author.display_name, icon_url = author.avatar)
            embed.color = 0xFAF99D
            embed.set_thumbnail(url="https://www.pngitem.com/pimgs/m/578-5784443_somnomed-com-calendar-clipart-png-transparent-png.png")
            await interaction.response.send_message(embed = embed, view = RSVP(interaction, num_people = count, embed_id = id, embed_author = author))
        else:
            await interaction.response.send_message(content = '**Maximum number of events created!**')
# Object that stores all pertinent information regarding each event embed
class RSVP_Embed:
    def __init__(self, author: discord.user, title: str, date: str, count: int, participants):
        self.author = author
        self.title = title
        self.date = date
        self.count = count
        self.participants = participants

# Helper method that stores an RSVP_Embed object into the embedDict dictionary
# returns the id of embedDict in which it was stored or None if the maximum was reached
def addToDict(RSVP_object: RSVP_Embed):
    if len(eventIDs) < 1:
        print('Maximum events reached!')
        return None
    else:
        id = eventIDs.pop()
        embedDict[id] = RSVP_object
        print(f'Added Key {id}')
        return id

class RSVP(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, num_people: int, embed_id: int, embed_author: discord.user):
        super().__init__(timeout = None)
        for i in range(1, num_people + 1):
            self.add_item(AttendButton(spot_num = i, embed_id = embed_id))
        self.add_item(DeleteButton(interaction, embed_author = embed_author, embed_id = embed_id))

class DeleteButton(discord.ui.Button):
    def __init__(self, interaction: discord.Interaction, embed_author: discord.user, embed_id: int):
        super().__init__()
        self.embed_author = embed_author
        self.embed_id = embed_id
        self.interaction = interaction
        self.label = "Delete Event"
        self.style = discord.ButtonStyle.red
    async def callback(self, interaction: discord.Interaction):
        if interaction.user == self.embed_author:
            del embedDict[self.embed_id]
            print(f'Removed Key {self.embed_id}')
            await self.interaction.delete_original_response()
        else:
            await interaction.response.send_message(content = "Only the creator of the event can delete it!", ephemeral = True)

class AttendButton(discord.ui.Button):
    def __init__(self, spot_num: int, embed_id: int):
        super().__init__()
        self.embed_id = embed_id
        self.label = f'Spot {spot_num}'
        self.style = discord.ButtonStyle.green

    async def callback(self, interaction: discord.Interaction):
        # disable clicked button and change button text
        assert self.view is not None
        view: RSVP = self.view

        if interaction.user in embedDict[self.embed_id].participants:
            await interaction.response.send_message(content = "You have already claimed a spot!", ephemeral = True)
        else:
            self.disabled = True
            self.label = 'Spot taken!'
            # add new participant to embed data in dictionary
            old_embed = embedDict[self.embed_id]
            old_embed.participants.append(interaction.user)
            embedDict[self.embed_id] = old_embed
            # create new embed that will replace the old one to reflect participant change
            new_embed = discord.Embed(title = old_embed.title, description = old_embed.date)
            new_embed.set_author(name = old_embed.author.display_name, icon_url = old_embed.author.avatar)
            new_embed.color = 0xFAF99D
            new_embed.set_thumbnail(url="https://www.pngitem.com/pimgs/m/578-5784443_somnomed-com-calendar-clipart-png-transparent-png.png")
            for i in range(1, len(old_embed.participants) + 1):
                new_embed.add_field(name = f'Spot {i}', value = old_embed.participants[i-1].display_name)
            await interaction.response.edit_message(embed = new_embed, view=view)

def convert(interaction: discord.Interaction, date, time):
    # boilerplate timezone role objects
    PST = discord.utils.get(interaction.guild.roles, name = 'PST')
    MST = discord.utils.get(interaction.guild.roles, name = 'MST')
    CST = discord.utils.get(interaction.guild.roles, name = 'CST')
    EST = discord.utils.get(interaction.guild.roles, name = 'EST')
    # converts string to a datetime object
    date_dt_object = datetime.strptime(date, "%m/%d/%y")
    time_dt_object = datetime.strptime(time, "%I:%M %p").time()
    combined_dt_object = datetime.combine(date_dt_object, time_dt_object)
    # converts datetime object to formatted string
    datetime_to_string = combined_dt_object.strftime("On %m/%d/%y at %I:%M%p ")
    # adds appropriate timezone designation based on timezone role
    author = interaction.user
    if (PST in author.roles):
        datetime_to_string += "PST"
    elif (MST in author.roles):
        datetime_to_string += "MST"
    elif (CST in author.roles):
        datetime_to_string += "CST"
    elif (EST in author.roles):
        datetime_to_string += "EST"
    return datetime_to_string
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Create(bot))
