import os
import dotenv
import discord
import humanize
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound


class Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.error(coro=self.__dispatch_to_app_command_handler)
        dotenv.load_dotenv()

    # Custom Command Handling
    async def __dispatch_to_app_command_handler(self, interaction: discord.Interaction,
                                                error: discord.app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Handler Loaded")

    @commands.Cog.listener("on_app_command_error")
    async def get_app_command_error(self, interaction: discord.Interaction,
                                    error: discord.app_commands.AppCommandError):

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(
                description="You can only use this command only in **NSFW** channels.",
                color=0x2F3136)
            return await interaction.response.send_message(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                description=f"Missing the **`{error.param.name}`** argument.",
                color=0x2F3136)
            return await interaction.response.send_message(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            d = ", ".join(error.missing_perms).replace("_", " ")
            s = d.title()
            em = discord.Embed(title="⚠ | Missing Permissions!",
                               description=f"You don't have **`{s}`** permission to do this command.",
                               color=0x2F3136)
            return await interaction.response.send_message(embed=em)

        elif isinstance(error, commands.BotMissingPermissions):
            d = ", ".join(error.missing_perms).replace("_", " ")
            s = d.title()
            try:
                em = discord.Embed(title="⚠ | Missing Permissions!",
                                   description=f"I'm missing the **`{s}`** permission to run this command",
                                   color=0x2F3136)
                return await interaction.response.send_message(embed=em)
            except Exception:
                pass

        elif isinstance(error, discord.Forbidden):
            try:
                return await interaction.response.send_message(f"**`{error.status}`**: **{error.text}** (Code `{error.code}`)")
            except Exception:
                pass

        elif isinstance(error, commands.CommandOnCooldown):
            return await interaction.response.send_message("Yo, you have a cool down  bitch**{}**.".format(
                humanize.precisedelta(error.retry_after)))

        elif isinstance(error, commands.MemberNotFound):
            d = "".join(error.args)
            return await interaction.response.send_message(f"{d}")


        elif isinstance(error, commands.BadArgument):
            pass

        elif isinstance(error, commands.NotOwner):
            return

        elif isinstance(error, CommandNotFound):
            return

        elif isinstance(error, commands.BotMissingPermissions):
            return await interaction.response.send_message("***Yo I am missing permissions***")

        elif isinstance(error, commands.MaxConcurrencyReached):
            cmd = interaction.command.name
            return await interaction.response.send_message(f"There's already a **{cmd}** command running.")

        elif isinstance(error, commands.CheckFailure):
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        if isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(
                description="You can only use this command only in **NSFW** channels.",
                color=0x2F3136)
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                description=f"Missing the **`{error.param.name}`** argument.",
                color=0x2F3136)
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            d = ", ".join(error.missing_perms).replace("_", " ")
            s = d.title()
            em = discord.Embed(title="⚠ | Missing Permissions!",
                               description=f"You don't have **`{s}`** permission to do this command.",
                               color=0x2F3136)
            await ctx.send(embed=em)

        elif isinstance(error, commands.BotMissingPermissions):
            d = ", ".join(error.missing_perms).replace("_", " ")
            s = d.title()
            try:
                em = discord.Embed(title="⚠ | Missing Permissions!",
                                   description=f"I'm missing the **`{s}`** permission to run this command",
                                   color=0x2F3136)
                await ctx.send(embed=em)
            except Exception:
                await ctx.send(f"I'm missing the **`{s}`** permission to run this command")

        elif isinstance(error, discord.Forbidden):
            try:
                await ctx.send(
                    f"**`{error.status}`**: **{error.text}** (Code `{error.code}`)")
            except Exception:
                pass

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply("Yo, you have a cool down  bitch**{}**.".format(
                humanize.precisedelta(error.retry_after)))

        elif isinstance(error, commands.MemberNotFound):
            d = "".join(error.args)
            return await ctx.send(f"{d}")

        elif isinstance(error, commands.BadArgument):
            pass

        elif isinstance(error, commands.NotOwner):
            return

        elif isinstance(error, CommandNotFound):
            return

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("***Yo I am missing permissions***")

        elif isinstance(error, commands.MaxConcurrencyReached):
            cmd = ctx.command.qualified_name
            return await ctx.send(f"There's already a **{cmd}** command running.")

        elif isinstance(error, commands.CheckFailure):
            pass

        else:
            chan = self.bot.get_channel(os.getenv("ERRORLOGS")) # here use env
            print(error)
            if ctx.author:
                auth = f"{ctx.author.name}#{ctx.author.discriminator}"
                command = ctx.command.qualified_name
                em = discord.Embed(title="Error",
                                   description=f"Errored in **{ctx.guild.name}** by : **{auth}** with **{command}**\n```py\n{error}\n```",
                                   color=0x2F3136)
                await chan.send(embed=em)


async def setup(bot):
    await bot.add_cog(Handler(bot))