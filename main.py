from os import getenv
from wikie import WikiElteBot
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    bot: WikiElteBot = WikiElteBot()
    print(getenv("TOKEN"))
    bot.run(getenv('TOKEN'))
