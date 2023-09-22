import os
import discord
from dotenv import load_dotenv

from Bot_Functions import translate 
from Bot_Functions import places
from Bot_Functions import weather
from Bot_Functions import ttt


load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True


class DevPSUBot(discord.Client):
    async def on_ready(self):
        print("logged on")
        self.units = 'imperial'
        self.unitList = ['imperial', 'standard', 'metric']
    
    async def on_message(self, message):
        print(f"message found: {message.content} from {message.author} in {message.channel}")
        # print(f"mentions: {message.mentions}")
        if message.author == client.user:
            return
        if "hello" in message.content.lower():
            print(f"command recognized: hello")
            await message.channel.send("hello!")
        if client.user in message.mentions:
            print("bot mentioned")
            await message.channel.send(f"I was mentioned by {message.author}!")
        if message.content == "react":
            print("react command recognized")
            await message.add_reaction('👍')
            await message.add_reaction('😈')
        


        #translate.
        if 'translate' in message.content.lower():
            message_list = message.content.split()
            i = 1
            msg = ''

            if 'to' in message.content:
                while message_list[i] != 'to':
                    msg += message_list[i]
                    i += 1
                
                lang = message_list[i + 1]

                await message.channel.send(translate.translator_func(msg,lang))

            else:
                while i < len(message_list):
                    msg += message_list[i +1]
                    i += 1

                await message.channel.send(translate.translator_func(msg))

        #places
        if 'find' in message.content.lower():
            message_list = message.content.lower().split()

            index = message_list.index('find')
            search_string = ''
            index += 1
            while message_list[index] != 'near' and message_list[index] != 'in':
                search_string = search_string + message_list[index]
                index +=1

            if message_list[index] == 'near':
                preference = 'distance'
            preference = 'popularity'
            index += 1

            location = ''
            while index < len(message_list):
                if index != len(message_list) -1:
                    location += message_list[index] + ' '
                else:
                    location += message_list[index]
                index += 1
            await message.channel.send(places.find_places_nearby(location, search_string, preference))


        #set units to:
        if 'set units to' in message.content.lower():
            new_unit = message.content.lower()[12:].strip()

            if new_unit not in self.unitList:
                await message.channel.send('Invalid units, please use one of the units below: \n' + 'imperial \n'+ 'standard \n'+ 'metric')
            elif new_unit == self.units:
                await message.channel.send('Units are already set to ' + self.units)

            else:
                self.units = new_unit
                await message.channel.send('Units are changed to ' + self.units)

            

        #show-units:
        if message.content.lower() == 'show units':
            await message.channel.send('Units are set to: ' + self.units)
        #weather 
        if 'temperature' in message.content.lower() or 'weather' in message.content.lower():

            msgList = message.content.lower().split()

            if len(msgList) == 1:
                location = 'me'

            else:
                location = ''
                i = 2
                while i < len(msgList):
                    location += msgList[i]
                    i += 1

            await message.channel.send(weather.find_weather(location, self.units))

        #game
        if "ttt" in message.content.lower():
            self.state = "ttti"
            self.player_1 = message.author
            await message.channel.send(f'player one is {self.player_1}')
            await message.channel.send(f'please mention player 2')
        if self.state == 'ttti' and message.author == self.player_1 and len(message.mentions) == 1:
            self.state = 'ttt1'
            self.player_2 = message.mentions
            await message.channel.send(f'player 2 is {self.player_2}')
            await message.channel.send(f'use the numpad for input:\n```7 | 8 | 9\n--+---+--\n4 | 5 | 6\n--+---+--\n1 | 2 | 3\n```')
            await message.channel.send(f'{self.player_1}`s turn')
            self.game = ttt()

        if message.content() in {'1','2','3','4','5','6','7','8','9'} and self.state in {'ttt1', 'ttt2'} and message.author in {self.player_1, self.player_2}:
            status = self.game.update_board(message.content, self.state)
            if status == -1: await message.channel.send(f'invalid ttt position')
            elif status == 0:
                await message.channel.send(format_board(self.game.board))
                if self.state == 'ttt1':
                    self.state = 'ttt2'
                    await message.channel.send(f'{self.player_2}`s turn')
                else:
                    self.state = 'ttt1'
                    await message.channel.send(f'{self.player_1}`s turn')
            if status == 1:
                await message.channel.send(format_board(self.game.board))
                await message.channel.send(f'player {self.state[3]} wins!')
                self.state = 'message'
            if status == 2:
                await message.channel.send(format_board(self.game.board))
                await message.channel.send(f'stalemate')
                self.state = 'message'

    #async def on_typing(self, channel, user, when):
        #print(f"{user} is typing in {channel} at {when}")
        #await channel.send(f"I see you typing, {user}")


client = DevPSUBot(intents=intents)
client.run(token)