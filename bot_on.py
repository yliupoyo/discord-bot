import openai
import discord
from discord.ext import commands
import yaml
import importlib.util

# Read config.yaml and get the openai_key and bot_token
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

# Set OpenAI API key
openai.api_key = config_data.get("openai_api_key")
bot_token = config_data.get("discord_bot_token")

# Permissions to send events and access data
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

# Inheritance of MemberConverter. this allows users to mention someone in the sever by displayname, not UserID or User tags
class DisplayNameMemberConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        for member in ctx.guild.members:
            if member.display_name.lower() == argument.lower():
                return member
        raise commands.MemberNotFound(argument)

#async def generate_cardReading(username, question, cards):
    #prompt = f"based on the question from {username}, create an appropriate and gentle tarrot card reading"\
    #         f"according to {cards} and focus on topics:\n{question}\n"
    #response = openai.responses.create(
    #     model="gpt-4o-2024-08-06",
    #        input=prompt,
    #        temperature=0.5,
    #)
    #read = response.output_text.strip()
    #return read

bot = commands.Bot(command_prefix="/!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")

@bot.command(name="test")
async def test(ctx):
    await ctx.send("test command!")

@bot.command(name='tarrot')
async def tarrot(ctx, *, username: str, message):
    try:
        user = await DisplayNameMemberConverter().convert(ctx, username)
    except commands.MemberNotFound:
        await ctx.send(f"user {username} not found.")
        return
    #question = []
    #question.append(message)
    #card = 1
    #read = await generate_cardReading(username,question,card)
    cardurl = "https://randomtarotcard.com/TheHermit.jpg"
    await ctx.send(cardurl)


# connect the bot to talk


bot.run(bot_token)