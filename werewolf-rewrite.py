import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import nacl
import random
#import tenorpy
from asyncio import coroutine
import asyncio
import time

import nest_asyncio
nest_asyncio.apply()
#__import__('IPython').embed()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()
bot = commands.Bot(command_prefix='$')
global nospeak
nospeak = False




@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    #global nospeak
    #nospeak = False





def run_and_get(coro):
    task = asyncio.create_task(coro)
    asyncio.get_running_loop().run_until_complete(task)
    return task.result()


#print(TOKEN)
class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.t = tenorpy.Tenor()
        self.i = 0
        self.game_started = 0
        self.game_host = None
        self.players = []
        
        


    #@commands.Cog.listener()
    #async def on_voice_state_update(self,member, before, after):
        

    #@commands.Cog.listener()
    #async def on_message(self,message):
        
    def lobby_open():
        async def predicate(self,ctx):
            return self.game_started == 1  
        return commands.check(predicate)
    #condition for listener. called before __init__(), fix.
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.game_started == 1 and not(user in self.players):
            # on reaction. if game lobby open, and the user isn't already in the list
            self.players.append(user)
            await user.send("you have opted in for playing the game")
            # add to list, message in dms

    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if self.game_started == 1 and user in self.players:
            # on reaction remove, if game lobby is open and the user is in the list
            self.players.remove(user)
            await user.send("you have opted out for playing the game")
            # remove from list, message in dms


    @commands.command(name="new",pass_context=True)
    async def new(self, ctx):
        # set game lobby to open
        self.game_started = 1
        self.game_host = ctx.author
        self.players.append(ctx.author)
        # set game host for $start command, and add player to player list
        await ctx.send("react to this message to join the game")
        # create message for players to react to

    
    @commands.command(name="start")
    async def start(self, ctx):
        # if lobby is open, and the host used the command
        # if number of players meets the criteria. set to 0 for testing purposes
        if self.game_started == 1 and ctx.author ==self.game_host:
            if len(self.players) >= 0:                
                await ctx.send("starting game. check dms to find out your role")
                # send dm with role
                self.game_started = 2
                # set game lobby to started
                bot.add_cog(Game(bot,self.players,ctx))
                # start game cog

                # debugging shit:
                
                '''
                channel = ctx.author.voice.channel
                vc = await channel.connect()
                await self.play(ctx, "test.mp3")
                '''

                
                bot.remove_cog('Game')
                # remove game cog
            else:
                await ctx.send("not enough players to start")
            

class Game(commands.Cog):
    '''
    def __init__(self,bot,players):
        self.bot = bot
        self.players = players
        role_list = ["werewolf","werewolf","seer","toublemaker","drunk","insomniac","villager","villager"]
        self.role_list = role_list
        self.role_list_copy = role_list
        self.roles = {}
        self.middle_cards = []
        self.roles_copy = {}
        self.current_player = None
        self.other_werewolf = None
        for player in self.players:
            # for each player in lobby
            role = self.random_pick(role_list)
            # pick a random role
            try:
                # assign the player to that role
                self.roles[player] = role
                self.message_send(player,role)
                print(player)
            except:
                print("rip")
        
        for i in range(0,2):
            role = self.random_pick(role_list)
            self.middle_cards.append(role)
        self.roles_copy = self.roles
        '''
    def __init__(self,bot,players,ctx):
        self.bot=bot
        self.players=players
        role_list = ["werewolf","werewolf","seer","troublemaker","drunk","tanner","villager","villager","insomniac"]
        self.role_list = role_list
        random.shuffle(self.role_list)
        '''
        coro = self.werewolf(bot,players[0],None)
        self.fut = asyncio.Task(coro, loop = client.loop, name = "kms")
        self.fut.result()
        '''
        x = seer(bot,players[0],players,self.role_list)
        y = run_and_get(x.doRole())
        print(y)

        role_func = {"werewolf":werewolf,
                     "seer":seer,
                     "troublemaker":troublemaker,
                     "drunk":drunk,
                     "insomniac":insomniac,
                     "villager":villager,
                     "tanner":tanner}

        playerIterate = players
        #new_players = players
        used_roles = sorted(self.role_list[:-3],key = lambda x: role_list.index(x))
        roles = []
        self.roles_switched = self.role_list
        i=0
        for role in used_roles:
            player = playerIterate[role_list.index(role)]
            roles.append(role_func[role](bot,player,players,self.role_list))
            if role!= "insomniac":
                switch = run_and_get(roles[-1].doRole())
            else:
                run_and_get(roles[-1].doRole(self.roles_switched[i]))
            if switch != None:
                x1 = self.roles_switched[switch[0]]
                self.roles_switched[switch[0]] = self.roles_switched[switch[1]]
                self.roles_switched[switch[1]] = x1
                #x2 = roles_switched[switch[1]]
            playerIterate.remove(player)

        x = dict(zip(players,roles_switched))
        
        run_and_get(ctx.send(x))        
                

        #for switch in switches
        
        #run_and_get(
        #bot.add_cog(werewolf(bot,players[0],None))
        #await 
        #self.role_map = zip(self.role_list,self.players))

        

'''
class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass
'''

