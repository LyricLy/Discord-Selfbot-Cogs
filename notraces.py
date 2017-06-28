import discord, asyncio
from cogs.utils.checks import *

class notraces:

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.delete_after = 30
        config = load_config()
        self.cmd_prefix = config["cmd_prefix"]
        self.bot_prefix = config["bot_identifier"]
    
    @commands.command(aliases=['fu'], pass_context=True)
    async def finduser(self, ctx):
        if message.content.startswith("{p}notrace".format(p=self.cmd_prefix)):
            params = message.content.split(' ', 1)
            await self.bot.delete_message(message)
            if len(params) == 2: self.delete_after = int(params[1].strip())
            await self.bot.send_message(message.channel, "{p} No Traces mode activated, all following messages will auto-delete after {t} secs.".format(p=self.bot_prefix,t=self.delete_after))
            self.active = True
        elif message.content == "{p}trace".format(p=self.cmd_prefix):
            await self.bot.delete_message(message)
            await self.bot.send_message(message.channel, "{p} No Traces mode deactivated.".format(p=self.bot_prefix))
            self.active = False
        elif self.active:
            await asyncio.sleep(self.delete_after)
            await self.bot.delete_message(message)
        return True
    
def setup(bot):
    bot.add_cog(notraces(bot))
