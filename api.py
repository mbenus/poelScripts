from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

import pymysql.cursors
import time

app = Flask(__name__)
api = Api(app)
CORS(app)


def openMysql():
    return pymysql.connect(host='localhost',
                             user='MYSQL_USER',
                             password='MYSQL_PASSWORD',
                             db='moneropoel',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
connection = openMysql()

# IP authorization #############################
admins_ips = ['127.0.0.1']
def isadmin():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    print (ip)
    if (ip not in admins_ips):
        abort(401, message="muhaha")
################################################


parser = reqparse.RequestParser()
parser.add_argument('task')

class Miner(Resource):
    def get(self, minerId):
        isadmin()
        def getData():
            sql = "SELECT id, address, UNIX_TIMESTAMP(created) as created FROM miners WHERE id=%s" 
            with connection.cursor() as cursor:
                cursor.execute(sql, (minerId))
                miner = cursor.fetchone()
                return miner
        try:
            return getData()
        except:
            connection = openMysql()
        return getData()

class Miners(Resource):
    def get(self):
        isadmin()
        
        def getData():
            sql = "SELECT id, address, UNIX_TIMESTAMP(created) as created FROM miners"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                miners = cursor.fetchall()
                return miners
            
        try:
            return getData()
        except:
            connection = openMysql()
        return getData()


class MinerStats(Resource):
    def get(self, minerId):
        isadmin()
        
        def getData():
            to = time.time()
            fr = to - (60 * 60 * 24 * 1) # 3 dagen

            select = "SELECT id, hashes, lastshare, balance, UNIX_TIMESTAMP(created) as created FROM minerstats"
            where = " WHERE minerId=%s AND created >= FROM_UNIXTIME(%s)"
            order = " ORDER BY created asc"
            sql = select + where + order
            with connection.cursor() as cursor:
                cursor.execute(sql, (minerId, fr, to))
                miners = cursor.fetchall()
                return miners
        try:
            return getData()
        except:
            connection = openMysql()
        return getData()

class MoneroPrices(Resource):
    def get(self, target):
        #isadmin()

        def getData():
            to = time.time()
            fr = to - (60 * 60 * 24 * 3) # 3 dagen

            select = "SELECT price as y, UNIX_TIMESTAMP(created) as x FROM moneroprices"
            where = " WHERE target=%s AND timestamp >= FROM_UNIXTIME(%s)"
            order = " ORDER BY x asc"
            sql = select + where + order
            with connection.cursor() as cursor:
                cursor.execute(sql, (target, fr))
                prices = cursor.fetchall()
                return prices

        try:
            return getData()
        except:
            connection = openMysql()
        return getData()

##
## Actually setup the Api resource routing here
##
api.add_resource(Miners, '/api/miners')
api.add_resource(Miner, '/api/miners/<minerId>')
api.add_resource(MinerStats, '/api/miners/<minerId>/stats')
api.add_resource(MoneroPrices, '/api/prices/<target>')


if __name__ == '__main__':
    app.run(debug=True)
