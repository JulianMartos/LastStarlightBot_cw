from telethon import TelegramClient, events, custom, functions, types
import asyncio
from data import location_pattern
import json



#local variables
locations_dic= {}

def PasrseLocationMessage(msg):
    temp = msg.split(' ')
    if "Mine" in msg or "Ruins" in msg:
        return [temp[4] + " " + temp[5] + " " + temp[6].split('\n')[0], temp[-1]]
    else:
        return [temp[4] + " " + temp[5].split('\n')[0], temp[-1]]

bot = TelegramClient('Last StarLight Bot',api_id, api_hash)

@bot.on(events.NewMessage(pattern=location_pattern))
async def Handle_New_location(event):    
    temp = PasrseLocationMessage(event.message.text)
    print(temp)
    if temp[0] not in locations_dic:
        locations_dic[temp[0]] = temp[1]
        await event.reply("Locacion Salvada. Gracias por tu aporte")
        with open('data.json', 'w') as fp:
            print("here")
            json.dump(locations_dic, fp)
        print(locations_dic)

    else:
        await event.reply("ya esa la teniamos.")
    #await event.delete()


@bot.on(events.NewMessage(pattern='/myid'))
async def my_id(event):    
    temp = (str)(event.message.from_id)
    await event.reply(temp)

@bot.on(events.NewMessage(pattern='/get'))
async def get_location_handler(event):   
    temp = "" 
    for loc in locations_dic:
        temp = temp + loc + " " + locations_dic[loc] + "\n"
    print(temp)
    await event.reply(temp)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hi!')
    raise events.StopPropagation

bot.start(bot_token=bot_token)
with open('data.json', 'r') as fp:
    locations_dic = json.load(fp)
print("empeze")
bot.run_until_disconnected()
