import discord
from discord import app_commands
from revChatGPT.revChatGPT import Chatbot
import json

with open('config.json', 'r') as f:
    config = json.load(f)

chatbot = Chatbot(config, conversation_id=None)
chatbot.refresh_session()
guild_id = 438564961745371136

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync() #guild = discord.Object(id = guild_id) -> testing
            self.synced = True
        print(f'We have logged in as { self.user }')

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(name = "test", description= "testing", guild = discord.Object(id = guild_id))
async def self(interaction: discord.Integration, name: str):
    await interaction.response.send_message(f"Hello {name}! I was made with Discord.py!")

@tree.command(name = "say", description= "Have Donald Trump say something!")
async def defer(interaction: discord.Interaction, input: str):
    await interaction.response.defer()
    try:
        textRequest = f"Say {input} in the style of Donald Trump"
        response = chatbot.get_chat_response(textRequest, output="text")['message']
    except:
        await interaction.followup.send(f"Failed!")
        return
    chatbot.reset_chat()
    await interaction.followup.send(f"{response}")

@tree.command(name = "fanfiction", description= "Write a fanfiction about two characters!")
async def defer(interaction: discord.Interaction, char1: str, char2: str):
    await interaction.response.defer()
    textRequest = f"Write a fanfiction about {char1} and {char2}"
    try:
        response = chatbot.get_chat_response(textRequest, output="text")['message']
        chatbot.reset_chat()
    except:
        await interaction.followup.send(f"Failed!")
        return
    if(len(response) > 2000):
        broken = [response[i:i+1950] for i in range(0, len(response), 1950)]
        for substr in broken:
            await interaction.followup.send(f"{substr}")
    else:
        await interaction.followup.send(f"{response}")

@tree.command(name = "custom", description= "Customize your ChatGPT Query")
async def defer(interaction: discord.Interaction, input:str):
    await interaction.response.defer()
    textRequest = f"{input}"
    try:
        print(textRequest)
        response = chatbot.get_chat_response(textRequest, output="text")['message']
        chatbot.reset_chat()
        print(response)
    except:
        await interaction.followup.send(f"Failed!")
        return

    if(len(response) > 2000):
        broken = [response[i:i+1950] for i in range(0, len(response), 1950)]
        for substr in broken:
            await interaction.followup.send(f"{substr}")
    else:
        await interaction.followup.send(f"{response}")

@tree.command(name = "refresh", description= "Refreshes CGPT Headers")
async def defer(interaction: discord.Interaction):
    chatbot.refresh_session()
    chatbot.refresh_headers()
    await interaction.response.send_message(f"Reset Session!")

client.run(str(config['token']))