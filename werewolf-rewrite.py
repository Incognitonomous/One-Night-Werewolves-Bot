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
                bot.add_cog(Game(bot,self.players))
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
    def __init__(self,bot,players):
        self.bot=bot
        self.players=players
        role_list = ["werewolf","werewolf","seer","toublemaker","drunk","insomniac","villager","villager"]
        self.role_list = role_list
        random.shuffle(self.role_list)
        '''
        coro = self.werewolf(bot,players[0],None)
        self.fut = asyncio.Task(coro, loop = client.loop, name = "kms")
        self.fut.result()
        '''
        werewolf(bot,players[0],None)
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
    def __init__(self,bot,player,role):
        super().__init__()
        self.bot = bot
        self.player = player
        self.role = role
        self.emojis = {1:"<a:one:822414441508896839>",
                       2:"<a:two:822414519938318358>",
                       3:"<a:three:822414601550692362>",
                       4:"<a:four:822414646651781140>",
                       5:"<a:five:822414681473286144>",
                       6:"<a:six:822414750960189450>",
                       7:"<a:seven:822414801291444264>",
                       8:"<a:eight:822414839384768522>",
                       9:"<a:nine:822414904732024852>"}
        '''
        coro = self.doRole()
        self.fut = asyncio.Task(coro, loop = client.loop, name = "kms")
        self.fut.result()
        '''
        run_and_get(self.doRole())
        

    async def tellRole(self):
        await self.player.send("you are the "+role)

    async def doRole(self):
        result = await tellRole()
        return result

    def getEmojis(self,num):
        emojis = self.emojis
        print(emojis)
        return dict(filter(lambda x: x[0] in list(range(1,num+1)),emojis.items()))

    async def getReaction(self,message,num):
        this_message = await self.player.send(message)
        emoji_map = self.getEmojis(num)
        emojis = list(emoji_map.values())
        for emoji in emojis:
            this_message.add_reaction(emoji)
        reaction = await bot.wait_for_reaction(emoji=emojis,message=message)
        return emoji_map.keys()[emoji_map.values().index(reaction)] 

class werewolf(base):
    def __init__(self,bot,player,otherWerewolf):
        self.loneWerewolf = otherWerewolf==None
        self.partner = otherWerewolf
        super().__init__(bot,player,"werewolf")

    async def tellRole(self):
        if self.loneWerewolf:
            await self.player.send("you are the lone werewolf")
        else:
            await self.player.send("you are a werewolf")

    async def doRole(self):
        if self.loneWerewolf:
            #emojis = [
            x = await self.getReaction("please choose a card from the centre to view",3)    

        
                
        
    #def werewolf(num):
bot.add_cog(Main(bot))
#client.run(TOKEN)
bot.run(TOKEN)        
        
