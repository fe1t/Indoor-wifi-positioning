#!/usr/bin/python

import pymysql.cursors
import pymysql
import json
import md5

class CellQuery:
    def __init__(self):
        with open("config.json", 'r') as f:
            self.config = json.load(f)


    def __insert(self, x, y, essid, bssid ,rssi, q_l, q_t ):
        self.db = pymysql.connect(host=self.config['host'], user=self.config['user'], password=self.config['password'],  db=self.config['db'])
        with self.db.cursor() as cursor:
            sql = "INSERT INTO access_point (X, Y, ESSID, BSSID, RSSI, quality_level, quality_total) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (x, y, essid, bssid ,rssi, q_l, q_t ))
        self.db.commit()
        self.db.close()

    def get(self):
        self.db = pymysql.connect(host=self.config['host'], user=self.config['user'], password=self.config['password'],  db=self.config['db'])
        with self.db.cursor() as cursor:
                sql = "SELECT * FROM access_point;"
                cursor.execute(sql)
                rows = cursor.fetchall()
        out = {}
        for row in rows:
            #k = md5.new(row[5]).hexdigest()
            k = row[5]
            if k  not in out:
                out[k] = []
            out[k].append({
                    'bssid': row[5],
                    'essid': row[4],
                    'rssi': row[6],
                    'date': row[1],
                })
        self.db.close()
        return out

if __name__ == "__main__":
    cell = CellQuery()
    for d in cell.get():
        print d['date']
