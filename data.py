cw_id = 408101137
July_id = 745224074
zorbeto_id = 730529057
mauro_id = 646830635
chat_id = 330078789
bot_id = 925876891
comms_id = [July_id, zorbeto_id, mauro_id ]
location_pattern = "You found hidden"
report_pattern = '(?si).*Your result on the battlefield*'
hero_pattern = '(?si).*Expertise*'
import db_services



def Parse_hero(hero):
    lines = hero.split('\n')
    name = lines[0]
    guild = lines[0][4:7]
    level = (int)(lines[1].split(' ')[1])
    stats = lines[2].split(' ')
    atk = (int)(stats[1])
    defs = (int)(stats[3])
    return [name, guild, atk, defs, level]

def get_total_stats(reports):
    battle_reports_dic = {"SIR":[(0,0),(0,0),(0,0),0],"KGM":[(0,0),(0,0),(0,0),0],"OSO":[(0,0),(0,0),(0,0),0],"7NT":[(0,0),(0,0),(0,0),0], "TOG":[(0,0),(0,0),(0,0),0], "TRB":[(0,0),(0,0),(0,0),0], "OOH":[(0,0),(0,0),(0,0),0], "RFR":[(0,0),(0,0),(0,0),0], "total":[(0,0),(0,0),(0,0),0]}
    for row in reports:
        temp = battle_reports_dic[row[2]]
        lvl=(int)(row[5])
        if lvl >= 20 and lvl < 40:
            ga = temp[0][0] +(int)(row[3])
            gb = temp[0][1] +(int)(row[4])
            temp[0] = (ga,gb)
            gat = battle_reports_dic["total"][0][0]+(int)(row[3])
            gbt = battle_reports_dic["total"][0][1]+(int)(row[4])
            battle_reports_dic["total"][0] = (gat, gbt)
        if lvl >= 40 and lvl < 60:
            ga = temp[1][0] +(int)(row[3])
            gb = temp[1][1] +(int)(row[4])
            temp[1] = (ga,gb)
            gat = battle_reports_dic["total"][1][0]+(int)(row[3])
            gbt = battle_reports_dic["total"][1][1]+(int)(row[4])
            battle_reports_dic["total"][1] = (gat, gbt)
        if lvl > 60:
            ga = temp[2][0] +(int)(row[3])
            gb = temp[2][1] +(int)(row[4])
            temp[2] = (ga,gb)
            gat = battle_reports_dic["total"][2][0]+(int)(row[3])
            gbt = battle_reports_dic["total"][2][1]+(int)(row[4])
            battle_reports_dic["total"][2] = (gat, gbt)
        temp[3] += 1
        string = ''
    for guild in battle_reports_dic:
        string += (str)(guild+ '\n')
        for item in battle_reports_dic[guild]:
            if(item != battle_reports_dic[guild][3]):
                string += (str)(item[0]) + ' ' + (str)(item[1]) +'\n' 
            else:
                string += (str)(item) + '\n\n'    
    return string

def PasrseLocationMessage(msg):
    temp = msg.split(' ')
    if "Mine" in msg or "Ruins" in msg:
        return [temp[4] + " " + temp[5] + " " + temp[6].split('\n')[0], temp[-1]]
    else:
        return [temp[4] + " " + temp[5].split('\n')[0], temp[-1]]

def get_stats(reports, guild):
    battle_reports_dic = {"SIR":[(0,0),(0,0),(0,0),0],"KGM":[(0,0),(0,0),(0,0),0],"OSO":[(0,0),(0,0),(0,0),0],"7NT":[(0,0),(0,0),(0,0),0], "TOG":[(0,0),(0,0),(0,0),0], "TRB":[(0,0),(0,0),(0,0),0], "OOH":[(0,0),(0,0),(0,0),0], "RFR":[(0,0),(0,0),(0,0),0]}

    string = guild + '\n'    
    for row in reports:
        temp = battle_reports_dic[row[2]]
        lvl=(int)(row[5])
        if lvl >= 20 and lvl < 40:
            ga = temp[0][0] +(int)(row[3])
            gb = temp[0][1] +(int)(row[4])
            temp[0] = (ga,gb)
        if lvl >= 40 and lvl < 60:
            ga = temp[1][0] +(int)(row[3])
            gb = temp[1][1] +(int)(row[4])
            temp[1] = (ga,gb)
        if lvl > 60:
            ga = temp[2][0] +(int)(row[3])
            gb = temp[2][1] +(int)(row[4])
            temp[2] = (ga,gb)
        temp[3] += 1
    for item in battle_reports_dic[guild]:
        if(item != battle_reports_dic[guild][3]):
            string += (str)(item[0]) + ' - ' + (str)(item[1]) +'\n' 
        else:
            string += (str)(item) + '\n\n'    
    return string