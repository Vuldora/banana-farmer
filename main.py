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
heroes = ['Quincy','Cyber Quincy','Gwen','Science Gwen','Obyn','Ocean Obyn','Striker Jones','Biker Bones','Churchill','Sentai','Benjamin','DJ Benjammin','Ezili','Smudge Catt Ezili','Pat Fusty','Snowpat','Jericho','Highwayman','Star Captain','Adora']

@tree.command(
    name="map",
    description="Randomly select a map",
)
@app_commands.describe(hom_only="Return only Hall of Masters maps")
async def map_command(interaction: discord.Interaction, hom_only: Literal["Yes","No"]):
    if interaction.data["options"][0]["value"] == "Yes":
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
        self.subpage_index = 0
        self.max_pages = 0

    @discord.ui.button(emoji="◀️",style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_button = PageButtons()
        page_button.page_index = self.page_index
        page_button.subpage_index = self.subpage_index
        page_button.max_pages = self.max_pages
        if page_button.subpage_index == 1:
            page_button.subpage_index = 0
        else:
            page_button.subpage_index = 1
            page_button.page_index -= 1
        if page_button.page_index == 1 and page_button.subpage_index == 0:
            page_button.previous_button.disabled = True
        embed=lb_embed(15,page_button.page_index,page_button.subpage_index)
        page_button.pages_button.label = str((page_button.page_index-1)*2+page_button.subpage_index+1) + "/" + str(page_button.max_pages)
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(embed=embed,view=page_button)
    @discord.ui.button(label="1/?",style=discord.ButtonStyle.secondary, disabled=True)
    async def pages_button(self):
        pass
    @discord.ui.button(emoji="▶️",style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_button = PageButtons()
        page_button.page_index = self.page_index
        page_button.subpage_index = self.subpage_index
        page_button.max_pages = self.max_pages
        if page_button.subpage_index == 0:
            page_button.subpage_index = 1
        else:
            page_button.subpage_index = 0
            page_button.page_index += 1
        page_button.pages_button.label = str((page_button.page_index-1)*2+page_button.subpage_index+1) + "/" + str(page_button.max_pages)
        embed=lb_embed(15,page_button.page_index,page_button.subpage_index)
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(embed=embed,view=page_button)

def lb_embed(season,page,subpage):
    lb_url= "https://data.ninjakiwi.com/battles2/homs/season_" + str(season) + "/leaderboard?page=" + str(page)
    response = requests.get(lb_url)
    leaderboard = response.json()
    embed = discord.Embed(
            title="Season " + str(season) + " leaderboard",
            )
    if leaderboard["success"] == False:
        discord.Embed.add_field(embed,name="No more rankings left",value="last page reached")
    else:
        if subpage == 0:
            lb = leaderboard["body"][0:25]
        else:
            lb = leaderboard["body"][25:50]
        for index, entry in enumerate(lb):
            field_name="#" + str(index+1+(page-1)*50+subpage*25) + ". " + entry["displayName"]
            discord.Embed.add_field(
                embed,
                name=field_name,
                value=str(entry["score"])
                )
    return embed


@tree.command(
    name="leaderboard",
    description="Shows current season's leaderboard"
)
async def leaderboard_command(interaction: discord.Interaction):
    homs = requests.get("https://data.ninjakiwi.com/battles2/homs").json()
    rankings = lb_embed(15,1,0)
    page_button=PageButtons()
    page_button.page_index = 1
    page_button.previous_button.disabled = True
    page_button.max_pages = int((homs["body"][0]["totalScores"])/50+1)*2 
    page_button.pages_button.label = "1" + "/" + str(int((homs["body"][0]["totalScores"])/50+1)*2)
    await interaction.response.send_message(embed=rankings, view=page_button)

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Ryan Mehalic"))
    print("Initilization Complete")

client.run(DISCORD_TOKEN)
