import os
import threading
import requests
from io import BytesIO
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def card(ctx, uid: str = None):
    if not uid:
        await ctx.send("Usage: !card UID")
        return

    api_url = f"http://www.farhanexe.xyz/apis/profile_card?uid={uid}"

    try:
        r = requests.get(api_url, timeout=10)

        if r.status_code != 200:
            await ctx.send("Image fetch failed")
            return

        image = BytesIO(r.content)
        file = discord.File(image, filename="card.png")

        embed = discord.Embed(
            title="Profile Card",
            description=f"UID: {uid}",
            color=0x2f3136
        )
        embed.set_image(url="attachment://card.png")

        await ctx.send(embed=embed, file=file)

    except Exception as e:
        await ctx.send("Something went wrong")
        print(e)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
