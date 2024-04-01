import discord
import requests
import json
from discord.ext import commands, tasks

# Initialize Discord bot
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# API URL
API_URL = "http://<your_machine_ip>:5000/cyberthreats"

# Channel ID where updates will be posted
CHANNEL_ID = 1224245050981089430  # Replace with your Discord channel ID

# Previous threats for comparison
previous_threats = []

# Function to fetch all cyber threats from API
def fetch_all_threats():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        threats = response.json()
        return threats
    else:
        print(f"Failed to fetch all cyber threats. Status code: {response.status_code}")
        return None

# Background task to check for new cyber threats
@tasks.loop(minutes=5)
async def check_threats():
    global previous_threats
    
    threats = fetch_all_threats()
    
    if threats:
        new_threats = [threat for threat in threats if threat not in previous_threats]
        
        if new_threats:
            for threat in new_threats:
                embed = discord.Embed(title=f"New Cyber Threat Detected: {threat['type']}", color=discord.Color.red())
                embed.add_field(name="Severity", value=threat['severity'], inline=False)
                embed.add_field(name="Description", value=threat['description'], inline=False)
                embed.set_footer(text="Cyber Threat Alert")
                
                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(embed=embed)
            
            previous_threats = threats

# Event to run when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    check_threats.start()
    print("Threat monitoring started...")

# Run the bot
bot.run("MTIyNDI0NTQzOTU1Mzg2NzgxNg.G2z3IB.WK0gFdxaRlk9QLUZkmleiaaMnj9BK8RFSU3I4Y")
