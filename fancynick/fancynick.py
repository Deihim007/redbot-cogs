from ast import alias
import re
from click import command
import discord
from redbot.core import Config, checks, commands

class FancyNick(commands.Cog):
    """FancyNick cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=707350954969792584)
        default_guild = {"font": None, "prefix": None, "suffix": None, "enabled": False}
        self.config.register_guild(**default_guild)
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        self.fonts = [
            "๐๐ต๐๐๐ธ๐น๐ข๐ป๐ผ๐ฅ๐ฆ๐ฟ๐๐ฉ๐ช๐ซ๐ฌ๐๐ฎ๐ฏ๐ฐ๐ฑ๐ฒ๐ณ๐ด๐ต๐ถ๐ท๐ธ๐น๐๐ป๐๐ฝ๐พ๐ฟ๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซ",
            "๐ธ๐นโ๐ป๐ผ๐ฝ๐พโ๐๐๐๐๐โ๐โโโ๐๐๐๐๐๐๐โค๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐ ๐ก๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซ๐๐๐๐๐๐๐๐๐ ๐ก",
            "๏ผก๏ผข๏ผฃ๏ผค๏ผฅ๏ผฆ๏ผง๏ผจ๏ผฉ๏ผช๏ผซ๏ผฌ๏ผญ๏ผฎ๏ผฏ๏ผฐ๏ผฑ๏ผฒ๏ผณ๏ผด๏ผต๏ผถ๏ผท๏ผธ๏ผน๏ผบ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ฝ๏ผ๏ผ๏ผ๏ผ๏ผ๏ผ๏ผ๏ผ๏ผ๏ผ"
            "๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐ ๐ก๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซ๐ฌ๐ญ๐ฎ๐ฏ๐ฐ๐ฑ๐ฒ๐ณ๐๐๐๐๐๐๐๐๐๐",
            "๐๐๐๐๐๐๐๐๐๐๐๐๐ ๐ก๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซ๐ฌ๐ญ๐ฎ๐ฏ๐ฐ๐ฑ๐ฒ๐ณ๐ด๐ต๐ถ๐ท๐ธ๐น๐บ๐ป๐ผ๐ฝ๐พ๐ฟ๐๐๐๐๐๐๐๐๐ฌ๐ญ๐ฎ๐ฏ๐ฐ๐ฑ๐ฒ๐ณ๐ด๐ต",
            "๐ผ๐ฝ๐พ๐ฟ๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐ ๐ก๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซ๐ฌ๐ญ๐ฎ๐ฏ0123456789",
            "๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐ ๐ก๐ข๐ฃ๐ค๐ฅ๐ฆ๐ง๐จ๐ฉ๐ช๐ซ๐ฌ๐ญ๐ฎ๐ฏ๐ฐ๐ฑ๐ฒ๐ณ๐ด๐ต๐ถ๐ท๐ธ๐น๐บ๐ป0123456789",
        ]

    async def makefancy(self, member, nick):
        # strip anything but letters and numbers from name
        if nick:
            name = nick
        else:
            name = re.sub(r'[^A-Za-z0-9]+', '', member.name)
        
        # check if name is empty
        if not name:
            name = "Unknown"

        # get font
        font = await self.config.guild(member.guild).font()

        nick = ""
        # conversion
        for i in name:
            if i in self.letters:
                nick += self.fonts[font][self.letters.index(i)]
            else:
                nick += i

        # check prefix
        prefix = await self.config.guild(member.guild).prefix()
        if prefix:
            nick = prefix + nick

        # check suffix
        suffix = await self.config.guild(member.guild).suffix()
        if suffix:
            nick += suffix

        # set nick
        await member.edit(nick=nick)

    @checks.mod_or_permissions(manage_messages=True)
    @commands.group()
    async def fancynick(self, ctx):
        """FancyNick commands"""
        pass

    @fancynick.command()
    async def reset(self, ctx, *, member: discord.Member = None):
        """Reset user nick"""
        if member is None:
            member = ctx.author
        # check if bot can change nick
        if not ctx.me.guild_permissions.manage_nicknames:
            return await ctx.send("I don't have permission to change nicknames.")
        # check for role hierarchy and bot role
        if ctx.me.top_role.position < member.top_role.position:
            return await ctx.send("I can't change nicknames of people with higher roles than me.")
        # reset nick
        await self.makefancy(member)
        await ctx.tick()

    @fancynick.command()
    async def set(self, ctx, member: discord.Member, *, nick: str):
        """Set user nick"""
        if member is None:
            member = ctx.author
        # check if bot can change nick
        if not ctx.me.guild_permissions.manage_nicknames:
            return await ctx.send("I don't have permission to change nicknames.")
        # check for role hierarchy and bot role
        if ctx.me.top_role.position < member.top_role.position:
            return await ctx.send("I can't change nicknames of people with higher roles than me.")
        # set nick
        await self.makefancy(member, nick)
        await ctx.tick()

    @fancynick.command()
    async def generate(self, ctx, *, name: str):
        """Generate user nick"""
        # get font
        font = await self.config.guild(ctx.guild).font()

        nick = ""
        # conversion
        for i in name:
            if i in self.letters:
                nick += self.fonts[font][self.letters.index(i)]
            else:
                nick += i

        # check prefix
        prefix = await self.config.guild(ctx.guild).prefix()
        if prefix:
            nick = prefix + nick

        # check suffix
        suffix = await self.config.guild(ctx.guild).suffix()
        if suffix:
            nick += suffix

        await ctx.send(nick)

    @checks.admin_or_permissions(manage_roles=True)
    @commands.group()
    async def fancynickset(self, ctx):
        """FancyNick settings"""
        pass

    @fancynickset.command()
    async def font(self, ctx, font: int):
        """Set the font"""
        if font > len(self.fonts):
            await ctx.send("Font not found")
            return
        await self.config.guild(ctx.guild).font.set(font)
        await ctx.tick()

    @fancynickset.command()
    async def prefix(self, ctx, *, prefix = None):
        """Set the prefix"""
        await self.config.guild(ctx.guild).prefix.set(prefix)
        await ctx.tick()

    @fancynickset.command()
    async def suffix(self, ctx, *, suffix = None):
        """Set the suffix"""
        await self.config.guild(ctx.guild).suffix.set(suffix)
        await ctx.tick()

    @fancynickset.command()
    async def enabled(self, ctx, enabled: bool):
        """Set FancyNick enabled"""
        await self.config.guild(ctx.guild).enabled.set(enabled)
        await ctx.tick()

    # on member joining guild
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # check if enabled
        if not await self.config.guild(member.guild).enabled():
            return
        
        # make fancy
        await self.makefancy(member)
        