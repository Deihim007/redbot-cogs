from .fancynick import FancyNick

async def setup(bot):
    cog = FancyNick(bot)
    bot.add_cog(cog)