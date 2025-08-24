import openai
import discord
from discord.ext import commands
import yaml
import importlib.util

# Read config.yaml and get the openai_key and bot_token
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

#load the gpt bot from a different directory
bot_app_path = "../chatbot/app.py"
spec = importlib.util.spec_from_file_location("app.py", bot_app_path)
bot_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bot_app)

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


bot = commands.Bot(command_prefix="/!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")

@bot.command(name="test")
async def test(ctx):
    await ctx.send("test command!")

async def bot_talk(username, messages):


bot.run(bot_token)