class base():
    def __init__(self,bot,player,role,players,roles):
        super().__init__()
        self.bot = bot
        self.player = player
        self.players = players
        self.role = role
        self.roles = roles
        self.emojis = {1:"1⃣",
                       2:"2⃣",
                       3:"3⃣",
                       4:"4⃣",
                       5:"5⃣",
                       6:"6⃣",
                       7:"7⃣",
                       8:"8⃣",
                       9:"9⃣"}
        '''
        coro = self.doRole()
        self.fut = asyncio.Task(coro, loop = client.loop, name = "kms")
        self.fut.result()
        '''
        run_and_get(self.tellRole())
        

    async def tellRole(self):
        await self.player.send("you are the "+self.role)

    async def doRole(self):
        result = await tellRole()
        return result

    def getEmojis(self,num):
        emojis = self.emojis
        print(emojis)
        return dict(filter(lambda x: x[0] in list(range(1,num+1)),emojis.items()))

    async def getReaction(self,message,num,emojiNum):
        this_message = await self.player.send(message)
        emoji_map = self.getEmojis(emojiNum)
        emojis = list(emoji_map.values())
        for emoji in emojis:
            print(emoji)
            await this_message.add_reaction(emoji)
        #reaction = await bot.wait_for_reaction(emoji=emojis,message=message)
        while True:
            print(this_message.reactions)
            this_message = await self.player.fetch_message(this_message.id)
            reaction = list(filter(lambda x: x.count > 1,this_message.reactions))
            if len(reaction) > num-1:
                
                print("done!")
                print(reaction[0])
                break
        output = list(map(lambda x: list(emoji_map.keys())[(list(emoji_map.values()).index(x.emoji))],reaction))
        return output #list(emoji_map.keys())[(list(emoji_map.values()).index(reaction[0].emoji))] 

class werewolf(base):
    def __init__(self,bot,player,players,roles):
        self.loneWerewolf = True
        '''
        for i in range(0,len(roles)-3):
            if roles[i] == "werewolf" and players[i] != player:
                self.partner = players[i]
                loneWerewolf = False
                break
        '''
        print(roles)
        super().__init__(bot,player,"werewolf",players,roles)
        

    async def tellRole(self):
        if self.loneWerewolf:
            await self.player.send("you are the lone werewolf")
        else:
            await self.player.send("you are a werewolf")

    async def doRole(self):
        if self.loneWerewolf:
            #emojis = [
            x = await self.getReaction("please choose a card from the centre to view",1,3)    
            
            await self.player.send("the card at this position is"+self.roles[-3:][x-1])
        else:
            await self.player.send("the other werewolf is: "+self.partner)

class seer(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"seer",players,roles)

    async def doRole(self):
        x = await self.getReaction("look at another players card :one: or look at a card from the centre :two:?",1,2)
        if x[0] == 1:
            message = "choose a player to look at the card of:"
            i = 0
            for player in self.players:
                i+=1
                if player != self.player:
                    message += "\n{0} {1}".format(self.emojis[i],player)
            num = await self.getReaction(message,1,len(self.players)-1)
            await self.player.send("this player is a "+self.roles[i-1])
        else:
            x = await self.getReaction("please choose 2 cards to look at from the centre",2,3)
            await self.player.send("{0}:{1}".format(x[0],self.roles[-3:][x[0]-1]))
            await self.player.send("{0}:{1}".format(x[1],self.roles[-3:][x[1]-1]))
            print(self.roles)
            '''
            this_message = await self.player.send("please choose 2 cards to look at from the centre")
            emoji_map = self.getEmojis(3)
            emojis = list(emoji_map.values())
            for emoji in emojis:
                print(emoji)
                await this_message.add_reaction(emoji)
            #reaction = await bot.wait_for_reaction(emoji=emojis,message=message)
            while True:
                print(this_message.reactions)
                this_message = await self.player.fetch_message(this_message.id)
                reaction = list(filter(lambda x: x.count > 1,this_message.reactions))
                if len(reaction) >1:
                    print("done!")
                    print(reaction[0])
                    break
            
            thing1 = list(emoji_map.keys())[(list(emoji_map.values()).index(reaction[0].emoji))]
            thing2 = list(emoji_map.keys())[(list(emoji_map.values()).index(reaction[1].emoji))]
            print(self.roles)
            await self.player.send("{0}:{1}".format(thing1,self.roles[-3:][thing1-1]))
            await self.player.send("{0}:{1}".format(thing2,self.roles[-3:][thing2-1]))
            '''
class robber(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"robber",players,roles)
    async def doRole(self):
        message = "please choose a person to steal the card of"
        
        for player in self.players:
            i+=1
            if player != self.player:
                message += "\n{0} {1}".format(self.emojis[i],player)
        x = self.getReaction(message,1,len(self.players)-1)
        await self.player.send("you are now the "+self.roles[x[1]-1])
        x.append(self.players.index(self.player)+1)
        return x

class troublemaker(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"troublemaker",players,roles)

    async def doRole(self):
        message = "please choose two cards to swap from the list of players below"
        
        for player in self.players:
            i+=1
            if player != self.player:
                message += "\n{0} {1}".format(self.emojis[i],player)
        x = await self.getReaction(message,2,len(self.players)-1)
        return x

class drunk(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"drunk",players,roles)

    async def doRole(self):
        message = "please select a card in the middle to swap with your own"
        i=0
        for player in self.players:
            i+=1
            if player != self.player:
                message += "\n{0} {1}".format(self.emojis[i],player)
        x = await self.getReaction(message,2,len(self.players)-1)
        return x

class insomniac(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"insomniac",players,roles)

    async def doRole(self,new_role):
        await self.player.send("you have woken up as the "+new_role)

class villager(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"villager",players,roles)

    async def doRole(base):
        await self.player.send("you have slept a long relaxing sleep and wake up refreshed and ready for the day")

class tanner(base):
    def __init__(self,bot,player,players,roles):
        super().__init__(bot,player,"tanner",players,roles)

    async def doRole(base):
        await self.player.send("you have slept a long relaxing sleep and wake up refreshed and ready for the day")
    #def werewolf(num):
bot.add_cog(Main(bot))
#client.run(TOKEN)
bot.run(TOKEN)        
        
