from io import BytesIO
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from bson.objectid import ObjectId
from wikie import WikiElteBot



class Resources(commands.Cog):
    def __init__(self, bot: WikiElteBot):
        self.bot: WikiElteBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Resources Cog Loaded")

    @app_commands.command(name="create", description="Adds Resources")
    async def create(self, interaction: discord.Interaction, file: Optional[discord.Attachment]):
        if file is None:
            return await interaction.response.send_message(f"Proceeding without File Upload")
        # How to read the file
        # print(type(await file.read()))
        file_id = await self.bot.db.uploadFile(await file.read(), file.filename)
        await interaction.response.send_message(f"Uploaded File {file_id} to bucket")

    @app_commands.command(name="getfile", description="Test Command to get files from database")
    async def getfile(self, interaction: discord.Interaction, file_id: str):
        meta = await self.bot.db.getFile(ObjectId(file_id))
        await interaction.response.send_message("Lets Analyze", file=discord.File(BytesIO(meta['data']), filename=meta['name']))


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(Resources(bot=bot))