
import discord,os,sys
from discord.ext import commands
import config


class colors:
    byellow = u'\u001b[33;1m'
    reset = u'\u001b[0m'
    bcyan = u'\u001b[36;1m'
    bmagenta = u'\u001b[35;1m'
    bred = u'\u001b[31;1m'
    bblue = u'\u001b[34;1m'
    bgreen = u'\u001b[32;1m'

class variables:
    asciiart = u"""


 CCCCC  FFFFFFF XX    XX FFFFFFF iii              dd               
CC    C FF       XX  XX  FF          nn nnn       dd   eee  rr rr  
CC      FFFF      XXXX   FFFF    iii nnn  nn  dddddd ee   e rrr  r 
CC    C FF       XX  XX  FF      iii nn   nn dd   dd eeeee  rr     
 CCCCC  FF      XX    XX FF      iii nn   nn  dddddd  eeeee rr     
                                                                
    """
    pattern = "{}Created by {}github.com/humveee\n{}Running{}: %s\n{}Prefix:{}%s{}".format(colors.bmagenta,colors.bcyan,colors.bblue, colors.bcyan, colors.bmagenta, colors.bblue, colors.reset)


class functions:
    def clear():
        if 'win' in str(sys.platform):os.system("cls")
        if 'linux' in str(sys.platform):os.system("clear")


class CFXResolver(commands.Bot):
    def __init__(self, **options) -> None:
        super().__init__(**options)
    async def on_ready(self):
        functions.clear()
        print(colors.bmagenta+variables.asciiart+colors.reset)
        print(variables.pattern % ("{}%s{}#{}%s{}".format(colors.bmagenta, colors.bcyan,colors.bblue, colors.reset) % (self.user.display_name, self.user.discriminator), self.command_prefix))
        await self.loadall()
    async def loadall(self):
        print(colors.bcyan+"Loading cogs...")
        for cog in os.listdir("cogs"):
            if cog.endswith(".py"):
                
                try:
                    await self.load_extension("cogs.{cogname}".format(cogname=cog.rstrip(".py")))
                except Exception as err:
                    print("%sCan't load {cogname} Error : {error}%s".format(cogname=cog, error=err) % (colors.bred, colors.reset))
                    continue
                else:
                    print("%sLoaded {cogname}%s".format(cogname=cog) % (colors.bgreen, colors.reset))
            
bot = CFXResolver(command_prefix=config.prefix, intents=discord.Intents.all())


@bot.command()
async def nigga(ctx:commands.Context):
    await ctx.send("nihgggerrsrsr")


bot.run(config.token,log_handler=None)