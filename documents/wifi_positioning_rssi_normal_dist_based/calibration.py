#!/usr/bin/python

from cell import Cell
import pymysql.cursors
import pymysql
import json

class Calibration(Cell):
    def __init__(self):
        self.db =  None
        self.x = None
        self.y = None
        self.std = None
        self.cells = []
        with open("config.json", 'r') as f:
            self.config = json.load(f)


    def insert(self, x, y, essid, bssid ,rssi, q_l, q_t ):
        self.db = pymysql.connect(host=self.config['host'], user=self.config['user'], password=self.config['password'],  db=self.config['db'])
        with self.db.cursor() as cursor:
            sql = "INSERT INTO access_point (X, Y, ESSID, BSSID, RSSI, quality_level, quality_total) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (x, y, essid, bssid ,rssi, q_l, q_t ))
        self.db.commit()
        self.db.close()

    def get(self, x=None, y=None):
        self.db = pymysql.connect(host=self.config['host'], user=self.config['user'], password=self.config['password'],  db=self.config['db'])
        with self.db.cursor() as cursor:
            if x == None or y == None:
                sql = "SELECT * FROM access_point;"
                cursor.execute(sql)
            else:
                sql = "SELECT id, date, x, y, essid, bssid, avg(rssi) as rssi, quality_level, quality_total, STD(rssi) as std FROM access_point where x = %s and y = %s GROUP BY bssid;"
                cursor.execute(sql, (x, y))
            rows = cursor.fetchall()
        for row in rows:
            cell = Cell(row[5])
            cell.essid = row[4]
            cell.rssi = row[6]
            cell.quality = float(row[7]), float(row[8])
            if row[9] != None:
                cell.std= row[9]
            self.cells.append(cell)
        self.db.close()

        return self.cells
