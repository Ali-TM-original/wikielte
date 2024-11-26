import datetime
import os
import discord
import humanize
import psutil
from discord import app_commands
from discord.ext import commands
from wikie import WikiElteBot


def is_team():
    def predicate(ctx):
        return ctx.author.id == int(os.getenv("OWNER"))

    return commands.check(predicate)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


class Admin(commands.Cog):
    def __init__(self, bot: WikiElteBot):
        self.bot: WikiElteBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Admin Cog Loaded")

    @commands.command(name="reload",
                      aliases=["rel"],
                      help="Reloads specific extensions of bot or whole bot"
                           "only if you have perms")
    @is_team()
    async def reload(self, ctx, *, files: str):
        if files.lower() == "all":
            check = []
            errors = {}

            extensions = self.bot.extensions.copy()
            for file in extensions:
                try:
                    await self.bot.reload_extension(f"{file}")
                except Exception as e:
                    errors[f"{file}"] = e
                finally:
                    check.append(f"{file}")

            text = "\n".join(
                f"{module}" if module not in errors else f"{module}\n{errors[module]}"
                for module in check)
            title = "Reloaded all." if len(check) - len(list(errors)) == len(
                extensions) else f"{len(check) - len(list(errors))}/{len(extensions)} cogs reloaded."

            await ctx.send(embed=discord.Embed(title=title, description=text, color=0xffcff1))
        else:
            try:
                await self.bot.reload_extension(f"cogs.{files}")
                return await ctx.send(f":white_check_mark:  Reloaded cogs: **{files}**")
            except Exception as e:
                return await ctx.send(
                    f":negative_squared_cross_mark:  Something went "
                    f"wrong while reloading **{files}**:\n```py\n{e}\n```")

    @commands.command(name="sync")
    async def sync(self, ctx):
        print(ctx.guild)
        self.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Creating {len(synced)} slash command(s).")

    @app_commands.command(name="ping", description="test slash command")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.")

    @app_commands.command(name="botinfo", description="Tells Information About the bot")
    @is_team()
    async def botinfo(self, interaction: discord.Interaction):
        shards_guilds = {i: 0 for i in range(len(self.bot.shards))}
        for guild in self.bot.guilds:
            shards_guilds[guild.shard_id] += 1

        hdd = psutil.disk_usage('/')
        m = psutil.Process().memory_full_info()
        ram_usage = get_size(m.rss)

        em = discord.Embed(
            description=f"**Total Shards**: {len(self.bot.shards)}\n"
                        f"**Guild Shard**: #{interaction.guild.shard_id}\n"
                        f"**RAM Used**: {ram_usage}\n"
                        f"**Total Guilds**: {humanize.intcomma(len(self.bot.guilds))}\n"
                        f"**Storage**: {get_size(hdd.used)} / {get_size(hdd.total)}\n",
            color=interaction.user.color,
            timestamp=datetime.datetime.utcnow())

        em.set_thumbnail(url=self.bot.user.avatar)

        for shard_id, shard in self.bot.shards.items():
            em.add_field(name=f"Shard #{shard_id}", value=f"Latency: `{round(shard.latency * 1000, 2)}`ms\n"
                                                          f"Guilds: {humanize.intcomma(shards_guilds[shard_id])}")

        await interaction.response.send_message(embed=em)


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(Admin(bot=bot))
