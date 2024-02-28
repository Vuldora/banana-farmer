import discord, requests, json, math
from discord import app_commands, ui

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

leaderboard_command = discord.app_commands.Command(
    name="leaderboard",
    description="Shows current season's leaderboard",
    callback=leaderboard_command,
)

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
