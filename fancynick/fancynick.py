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
            "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
            "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
            "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９"
            "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
            "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
            "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯0123456789",
            "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻0123456789",
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
        