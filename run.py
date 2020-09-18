from telethon import TelegramClient, events, custom, functions, types
import asyncio
from data import location_pattern, report_pattern, cw_id, hero_pattern, Parse_hero, July_id, PasrseLocationMessage, get_total_stats, get_stats, comms_id, chat_id, bot_id
import db_services
import json
import time


api_id = 1267461
api_hash = '168acb04f099beb551aff4069d029320'
bot_token = '1288140554:AAFRTkLNEjBYnANATCDeAgxPDkyTwS_6u2Y'

#local variables
locations_dic= {}
bot = TelegramClient('Last StarLight Bot',api_id, api_hash)

@bot.on(events.NewMessage(pattern=location_pattern, forwards=True))
async def Handle_New_location(event):    
    print('loc')
    temp = PasrseLocationMessage(event.message.text)
    print(temp)
    info =db_services.get_loc(temp[0]) 
    print(info)
    if info== None:
        db_services.new_loc(temp[0].strip('*'), temp[1])
        await event.reply('Codigo guardado\nMuchas gracias por tu aporte')
    else:
        await event.reply('Ya ese codigo lo teniamos\nMuchas gracias por tu aporte')

@bot.on(events.NewMessage(pattern=report_pattern, forwards=True))
async def Handler_reports(event):
    a = event.message.fwd_from
    if  a.from_id== cw_id:
        mensg = event.message.text.split("\n")
        if (int)(mensg[3].split(" ")[1]) > 0 or '🔥Exp' not in event.message.text:
            await event.reply("Este reporte es invalido, No es de las batallas de la alianza o no participaste en la batalla")
        else:
            stats = mensg[0].split(" ")
            if stats[1].find('⚔:') ==-1:
                stats[0] = stats[0] + " " + stats[1]
                stats.pop(1)
            guildst = stats[0]
            guild = guildst[2:5]
            name = stats[0][6:]
            temp = stats[1].find("(")
            if(temp == -1):
                atk = (int)(stats[1][2:])
            else:
                atk = (int)(stats[1][2:temp])
            temp = stats[2].find("(")
            if temp == -1:
                defe = (int)(stats[2][2:])
            else:
                defe = (int)(stats[2][2:temp])
            lvl = (int)(stats[4])
            db_services.insert_report([name, guild, atk, defe, lvl] ,event.message.from_id)
            await event.reply('Report Aceptado')
    else:
        await event.reply("reporte invalido")


@bot.on(events.NewMessage(pattern=hero_pattern, incoming=True, forwards=True))
async def Handler_hero(event):
    a = event.message.fwd_from
    if  a.from_id== cw_id:
        ident = event.message.from_id
        info = Parse_hero(event.message.text)
        if info[1] in db_services.gulds:
            if db_services.try_get_hero(ident) != None:
                db_services.update_hero(info, ident)
            else:
                db_services.new_hero(info, ident)
            await event.reply('Perfil actualizado')
        else: 
            await event.reply('Usted no pertenece a los guilds de la alianza')

@bot.on(events.NewMessage(pattern='/get_hero', incoming=True))
async def Handler_Get_hero(event):
    temp = db_services.try_get_hero(event.message.from_id)
    if temp != None:
        hero = temp[1] + ' Guild: ' + temp[2]+'\n⚔️: ' + (str)(temp[3]) + ' 🛡' + (str)(temp[4]) + '  Level: ' + (str)(temp[5])
        await event.reply(hero)
    else:
        await event.reply('No tenemos su perfil en nuestros datos, por favor enviame tu /hero')


@bot.on(events.NewMessage(pattern='/get_total_stats',from_users=comms_id))
async def handle_request(event):
    reports = db_services.get_all_reports()
    rtemp = get_total_stats(reports)
    await event.reply(rtemp)

@bot.on(events.NewMessage(pattern='/get_stats_from', from_users=comms_id))
async def Handle_guild_stats(event):
    guild = event.message.text.split(' ')[1]
    guild = guild.upper()
    if guild not in db_services.gulds:
        await event.reply('Invalid Guild')
    else:
        reports = db_services.get_reports(guild)
        temp = get_stats(reports, guild)
        await event.reply(temp)


@bot.on(events.NewMessage(pattern='/myid'))
async def my_id(event):    
    temp = (str)(event.message.from_id)
    await event.reply(temp)

