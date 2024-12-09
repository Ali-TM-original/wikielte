import os
import discord
from discord import app_commands
from discord.ext import commands
from wikie import WikiElteBot
from openai import OpenAI


class AiCog(commands.Cog):
    def __init__(self, bot: WikiElteBot):
        self.bot: WikiElteBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ai Cog Loaded")

    @app_commands.command(name="prompt", description="Process a prompt with OpenAI")
    async def prompt(self, interaction: discord.Interaction, prompt: str):
        try:
            client = OpenAI()
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-instruct",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            print(completion)
            response_text = completion.choices[0].message
            await interaction.response.send_message(response_text)
        except Exception as e:
            # Handle errors and send a friendly message
            await interaction.response.send_message(f"An error occurred: {str(e)}")


async def setup(bot):
    # Add the cog to the bot
    await bot.add_cog(AiCog(bot=bot))
