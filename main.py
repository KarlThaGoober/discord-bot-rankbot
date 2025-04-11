import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load the .env file containing the bot token
load_dotenv()

# Retrieve the token from the environment
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Define your guild ID here once, so it's easier to manage
MY_GUILD_ID = 1335619362710622289  # Replace with your actual guild/server ID
GUILD = discord.Object(id=MY_GUILD_ID)

# Helper function to split the text into chunks
def split_text(text, chunk_size=1024):
    """Helper function to split text into chunks of specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Create the bot instance
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    print('-----------------------------------------------------')
    print(f'Logged in as ({client.user})')
    print('-----------------------------------------------------')
    print('Bot | Online')
    print('-----------------------------------------------------')

    try:
        synced = await client.tree.sync(guild=GUILD)
        print(f'Synced {len(synced)} commands to guild {MY_GUILD_ID}')
        print('-----------------------------------------------------')

    except Exception as e:
        print(f'Error syncing commands: {e}')
        print('-----------------------------------------------------')

@client.tree.command(name='show_ranks', description='Shows the list of the ranks for the server named "The Mighty Seventh"', guild=GUILD)
async def showranks(interaction: discord.Interaction):
    try:
        with open('ranks.txt', 'r') as f:
            ranks_data = f.read()

        if not ranks_data.strip():
            await interaction.response.send_message("Ranks file is empty.")
            return

        sections = {
            "Recruit's": "",
            "Main": "",
            "Admins": "",
            "Info": "",
        }

        current_section = None
        for line in ranks_data.splitlines():
            if '--' in line:
                section_name = line.strip('-').strip()
                if section_name in sections:
                    current_section = section_name
            elif current_section:
                sections[current_section] += line + "\n"

        embed = discord.Embed(
            title=":military_medal: Ranks",
            color=discord.Color.from_rgb(45, 60, 141),
            description="**Here are the latest server ranks:**"
        )

        # Set author (your YouTube profile picture as icon)
        embed.set_author(
            name="Karl(KUTSUMETS)",
            icon_url="https://yt3.googleusercontent.com/NPjAhH3_618QGAT-v02By02fctCg5noZ-MURCpFfnR7py8rEjezGMPSEFayYwJBMACsJ8top1g=s88-c-k-c0x00ffffff-no-rj"
        )

        # Add sections
        for section_name in ["Recruit's", "Main", "Admins", "Info"]:
            section_content = sections[section_name]
            if section_content.strip():
                chunks = split_text(section_content, 1024)
                for chunk in chunks:
                    embed.add_field(name=section_name, value=f"```{chunk}```", inline=False)

        await interaction.response.send_message(embed=embed)

    except FileNotFoundError:
        await interaction.response.send_message("Ranks file not found.")
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}")

# Run the bot
client.run(TOKEN)