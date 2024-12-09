import os
import discord
from discord import app_commands
from discord.ext import commands
from wikie import WikiElteBot
import google.generativeai as genai


class AiCog(commands.Cog):
    def __init__(self, bot: WikiElteBot):
        self.bot: WikiElteBot = bot
        self.model = genai.GenerativeModel("gemini-pro")
        genai.configure(api_key=os.getenv("AI_API_KEY"))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ai Cog Loaded")

    @app_commands.command(name="prompt", description="Process a prompt with OpenAI")
    async def prompt(self, interaction: discord.Interaction, prompt: str):
        try:
            res = self.model.generate_content(prompt)
            if not res.text or not res or res.text == '':
                raise Exception
            await interaction.response.send_message(res.text)
        except Exception as e:
            # Handle errors and send a friendly message
            await interaction.response.send_message(f"An error occurred: {str(e)}")


async def setup(bot):
    # Add the cog to the bot
    await bot.add_cog(AiCog(bot=bot))
