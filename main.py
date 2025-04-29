import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import os

# Configuração do Flask para manter o bot online
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Configuração do bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs dos canais a limpar
canal_ids = [
    1366435302343835719,  # ID do Canal 1
    1366260085487177759   # ID do Canal 2
]

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    limpar_canal.start()

@tasks.loop(seconds=30)
async def limpar_canal():
    try:
        for canal_id in canal_ids:
            canal = bot.get_channel(canal_id)
            if canal:
                await canal.purge(limit=100)
                print(f"Canal {canal.name} limpo!")
            else:
                print(f"Canal com ID {canal_id} não encontrado.")
    except Exception as e:
        print(f"Erro ao limpar: {e}")

keep_alive()

bot.run(os.getenv(""))