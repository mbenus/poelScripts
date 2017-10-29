#!/usr/bin/env python3

import redis
import pymysql.cursors

#####################################
# Read miners from mysql
# Read stats per miner from redis
# Copy stats to mysql
#####################################

# connect to redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='MYSQL_USER',
                             password='MYSQL_PASSWORD',
                             db='moneropoel',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
# The query to execute
sql = "INSERT INTO `minerstats` (`minerId`, `hashes`, `lastshare`, `balance`) VALUES (%s, %s, %s, %s)"
                             
def getMiners():
    """Get miners from mysql"""
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `miners`"
        cursor.execute(sql)
        miners = cursor.fetchall()
    return miners
   
def copyMinerStats(miner):
    """Copy miner statistics to mysql"""
    stat = r.hgetall("monero:workers:" + miner['address'])
    minerid = int(miner['id'])
    hashes = float(stat['hashes'] if 'hashes' in stat else 0)
    lastshare = float(stat['lastShare'] if 'lastShare' in stat else 0)
    balance = stat['balance'] if 'balance' in stat else None
    with connection.cursor() as cursor:
        cursor.execute(sql, (minerid, hashes, lastshare, balance))
        connection.commit()

#####################################
# MAIN 
miners = getMiners()
for miner in miners:
    copyMinerStats(miner)

connection.close()