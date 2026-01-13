import discord
from discord.ext import commands
import json
import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

DB_FILE = "database.json"

# --- LOGIKA DATA ---
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

users_data = load_data()

# --- PERINTAH BARU ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Daftar Perintah Bot", color=discord.Color.blue())
    embed.add_field(name="!level", value="Cek level dan XP kamu sekarang.", inline=False)
    embed.add_field(name="!ping", value="Cek kecepatan respon bot.", inline=False)
    embed.add_field(name="!info", value="Info singkat tentang bot keren ini.", inline=False)
    embed.set_footer(text="Chat terus buat naik level!")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command()
async def info(ctx):
    await ctx.send("Bot ini dibuat dengan cinta dan logika GitHub Runner. Leveling jalan terus!")

# --- EVENT LEVELING & GAMBAR ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    
    user_id = str(message.author.id)
    if user_id not in users_data:
        users_data[user_id] = {"xp": 0, "level": 0}

    users_data[user_id]["xp"] += 15 # Tambah XP tiap chat
    
    lvl = users_data[user_id]["level"]
    if users_data[user_id]["xp"] >= (lvl + 1) * 100:
        users_data[user_id]["level"] += 1
        save_data(users_data)
        await message.channel.send(f"🔥 GOKIL! {message.author.mention} naik ke Level {lvl + 1}!")

    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))
  
