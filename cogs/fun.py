import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from wikie import WikiElteBot
from asyncdagpi import ImageFeatures


class Fun(commands.Cog):
    def __init__(self, bot: WikiElteBot):
        self.bot: WikiElteBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Fun Cog Loaded")

    async def helper(self, interaction: discord.Interaction, feature: ImageFeatures, author: discord.Member = None):
        if author is None:
            author = interaction.user
        await interaction.response.defer()
        try:
            img = await self.bot.dagpi.image_process(feature=feature, url=author.avatar.url)
            file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
            await interaction.followup.send(file=file)
        except Exception as e:
            print(e)
            await interaction.response.send_message("Ah oh looks like there was an error")

    @app_commands.command(name="hitler", description="Applies a hitler cover. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hitler(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.hitler(), author)

    @app_commands.command(name="jail", description="Applies bars in front of profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jail(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.jail(), author)

    @app_commands.command(name="pixel", description="pixelates profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pixel(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.pixel(), author)

    @app_commands.command(name="ascii", description="converts profile pic into ascii art. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ascii(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.ascii(), author)

    @app_commands.command(name="rainbow", description="Applies a Rainbow filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rainbow(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.rainbow(), author)

    @app_commands.command(name="colors", description="Shows prominent colors in profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def colors(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.colors(), author)

    @app_commands.command(name="murica", description="Applies a American flag filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def america(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.america(), author)

    @app_commands.command(name="communism", description="Applies a communism filter on profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def communism(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.communism(), author)

    @app_commands.command(name="trigger", description="Applies a triggered filter profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def triggered(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.triggered(), author)

    @app_commands.command(name="wasted", description="GTA V wasted filter profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wasted(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.wasted(), author)

    @app_commands.command(name="invert", description="Inverts profile pic colors. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invert(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.invert(), author)

    @app_commands.command(name="sobel", description="Sobel filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sobel(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.sobel(), author)

    @app_commands.command(name="hog", description="hog filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hog(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.hog(), author)

    @app_commands.command(name="triangle", description="Triangular profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def triangle(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.triangle(), author)

    @app_commands.command(name="blur", description="Blurs profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blur(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.blur(), author)

    @app_commands.command(name="rgb", description="RGB filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rgb(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.rgb(), author)

    @app_commands.command(name="angel", description="Angelify your profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def angel(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.angel(), author)

    @app_commands.command(name="satan", description="Satanify your profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def satan(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.satan(), author)

    @app_commands.command(name="delete", description="Delete meme. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def delete(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.delete(), author)

    @app_commands.command(name="fedora", description="Fedora Linux. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fedora(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.fedora(), author)

    @app_commands.command(name="wanted", description="Wanted filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.wanted(), author)

    @app_commands.command(name="sith", description="Sith lord. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sith(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.sith(), author)

    @app_commands.command(name="trash", description="Turns profile pic to trash can. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trash(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.trash(), author)

    @app_commands.command(name="deepfry", description="Deep fries profile pic in oil. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deepfry(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.deepfry(), author)

    @app_commands.command(name="charcoal", description="Convert profile pic to organic substances. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def charcoal(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.charcoal(), author)

    @app_commands.command(name="posterize", description="Poster size filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def posterize(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.poster(), author)

    @app_commands.command(name="sepai", description="Applies sepai filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sepai(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.sepia(), author)

    @app_commands.command(name="swirl", description="Swirls profile pic. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def swirl(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.swirl(), author)

    @app_commands.command(name="paint", description="Paint filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def paint(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.paint(), author)

    @app_commands.command(name="night", description="Applies a night filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def night(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.night(), author)

    @app_commands.command(name="magic", description="Applies a magic filter. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def magic(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.magik(), author)

    @app_commands.command(name="obama", description="Obama awarding himself. Params= [user]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def obama(self, interaction: discord.Interaction, author: discord.Member = None):
        await self.helper(interaction, ImageFeatures.obama(), author)

    @app_commands.command(name="shatter", description="Shatters profile pic.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shatter(self, interaction: discord.Interaction):
        await self.helper(interaction, ImageFeatures.shatter(), interaction.user)


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(Fun(bot=bot))
