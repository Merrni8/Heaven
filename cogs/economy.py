import discord
from discord.ext import commands
from discord import app_commands
import database
from datetime import datetime, timedelta

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balans", description="Sprawdź swoje pieniądze")
    async def balans(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        user = await database.get_user(member.id)

        embed = discord.Embed(
            title=f"Portfel {member.display_name}",
            description=f"💰 **{user['money']}** monet",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Odbierz codzienną nagrodę")
    async def daily(self, interaction: discord.Interaction):
        user = await database.get_user(interaction.user.id)
        now = datetime.utcnow()

        if user["last_daily"]:
            last = datetime.fromisoformat(user["last_daily"])
            if now - last < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last)
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds % 3600) // 60
                await interaction.response.send_message(
                    f"Już odebrałeś daily! Wróć za {hours}h {minutes}min.",
                    ephemeral=True
                )
                return

        reward = 150
        new_money = user["money"] + reward
        await database.update_user(
            interaction.user.id,
            money=new_money,
            last_daily=now.isoformat()
        )

        await interaction.response.send_message(
            f"Odebrałeś **{reward}** monet! Masz teraz **{new_money}** 💰"
        )

    @app_commands.command(name="pay", description="Przelej pieniądze komuś")
    @app_commands.describe(member="Komu chcesz dać pieniądze", amount="Ile monet")
    async def pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if amount <= 0:
            await interaction.response.send_message("Kwota musi być większa od 0.", ephemeral=True)
            return

        if member.id == interaction.user.id:
            await interaction.response.send_message("Nie możesz płacić samemu sobie.", ephemeral=True)
            return

        sender = await database.get_user(interaction.user.id)
        if sender["money"] < amount:
            await interaction.response.send_message("Nie masz tyle monet.", ephemeral=True)
            return

        receiver = await database.get_user(member.id)

        await database.update_user(interaction.user.id, money=sender["money"] - amount)
        await database.update_user(member.id, money=receiver["money"] + amount)

        await interaction.response.send_message(
            f"Przelałeś **{amount}** monet do {member.mention}."
        )

async def setup(bot):
    await bot.add_cog(Economy(bot))
