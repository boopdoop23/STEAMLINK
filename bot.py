import discord
from discord.ext import commands
from discord import app_commands, Interaction, ButtonStyle
from discord.ui import View, Button, Modal, TextInput
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CONFIGURABLE (Load from environment variables)
VIP_ROLE_ID = int(os.getenv("VIP_ROLE_ID"))  # VIP Role ID from .env
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))  # Admin Role ID from .env
LINKED_JSON_PATH = "linked.json"

intents = discord.Intents.default()
intents.message_content = False
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Ensure JSON exists
if not os.path.exists(LINKED_JSON_PATH):
    with open(LINKED_JSON_PATH, "w") as f:
        json.dump({}, f)

def load_links():
    with open(LINKED_JSON_PATH, "r") as f:
        return json.load(f)

def save_links(data):
    with open(LINKED_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)

class SteamLinkModal(Modal, title="Link Your Steam Account"):
    steam_id = TextInput(label="Steam 64 ID", placeholder="7656119XXXXXXXXXX", required=True)

    async def on_submit(self, interaction: Interaction):
        if not self.steam_id.value.isdigit() or not self.steam_id.value.startswith("7656"):
            await interaction.response.send_message("❌ Invalid Steam ID format.", ephemeral=True)
            return

        links = load_links()
        links[str(interaction.user.id)] = self.steam_id.value
        save_links(links)

        await interaction.response.send_message(f"✅ Linked Steam ID `{self.steam_id.value}` to your Discord.", ephemeral=True)

class SteamLinkView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="🔗 Link Steam", style=ButtonStyle.primary, custom_id="link_steam"))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_interaction(interaction: Interaction):
    if interaction.type == discord.InteractionType.component and interaction.data["custom_id"] == "link_steam":
        member = interaction.user
        if VIP_ROLE_ID not in [role.id for role in member.roles]:
            await interaction.response.send_message("❌ You must have the VIP role to link your Steam account.", ephemeral=True)
            return
        await interaction.response.send_modal(SteamLinkModal())

@bot.tree.command(name="exportguids", description="Export all linked Steam GUIDs (Admin only)")
async def export_guids(interaction: Interaction):
    member = interaction.user
    if ADMIN_ROLE_ID not in [role.id for role in member.roles]:
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    links = load_links()
    steam_ids = list(links.values())
    output = f"GUID={' ;'.join(steam_ids)}"
    await interaction.response.send_message(f"```{output}```", ephemeral=True)

@bot.tree.command(name="sendembed", description="Send the Steam linking embed to the channel (Admin only)")
async def send_embed(interaction: Interaction):
    member = interaction.user
    if ADMIN_ROLE_ID not in [role.id for role in member.roles]:
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    embed = discord.Embed(title="Link Your Steam", description="Click the button below to link your Steam account to your Discord.", color=discord.Color.purple())
    await interaction.response.send_message(embed=embed, view=SteamLinkView())

# Replace this with your bot token from .env
bot.run(os.getenv("DISCORD_TOKEN"))
