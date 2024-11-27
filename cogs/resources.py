import os
from io import BytesIO
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from bson.objectid import ObjectId
from wikie import WikiElteBot
from nudenet import NudeDetector
from lib import ResourceModel, Pagination


class Resources(commands.Cog):
    def __init__(self, bot: WikiElteBot):
        self.bot: WikiElteBot = bot
        os.makedirs("./temp", exist_ok=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Resources Cog Loaded")

    @app_commands.command(name="create", description="Adds Resources")
    async def create(self, interaction: discord.Interaction, name: str, course: str, description: str,
                     file: Optional[discord.Attachment]):
        # Allowed image extensions
        image_extensions = [".png", ".jpg", ".jpeg"]
        fileID = None
        if file is not None and any(file.filename.lower().endswith(ext) for ext in image_extensions):
            try:
                # Read the file contents
                file_data = await file.read()

                # Save the file to the ./temp directory
                file_path = f"./temp/{file.filename}"
                with open(file_path, "wb") as f:
                    f.write(file_data)
                result = self.bot.detector.detect(file_path)
                os.remove(f"./temp/{file.filename}")
                if not result:
                    fileID = await self.bot.db.uploadFile(await file.read(), file.filename)
                else:
                    return await interaction.response.send_message("Cannot Create File avoid sending NSFW content")
            except Exception as e:
                return await interaction.response.send_message(f"Failed to process")

        if await self.bot.db.createResource(
                ResourceModel(name=name, course=course, description=description, creatorID=interaction.user.id,
                              creatorName=interaction.user.global_name, fileID=fileID)
        ):
            return await interaction.response.send_message(f"Creating Resource")
        return await interaction.response.send_message(f"Failed to create Resource")

    @app_commands.command(name="list", description="Lists resources")
    async def list(self, interaction: discord.Interaction, course: Optional[str]):
        if not course:
            res = await self.bot.db.getAllResources()
        else:
            res = await self.bot.db.filterByCourse(course)
        if not res:
            return await interaction.response.send_message("Could not find course")
        data = [f"**Name**: {i['name']}, **Course**: {i['course']}" for i in res]
        L = 10

        async def get_page(page: int):
            emb = discord.Embed(title="Resources", description="")
            offset = (page - 1) * L
            for user in data[offset:offset + L]:
                emb.description += f"{user}\n"
            emb.set_author(name=f"Requested by {interaction.user}")
            n = Pagination.compute_total_pages(len(data), L)
            emb.set_footer(text=f"Page {page} from {n}")
            return emb, n

        await Pagination(interaction, get_page).navegate()

    @app_commands.command(name="deleteresource", description="This Commands deletes a resource")
    async def deleteresource(self, interaction: discord.Interaction, name: str, course:str):
        if await self.bot.db.deleteOne(name, course, int(interaction.user.id)):
            return await interaction.response.send_message("Deleted Resource")
        return await interaction.response.send_message("Could not delete resource")

    @app_commands.command(name="getresource", description="This Commands gets individual resources")
    async def getresource(self, interaction: discord.Interaction, name: str, course: str):
        data = await self.bot.db.getOne(name, course)
        if not data:
            return await interaction.response.send_message("Resource does not exist")
        try:
            f = None
            if data['fileID'] is not None:
                meta = await self.bot.db.getFile(ObjectId(data['fileID']))
                f = discord.File(BytesIO(meta['data']), filename=meta['name'])
            emb = discord.Embed(title=data.get("name", "No Title"), description=data.get("course", "No Course"))
            emb.set_author(name=f"Requested by {interaction.user}")
            emb.add_field(name="Description", value=data.get("description", "No description available"), inline=False)
            emb.set_footer(text=f"Created by {data.get('creatorName', 'Unknown')}")
            return await interaction.response.send_message(embed=emb, file=f)
        except Exception as e:
            print(e)
            return await interaction.response.send_message("Failed to fetch data")

    @app_commands.command(name="getfile", description="Test Command to get files from database")
    async def getfile(self, interaction: discord.Interaction, file_id: str):
        meta = await self.bot.db.getFile(ObjectId(file_id))
        await interaction.response.send_message("Lets Analyze",
                                                file=discord.File(BytesIO(meta['data']), filename=meta['name']))


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(Resources(bot=bot))
