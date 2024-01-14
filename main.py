import discord, random, requests, json, os
from discord import app_commands, ui
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN= os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
api_url = "https://data.ninjakiwi.com/battles2/homs"
page_index = 1

towers = ['Dart','Tack','Boomerang','Bomb','Ice','Glue','Sniper','Sub','Boat','Ace','Heli','Mortar','Dartling','Wizard','Super','Ninja','Alchemist','Druid','Village','Farm','Spike Factory','Engineer']
maps = ['Bloontonium Mines','Docks','In the Wall','Mayan','Thin Ice','Banana Depot','Basalt Columns','Bloon Bot Factory','Building Site','Castle Ruins','Cobra Command','Dino Graveyard','Garden','Glade','Inflection','Koru','Oasis','Off-tide','Pirate Cove','Ports','Precious Space','Sands of Time','Star','Sun Palace']
heroes = ['Quincy','Cyber Quincy','Gwen','Science Gwen','Obyn','Ocean Obyn','Striker Jones','Biker Bones','Churchill','Sentai','Benjamin','DJ Benjammin','Ezili','Smudge Catt Ezili','Pat Fusty','Patclown','Jericho','Highwayman','Star Captain','Adora']

@tree.command(
    name="map",
    description="Randomly select a map",
)
@app_commands.describe(hom_only="Return only Hall of Masters maps")
async def map_command(interaction: discord.Interaction, hom_only: Literal["Yes","No"]):
    if map_command.get_parameter("hom_only") == "Yes":
        await interaction.response.send_message(maps[random.randint(4,(len(maps) - 1))]) 
    else:
        await interaction.response.send_message(maps[random.randint(0,(len(maps) - 1))])

@tree.command(
    name="quad",
    description="Randomly generate a tower loadout"
)
async def quad_command(interaction):
    quad = random.sample(towers, k=3)
    await interaction.response.send_message(quad[0] + ", " + quad[1] + ", " + quad[2] + ", and " + heroes[random.randint(0,(len(heroes) - 1))])

class PageButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.page_index = 0

    @discord.ui.button(emoji="◀️",style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_button = PageButtons()
        page_button.page_index = self.page_index - 1
        if page_button.page_index == 1:
            page_button.previous_button.disabled = True
        await interaction.response.send_message(lb_message(15,page_button.page_index), view=page_button)
    @discord.ui.button(emoji="▶️",style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_button = PageButtons()
        page_button.page_index += self.page_index + 1
        await interaction.response.send_message(lb_message(15,page_button.page_index), view=page_button)

def lb_message(season,page):
    lb_url= "https://data.ninjakiwi.com/battles2/homs/season_" + str(season) + "/leaderboard?page=" + str(page)
    response = requests.get(lb_url)
    leaderboard = response.json()
    if leaderboard["success"] == False:
        return "No more rankings available"
    rankings = "```Rank Player         Score \n"
    index_suffix = ""
    space1 = ""
    space2 = ""
    for index, entry in enumerate(leaderboard["body"]):
        if index == 10 or index == 11:
            index_suffix = "th"
        elif index % 10 == 0:
            index_suffix = "st"
        elif index % 10 == 1:
            index_suffix = "nd"
        else:
            index_suffix = "th"
        if index < 9:
            space1 = "  "
        else:
            space1 = " "
        for x in range(15-len(entry["displayName"])):
            space2 += " "
        rankings += str(index+1+(page-1)*50) + index_suffix + space1 + entry["displayName"] + space2 + str(entry["score"]) + "\n"
        space2 = ""
    rankings += "```"
    return rankings

@tree.command(
    name="leaderboard",
    description="Shows current season's leaderboard"
)
async def leaderboard_command(interaction: discord.Interaction):
    rankings = lb_message(15,1)
    page_button=PageButtons()
    page_button.page_index = 1
    page_button.previous_button.disabled = True
    await interaction.response.send_message(rankings, view=page_button)

@tree.command(
        name="embed",
        description="test command for embeds"
        )
async def embed_command(interaction: discord.Interaction):
    embed = discord.Embed(
            title="test",
            description="this is a description"
            )
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Ryan Mehalic"))
    print("Initilization Complete")

client.run(DISCORD_TOKEN)
