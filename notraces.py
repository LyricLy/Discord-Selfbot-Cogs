import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class notraces:

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.delete_after = 30
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    @commands.command(aliases=['nt'], pass_context=True)
    async def notrace(self, ctx):
        """Toggles notraces mode which autodeletes **all** your messages after [seconds_tod_elete] have passed."""
        if not self.active:
        #if ' ' in ctx.message.content:
            params = ctx.message.content.split(' ', 1)
            if len(params) == 2: self.delete_after = int(params[1].strip())
            await self.bot.send_message(ctx.message.channel, "{p} No Traces mode activated, all following messages will auto-delete after {t} secs.".format(p=self.bot_prefix,t=self.delete_after))
            self.active = True
        else:
            await self.bot.send_message(ctx.message.channel, "{p} No Traces mode deactivated.".format(p=self.bot_prefix))
            self.active = False

    async def on_message(self, message):
        if self.active and message.author == self.bot.user:
            await asyncio.sleep(self.delete_after)
            await self.bot.delete_message(message)

def setup(bot):
    bot.add_cog(notraces(bot))
