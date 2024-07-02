import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Convert the string to an integer

# Initiate bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Store the history of interactions per channel
history = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if 'vesper' in content and 'hello' in content:
        await message.channel.send("Hello! Here to assist and maybe drop a joke or two. 😉")
        return

    # Process every message as a prompt
    response = await get_openai_response(message.channel.id, message.content)
    await message.channel.send(response)

    # React to emojis or external stickers
    for reaction in message.reactions:
        emoji = reaction.emoji
        await message.add_reaction(emoji)

    await bot.process_commands(message)

# Get response from OpenAI
async def get_openai_response(channel_id, prompt):
    global history
    context = history.get(channel_id, [{"role": "system", "content": "You are Vesper, a helpful assistant with a hint of fun and cuteness. Always be informative but don't shy away from a good joke when appropriate!"}])
    context.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=context
    )
    response_text = response.choices[0].message['content']
    context.append({"role": "assistant", "content": response_text})
    history[channel_id] = context[-20:]
    return response_text

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}, ready to assist with a touch of fun!")

bot.run(DISCORD_TOKEN)
