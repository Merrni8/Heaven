import discord
from discord.ext import commands
import config
import database
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    await database.init_db()
    
    try:
        synced = await bot.tree.sync()
        print(f"Zsynchronizowano {len(synced)} komend slash")
    except Exception as e:
        print(f"Błąd synchronizacji: {e}")

async def load_cogs():
    cogs = ["welcome", "levels", "economy", "moderation", "giveaways"]
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Załadowano: {cog}")
        except Exception as e:
            print(f"Nie udało się załadować {cog}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
