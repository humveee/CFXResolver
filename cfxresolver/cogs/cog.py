import discord,requests,cloudscraper,json,os,shutil
from discord.ext import commands

class colors:
    byellow = u'\u001b[33;1m'
    reset = u'\u001b[0m'
    bcyan = u'\u001b[36;1m'
    bmagenta = u'\u001b[35;1m'
    bred = u'\u001b[31;1m'
    bblue = u'\u001b[34;1m'
    bgreen = u'\u001b[32;1m'


class CFXResolve(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    #region genembed
    def generateembed(self, **kwargs):
        if kwargs.get("title") == None:
            return print(colors.bred+"Missing title or description argument"+colors.reset)
        embed = discord.Embed()
        
        embed.title = kwargs.get("title")

        if kwargs.get("description") is not None:
            embed.description = kwargs.get("description")

        if kwargs.get("fields") is not None:
            for field in kwargs.get("fields"):

                embed.add_field(name=kwargs.get("fields").get(field)[0], value=kwargs.get("fields").get(field)[1], inline=kwargs.get("fields").get(field)[2] if len(kwargs.get("fields").get(field)) > 2 else True)
        if kwargs.get("color") is not None:
            embed.color = kwargs.get("color")
        if kwargs.get("image") is not None:
            embed.set_image(kwargs.get("image"))
        if kwargs.get("thumbnail") is not None:
            embed.set_thumbnail(kwargs.get("thumbnail"))
        if kwargs.get("author") is not None:
            embed.set_author(name=kwargs.get("author").get("name"), url=kwargs.get("author").get("url"),icon_url=kwargs.get("icon_url"))
        if kwargs.get("footer") is not None:
            embed.set_footer(text=kwargs.get("footer").get("text"), icon_url=kwargs.get("footer").get("icon_url"))
        return embed
    #endregion
    
        
    @commands.command()
    async def resolve(self,ctx:commands.Context,servercode=None):
        if os.path.exists(os.path.join("temp",str(ctx.author.id))):
            return 
        if isinstance(servercode, type(None)):

            return await ctx.send(embed=self.generateembed(
                title = "Error",
                description="Join code is none",
                color=discord.Color.random(),
                footer = {
                    "text":str(ctx.author.display_name+"#"+ctx.author.discriminator),
                    "icon_url":ctx.author.display_avatar.url
                }
            ))

        
        #region resolver start
        scraper = cloudscraper.create_scraper()
        req = scraper.get("https://servers-frontend.fivem.net/api/servers/single/{code}".format(
            code=servercode
        ))
        if req.headers['Content-Type'] != "application/json; charset=utf-8":
            return await ctx.send(embed=self.generateembed(
                title = "Error",
                description = "unspecified error",
                color = discord.Color.random(),
                footer = {
                    "text":str(ctx.author.display_name+"#"+ctx.author.discriminator),
                    "icon_url":ctx.author.display_avatar.url
                }
            ))
        if 'error' in req.json():
            return await ctx.send(embed=self.generateembed(
                title = "Error",
                description = req.json()['error'],
                color = discord.Color.random(),
                footer = {
                    "text":str(ctx.author.display_name+"#"+ctx.author.discriminator),
                    "icon_url":ctx.author.display_avatar.url
                }
            ))
        if servercode not in req.text:
            return "unspecified error"
        os.mkdir("temp"+"//"+str(ctx.author.id))
        with open("temp"+"//"+str(ctx.author.id)+"//"+"players.txt", "w+", encoding="utf-8") as players:
            for player in req.json()['Data']['players']:
                players.write("ID: {playerid}, Identifiers: {identifiers}, Name: {name}, Ping: {ping}\n".format(
                    playerid = player['id'],
                    identifiers = player['identifiers'],
                    name = player['name'],
                    ping = player['ping']
                ))
            players.close()
        with open(os.path.join("temp",str(ctx.author.id), "resources.txt"), "w+", encoding="utf-8") as resources:
            for resource in req.json()['Data']['resources']:
                resources.write(str(resource)+"\n")
            resources.close()
        ip = req.json()['Data']['connectEndPoints'][0]
        ipjson = requests.get("http://ip-api.com/json/%s" % (ip.split(":")[0]))

        await ctx.send(embed=self.generateembed(
            title = "INFO",
            color = discord.Color.random(),
            fields={
                "playersfield":[
                    "Players",
                    str("{curr}/{max}").format(curr=req.json()['Data']['clients'], max=str(req.json()['Data']['sv_maxclients'])),
                    True
                ],
                "serverfiles":[
                    "Server Files",
                    req.json()['Data']['server'],
                    True
                ],
                "ipfield":[
                    "Server Endpoint ('s)",
                    req.json()['Data']['connectEndPoints'],
                    True
                ],
                "resourcesfield":[
                    "Server resources",
                    str(len(req.json()['Data']['resources'])),
                    True
                ],
                "svlan":[
                    "sv_lan 1",
                    str(req.json()['Data']['vars']['sv_lan']),
                    True
                
                ],
                "gamebuild":[
                    "Build",
                    str(req.json()['Data']['vars']['sv_enforceGameBuild']),
                    True
                ],
                "country":[
                    "Country",
                    ipjson.json()['country'],
                    True
                ],
                "city":[
                    "City",
                    ipjson.json()['city'],
                    True
                ],
                "countrycode":[
                    "Country Code",
                    ipjson.json()['countryCode'],
                    True
                ],
                "isp":[
                    "ISP",
                    ipjson.json()['isp'],
                    True
                ],
                "zipcode":[
                    "Zip-Code",
                    ipjson.json()['zip'],
                    True
                ],
                "timezone":[
                    "Time Zone",
                    ipjson.json()['timezone'],
                    True
                ]
            },
            footer={
                "text":str(ctx.author.display_name+"#"+ctx.author.discriminator),
                "icon_url":ctx.author.display_avatar.url
            }
        ), files={
            discord.File(os.path.join("temp",str(ctx.author.id), "players.txt")),
            discord.File(os.path.join("temp", str(ctx.author.id), "resources.txt"))
        })
        return shutil.rmtree(os.path.join("temp", str(ctx.author.id)))
        #endregion
        
async def setup(bot:commands.Bot):
    await bot.add_cog(CFXResolve(bot))