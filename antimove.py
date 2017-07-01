import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class antimove:

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.allowed = False
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    async def on_voice_state_update(self, before, after):
        if not self.active: return
        if not before == self.bot.user: return
        if before.voice.voice_channel == after.voice.voice_channel: return
        if self.allowed: self.allowed = False; return
        try:
            self.allowed = True
            await self.bot.move_member(before, before.voice.voice_channel)
            print("Someone tried to move me from \"{b}\" to \"{a}\" on server \"{s}\"!".format(b=before.voice.voice_channel,a=after.voice.voice_channel,s=before.server.name))
        except discord.Forbidden: print("Insufficient to move yourself back to \"{n}\" on server \"{s}\"".format(n=before.voice.voice_channel,s=before.server.name))

    @commands.command(aliases=['am'], pass_context=True)
    async def antimove(self, ctx):
        """Toggles Voice Antimove so you stay in the channel you choose."""
        self.active = not self.active
        await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + 'Antimove set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(antimove(bot))
