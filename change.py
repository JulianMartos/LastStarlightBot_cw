import sqlite3
import json
import db_services

locations_dic = {}

with open('data.json', 'r') as fp:
    locations_dic = json.load(fp)


temp = "" 
for loc in locations_dic:
    a = locations_dic[loc]
    db_services.new_loc(loc.strip('*'), locations_dic[loc])
print(temp)
