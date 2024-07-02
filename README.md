# Vesper - A Cute & Humorous Discord Bot
Vesper is a delightful, fun-filled Discord bot powered by OpenAI's GPT-4 model.

## Requirements

1. Python 3.7+
2. Discord Account (for creating the bot)
3. OpenAI API key (for interfacing with GPT-4)

## Dependencies

The bot utilizes several Python packages:

- `discord.py` for interacting with the Discord API.
- `openai` for sending queries to the OpenAI API.
- `dotenv` for loading environment variables.

Install the dependencies with:

```bash
pip3 install discord.py openai python-dotenv 
```

## Setting up the Bot

1. **Discord Bot Setup**:
   - Visit the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on "New Application" and give your bot a name.
   - Navigate to the "Bot" tab and click "Add Bot".
   - Under the TOKEN section, click "Copy" to get your bot token. This will be added to the `.env` file later.

3. **Setting up the `.env` file**:
   Create a `.env` file in the root directory of the project and add the following:

   ```
   OPENAI_API_KEY=YourOpenAPIKeyHere
   DISCORD_TOKEN=YourDiscordBotTokenHere
   CHANNEL_ID=YourChannelIDHere
   ```

   Replace placeholders with appropriate values.

## Running the Bot

Navigate to the directory containing `bot.py` and run:

```bash
python3 Vesper.py
```

Vesper should now be online and ready to sprinkle some fun in your server!

## Contribution & Support

Feel free to fork this project, submit PRs, or report issues. For questions, reach out to Miles Oldenburger, the genius who tickled Vesper's digital brain into existence!
