#!/usr/bin/env python3

import requests
import json
import pymysql.cursors
from datetime import datetime

baseurl = 'https://api.cryptonator.com/api/ticker/'
currencies = ['XMR-EUR', 'XMR-GBP', 'XMR-USD', 'XMR-BTC']

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='MYSQL_USER',
                             password='MYSQL_PASSWORD',
                             db='moneropoel',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

# The query to execute
sql = "INSERT INTO `moneroprices` (`base`, `target`, `price`, `changed`, `volume`, `timestamp`) VALUES (%s, %s, %s, %s, %s, %s)"

for cur in currencies:
    url = baseurl + cur;
    r = requests.get(url)
    if (r.ok):
        p = Payload(r.text)
        timestamp = datetime.utcfromtimestamp(int(p.timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        changed = float(p.ticker['change'])
        price = float(p.ticker['price'])
        volume = 0 if p.ticker['volume'] == "" else float(p.ticker['volume'])
        base = p.ticker['base']
        target = p.ticker['target']
        
        with connection.cursor() as cursor:
            cursor.execute(sql, (base, target, price, changed, volume, timestamp))
            connection.commit()

# close mysql connection
connection.close()