@bot.on(events.NewMessage(pattern='/get_locations'))
async def get_location_handler(event):   
    ruins = ''
    headq = ''
    mines = ''
    glory = ''
    temp = db_services.get_all_loc()
    for var in temp:
        if 'Ruins' in var[0]:
            ruins += var[0] + ' - '+ var[1] + '\n'
        elif 'Mine' in var[0]:
            mines += var[0] + ' - '+ var[1] + '\n'
        elif ('Tower' in var[0] and var[0]!= 'Fuzzy Tower') or 'Fort' in var[0] or 'Outpost' in var[0]:
            glory += var[0] + ' - '+ var[1] + '\n'
        else:
            headq += var[0] + ' - '+ var[1] + '\n'
    string = '**Ruins:**\n' + ruins + '\n**Mines:**\n' + mines + '\n**Glory:**\n'+ glory + '\n**HeadQuarters**:\n' + headq
    await event.reply(string)

@bot.on(events.NewMessage(from_users=July_id, pattern='/clear_locs'))
async def filter_location_handler(event):  
    temp = db_services.get_all_loc()
    for var in temp:
        if var[0] not in event.message.text:
            db_services.clear_loc(var[0])
    await event.reply('Locationn Updated')

@bot.on(events.NewMessage(pattern='/restart', from_users=July_id))
async def handle_restart(event):
    db_services.clear()
    await event.reply('DB Reports Clear')

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Hi!')
    raise events.StopPropagation

@bot.on(events.NewMessage(incoming=True, pattern='/add_guild', from_users=July_id))
async def handle_add_guild(event):
    guildname = event.message.text.split(' ')
    db_services.addguild(guildname[1], event.message.chat_id)
    await event.reply('guild added')
    await bot.send_message('Pastaper')

@bot.on(events.NewMessage(incoming=True, pattern='/send_one', from_users=comms_id))
async def handle_send_message(event):
    ids = db_services.getchat(event.message.text.split(' ')[1])
    temp = await bot.get_entity(ids)
    reply = await event.get_reply_message()
    await bot.send_message(temp, reply.message)

    
@bot.on(events.NewMessage(incoming=True, pattern='/send_all',from_users=comms_id))
async def handle_sendall_message(event):
    ids = db_services.get_all_chats()
    reply = await event.get_reply_message()
    for idss in ids:
        temp = await bot.get_entity(idss[1])
        await bot.send_message(temp, reply.text)
        await event.reply('mensage sended to ' + idss[0])
        time.sleep(1)


@bot.on(events.NewMessage(incoming=True, pattern='/send_to',from_users=comms_id))
async def handle_sendto_message(event):
    guilds = event.message.text.split(' ')
    ids = db_services.get_all_chats()
    reply = await event.get_reply_message()
    for idss in ids:
        if(idss[0] in guilds):
            temp = await bot.get_entity(idss[1])
            await bot.send_message(temp, reply.text)
            await event.reply('mensage sended to ' + idss[0])
            time.sleep(1)

@bot.on(events.NewMessage(incoming=True, pattern='/send_pin_to',from_users=comms_id))
async def handle_send_pin_order_message(event):
    guilds = event.message.text.split(' ')
    ids = db_services.get_all_chats()
    reply = await event.get_reply_message()
    for idss in ids:
        if(idss[0] in guilds):
            temp = await bot.get_entity(idss[1])
            msg = await bot.send_message(temp, reply.text)
            await event.reply('mensage sended to ' + idss[0])
            time.sleep(1)
            await bot.pin_message(temp, msg)

@bot.on(events.NewMessage(incoming=True, pattern='/send_ord',from_users=comms_id))
async def handle_send_order_message(event):
    ids = db_services.get_all_chats()
    reply = await event.get_reply_message()
    for idss in ids:
        temp = await bot.get_entity(idss[1])
        msg = await bot.send_message(temp, reply.text)
        await event.reply('mensage sended to' + idss[0])
        time.sleep(1)
        await bot.pin_message(temp, msg)


@bot.on(events.NewMessage(pattern='/help', from_users=comms_id))
async def handle_menu(event):
    menu = 'comandos hasta ahora en el bot\nPara todos:\n/myid Devuelve id\n\nPara los lideres\n/get_locations\n\n/send_one (guild) on reply envia mensajeq se esta respondiendo al guild\n\n/send_to (guilds) on reply envia mensaje q se esta respondiendo a los guilds especificados separados por espacios\n\n/send_all on reply  envia mensajeq se esta respondiendo a todos\n\n/send_pin_to (guilds) on reply envia mensajeq se esta respondiendo a los guilds especificados separados por espacios y pinea el mensaje\n\n/send_ord on reply  envia mensajeq se esta respondiendo a todos y lo pinnea\n\n/get_total_stats devuelve los stats de todos los guilds y el total\n\n/get_stats_from (guild) devuelve los stats del guild solicitado'
    await event.reply(menu)
   

bot.start(bot_token=bot_token)
print(time.asctime())


bot.run_until_disconnected()