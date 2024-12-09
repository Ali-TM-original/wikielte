import asyncio
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

    @app_commands.command(name="prompt", description="Talk to your AI girlfriend!")
    async def prompt(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        try:
            # Add personality context to the prompt
            context = (
                "You are an old grumpy angry grandpa trying to help the user."
            )
            full_prompt = f"{context}\nUser: {prompt}\nLily:"

            # Generate the response
            res = self.model.generate_content(prompt)
            await interaction.followup.send(res.text)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            await interaction.followup.send("OOPS an error occured")


async def setup(bot):
    # Add the cog to the bot
    await bot.add_cog(AiCog(bot=bot))
