import discord
from discord.ext import commands
from discord import app_commands
import database
from datetime import datetime, timedelta
import asyncio
import random

class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="giveaway", description="Stwórz giveaway")
    @app_commands.describe(
        czas="Czas trwania (np. 1h, 30m, 1d)",
        nagroda="Co jest do wygrania",
        zwyciezcy="Ilu zwycięzców (domyślnie 1)"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def giveaway(self, interaction: discord.Interaction, czas: str, nagroda: str, zwyciezcy: int = 1):
        # Proste parsowanie czasu
        seconds = 0
        if czas.endswith("m"):
            seconds = int(czas[:-1]) * 60
        elif czas.endswith("h"):
            seconds = int(czas[:-1]) * 3600
        elif czas.endswith("d"):
            seconds = int(czas[:-1]) * 86400
        else:
            await interaction.response.send_message("Zły format czasu. Użyj np. 30m, 1h, 1d", ephemeral=True)
            return

        end_time = datetime.utcnow() + timedelta(seconds=seconds)

        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            description=f"**Nagroda:** {nagroda}\n**Zwycięzców:** {zwyciezcy}\n**Kończy się:** <t:{int(end_time.timestamp())}:R>",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Hosted by {interaction.user.display_name}")

        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.add_reaction("🎉")

        # Zapis do bazy
        async with database.aiosqlite.connect(database.DB_NAME) as db:
            await db.execute(
                "INSERT INTO giveaways (message_id, channel_id, prize, end_time, winners) VALUES (?, ?, ?, ?, ?)",
                (message.id, interaction.channel.id, nagroda, end_time.isoformat(), zwyciezcy)
            )
            await db.commit()

        # Czekanie
        await asyncio.sleep(seconds)

        # Losowanie
        message = await interaction.channel.fetch_message(message.id)
        users = []
        async for user in message.reactions[0].users():
            if not user.bot:
                users.append(user)

        if len(users) == 0:
            await interaction.channel.send("Nikt nie wziął udziału w giveawayu.")
            return

        winners = random.sample(users, min(zwyciezcy, len(users)))
        winners_text = ", ".join(w.mention for w in winners)

        await interaction.channel.send(f"🎉 Gratulacje {winners_text}! Wygraliście: **{nagroda}**")

async def setup(bot):
    await bot.add_cog(Giveaways(bot))
