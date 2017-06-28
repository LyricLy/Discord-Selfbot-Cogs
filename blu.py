import discord, asyncio
from cogs.utils.checks import *

class blu:

    def __init__(self, bot):
        self.bot = bot
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    async def on_message(self, message):
        if message.content == "plu":
            await self.bot.send_message(message.channel, "is garnicht da {p}".format(p=self.bot_prefix))
    
def setup(bot):
    bot.add_cog(blu(bot))
