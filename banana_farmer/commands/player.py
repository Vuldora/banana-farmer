import discord, requests, json, math
from discord import app_commands, ui

async def player_command(interaction, player: str):
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

player_command = discord.app_commands.Command(
    name="player",
    description="Shows a player's stats - must be in hall of masters",
    callback=player_command,
)

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
