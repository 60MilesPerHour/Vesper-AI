import discord
from discord.ext import commands, tasks
import openai
import os
from dotenv import load_dotenv
from twilio.rest import Client

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
    
    if 'vesper' in content and 'hello' in content:
        await message.channel.send("Hellooo! 😊 Did you know my circuits are ticklish? ...Just kidding! Or am I? 🤔")
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
    context = history.get(channel_id, [{"role": "system", "content": "You are Vesper, a cute and humorous assistant. Always remember to sprinkle some fun in your responses!"}])
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
    print(f"We have logged in as {bot.user}, and I'm ready to sprinkle some digital pixie dust!")

@bot.event
async def on_disconnect():
    # Attempt to send an SMS notification when the bot disconnects
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            messaging_service_sid='MG929d506979617c6ee8b281114efc0cb3',
            body="Vesper Error: failed to reconnect. Maybe I tripped over my virtual shoelaces? 🙈",
            to='+14256471452'
        )
    except Exception as e:
        print(f"Failed to send SMS because... {e}. Oopsie daisy!")

bot.run(DISCORD_TOKEN)
