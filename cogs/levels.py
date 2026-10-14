import discord
from discord.ext import commands
from discord import app_commands
import database
import random

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user = await database.get_user(message.author.id)
        xp_gain = random.randint(5, 15)
        new_xp = user["xp"] + xp_gain
        new_level = user["level"]

        # Sprawdzanie level up
        xp_needed = new_level * 100
        if new_xp >= xp_needed:
            new_level += 1
            new_xp = 0
            await message.channel.send(f"🎉 {message.author.mention} awansował na poziom **{new_level}**!")

        await database.update_user(message.author.id, xp=new_xp, level=new_level)

    @app_commands.command(name="poziom", description="Sprawdź swój poziom")
    async def poziom(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        user = await database.get_user(member.id)

        embed = discord.Embed(
            title=f"Poziom {member.display_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Poziom", value=user["level"], inline=True)
        embed.add_field(name="XP", value=f"{user['xp']} / {user['level'] * 100}", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))
