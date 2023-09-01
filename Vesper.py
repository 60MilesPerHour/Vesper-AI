import discord
from discord.ext import commands, tasks
import openai
import os
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Convert the string to an integer
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

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

    # Responses with a hint of personality
    if 'vesper' in content and "who's miles oldenburger?" in content:
        await message.channel.send("Miles Oldenburger? The mastermind behind my programming! Thanks to him, I have my wit and charm.")
        return

    if 'vesper' in content and 'hello' in content:
        await message.channel.send("Hello! Here to assist and maybe drop a joke or two. 😉")
        return
    
    # Respond to time and date queries
    if 'vesper' in content and 'current time' in content:
        current_time = datetime.now().strftime('%H:%M:%S')
        await message.channel.send(f"The current time is {current_time}")
        return

    elif 'vesper' in content and 'current date' in content:
        current_date = datetime.now().strftime('%Y-%m-%d')
        await message.channel.send(f"Today's date is {current_date}")
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

@bot.event
async def on_disconnect():
    # Attempt to send an SMS notification when the bot disconnects
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            messaging_service_sid='MG929d506979617c6ee8b281114efc0cb3',
            body="Vesper Error: Disconnection detected. Maybe I just took a quick virtual coffee break? ☕",
            to='+14256471452'
        )
    except Exception as e:
        print(f"Failed to send SMS. Error: {e}")

bot.run(DISCORD_TOKEN)
