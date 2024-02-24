import discord, random, requests, json, os, math
from discord import app_commands, ui
from typing import Literal
from dotenv import load_dotenv
import mapcmd

load_dotenv()
DISCORD_TOKEN= os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="quad",
    description="Randomly generate a tower loadout"
)
async def quad_command(interaction):
    towers = ['Dart','Tack','Boomerang','Bomb','Ice','Glue','Sniper','Sub','Boat','Ace','Heli','Mortar','Dartling','Wizard','Super','Ninja','Alchemist','Druid','Village','Farm','Spike Factory','Engineer']
    heroes = ['Quincy','Cyber Quincy','Gwen','Science Gwen','Obyn','Ocean Obyn','Striker Jones','Biker Bones','Churchill','Sentai','Benjamin','DJ Benjammin','Ezili','Smudge Catt Ezili','Pat Fusty','Snowpat','Jericho','Highwayman','Star Captain','Adora']
    quad = random.sample(towers, k=3)
    await interaction.response.send_message(quad[0] + ", " + quad[1] + ", " + quad[2] + ", and " + heroes[random.randint(0,(len(heroes) - 1))])

class PageButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.page_index = 0
        self.subpage_index = 0
        self.max_pages = 0

    @discord.ui.button(emoji="⏪",style=discord.ButtonStyle.green)
    async def first_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_button = PageButtons()
        page_button.page_index = 1
        page_button.subpage_index = 0
        page_button.max_pages = self.max_pages
        page_button.previous_button.disabled = True
        page_button.first_button.disabled = True
        embed=lb_embed(15,page_button.page_index,page_button.subpage_index)
        page_button.pages_button.label = str((page_button.page_index-1)*2+page_button.subpage_index+1) + "/" + str(page_button.max_pages)
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(embed=embed,view=page_button)
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
            page_button.first_button.disabled = True
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
        if (page_button.page_index-1)*2+page_button.subpage_index+1 == page_button.max_pages:
            page_button.next_button.disabled = True
        embed=lb_embed(15,page_button.page_index,page_button.subpage_index)
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(embed=embed,view=page_button)
    @discord.ui.button(emoji="⏩",style=discord.ButtonStyle.green)
    async def last_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_button = PageButtons()
        page_button.page_index = int((self.max_pages-1)/2)+1
        if self.max_pages%2 == 0:
            page_button.subpage_index = 1
        else:
            page_button.subpage_index = 0
        page_button.max_pages = self.max_pages
        page_button.next_button.disabled = True
        page_button.last_button.disabled = True
        embed=lb_embed(15,page_button.page_index,page_button.subpage_index)
        page_button.pages_button.label = str((page_button.page_index-1)*2+page_button.subpage_index+1) + "/" + str(page_button.max_pages)
        await interaction.response.defer()
        msg = await interaction.original_response()
        await msg.edit(embed=embed,view=page_button)

def lb_embed(season,page,subpage):
    lb_url= "https://data.ninjakiwi.com/battles2/homs/season_" + str(season) + "/leaderboard?page=" + str(page)
    response = requests.get(lb_url)
    leaderboard = response.json()
    embed = discord.Embed(
            title="Season " + str(season) + " leaderboard"
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
    page_button.first_button.disabled = True
    page_button.max_pages = int(math.ceil((homs["body"][0]["totalScores"])/25)) 
    page_button.pages_button.label = "1" + "/" + str(page_button.max_pages)
    await interaction.response.send_message(embed=rankings, view=page_button)

def player_embed(oakurl):
    player = requests.get(oakurl).json()
    embed = discord.Embed(
            title="Player Stats - " + player["body"]["displayName"]
            )
    image_url = player["body"]["equippedAvatarURL"]
    discord.Embed.set_thumbnail(embed, url=image_url)
    ranked = player["body"]["rankedStats"]
    ranked_stats = "Wins: " + str(ranked["wins"]) + " \n"
    ranked_stats += "Losses: " + str(ranked["losses"]) + " \n"
    ranked_stats += "Draws: " + str(ranked["draws"]) + " \n"
    ranked_stats += "Winrate: " + "{0:.2f}".format(ranked["wins"]/(ranked["losses"]+ranked["wins"])*100) + "%" + " \n"
    ranked_stats += "Current Winstreak: " + str(ranked["win_streak"]) + " \n"
    ranked_stats += "Highest Winstreak: " + str(ranked["highest_win_streak"])
    discord.Embed.add_field(
        embed,
        name="Ranked Stats",
        value=ranked_stats
        )
    return embed

def player_selection(matches):
    embed = discord.Embed(
        title="Found multiple results",
        description="please select which player's stats you want to view")
    return embed

class PlayerSelect(discord.ui.View):
    def __init__(self, players):
        self.players = players  
        discord.ui.Select(options=players["displayName"])

    async def options(self, interaction: discord.Interaction, select: discord.ui.Select):
        pass
        
@tree.command(
    name="player",
    description="Shows a player's stats - must be in hall of masters"
)
async def player_command(interaction: discord.Interaction, player: str):
    player = interaction.data["options"][0]["value"]
    homs = requests.get("https://data.ninjakiwi.com/battles2/homs").json()
    last_page = int(math.ceil((homs["body"][0]["totalScores"])/50))
    found = 0
    page = 1
    matches = []
    while (page <= last_page):
        lb_url= "https://data.ninjakiwi.com/battles2/homs/season_15/leaderboard?page=" + str(page)
        response = requests.get(lb_url)
        leaderboard = response.json()
        for entry in leaderboard["body"]:
            if entry["displayName"].lower() == player.lower():
                matches.append(entry)
                found += 1
        page += 1
    if found == 0:
        await interaction.response.send_message("I couldn't find this player")
    elif found == 1:
        player_stats = player_embed(matches[0]["profile"])
        await interaction.response.send_message(embed=player_stats)
    else:
        embed = discord.Embed(
        title="Found multiple results",
        description="please select which player's stats you want to view"
        )
        select = discord.ui.Select()
        for match in matches:
            select.add_option(label=match["displayName"],value=match["profile"])
        async def selection_callback(interaction):
            player_stats = player_embed(select.values[0])
            await interaction.response.send_message(embed=player_stats)
        select.callback = selection_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed,view=view)

@client.event
async def on_ready():
    tree.add_command(mapcmd.map_command)
    await tree.sync() 
    cute_people = ['Emilplane','Ryan Mehalic','Cologne', 'Paytrolah']
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=cute_people[random.randint(0,len(cute_people)-1)]))
    print("Initilization Complete")

client.run(DISCORD_TOKEN)
