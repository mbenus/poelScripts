#!/usr/bin/env python3

import redis
import pymysql.cursors


#####################################
# Read miners from redis
# Copy miners to mysql
#####################################

# Connect to redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
miners = r.keys("monero:workers:*")

# Connect to mysql
connection = pymysql.connect(host='localhost',
                             user='MYSQL_USER',
                             password='MYSQL_PASSWORD',
                             db='moneropoel',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
                             

sql = "INSERT INTO `miners` (`address`) VALUES (%s)"
for miner in miners:
    address = miner.split("monero:workers:")[1]
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (address))
            connection.commit()
    except pymysql.err.IntegrityError:
        # er zit een unique constraint op kolom 'address'
        print('Address already in dbase "{}"'.format(address))
    #finally:

connection.close()