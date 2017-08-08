import requests, discord, json
from discord.ext import commands

'''Joke generator.'''


class JokeGenerator:

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def joke(self, ctx):
        """Returns a random Joke from https://tambalapi.herokuapp.com via https://github.com/KiaFathi/tambalAPI"""
        response = json.loads(requests.get("https://tambalapi.herokuapp.com").text)
        await ctx.message.edit(content=":rofl: {}".format(response[0]["joke"]))


    @commands.command(pass_context=True)
    async def chuck(self, ctx):
        """Returns a random Chuck Norris joke from http://www.icndb.com/api/"""
        response = requests.get("http://api.icndb.com/jokes/random").text
        await ctx.message.edit(content=":rofl: {}".format(json.loads(response)["value"]["joke"]))


def setup(bot):
    bot.add_cog(JokeGenerator(bot))
