import os
import dotenv
import sys
from datetime import datetime
from typing import List
import aiohttp
import discord
from discord.ext import commands
from lib import DatabaseClient


async def get_prefix(bot, message: discord.Message) -> List[str]:
    return commands.when_mentioned_or("wiki ")(bot, message)


def Get_Intents() -> discord.Intents:
    intents = discord.Intents.all()
    return intents


class WikiElteBot(commands.AutoShardedBot):
    session: aiohttp.ClientSession

    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            description="Wikipedia for ELTE",
            case_insensitive=True,
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(
                roles=False,
                everyone=False),
            max_messages=100,

        )
        dotenv.load_dotenv()
        self.connector = None
        self.repo: str = "https://github.com/Ali-TM-original"
        self.launch_time: datetime = datetime.utcnow()
        self.owner_id = os.getenv('OWNER')
        self.db = DatabaseClient()

    async def setup_hook(self):
        self.connector = aiohttp.TCPConnector(limit=200)
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": f"python-requests/2.25.1 wikielte /1.1.0 Python/{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} aiohttp/{aiohttp.__version__}"},
            connector=self.connector,
            timeout=aiohttp.ClientTimeout(total=60),
        )
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                except Exception:
                    print(f"Could not load {file[:-3]}")


    async def on_ready(self):
        print(f"{self.user.display_name} is connected to server.")
        print(f"Bot Latency is: {round(self.latency * 1000)} ms")