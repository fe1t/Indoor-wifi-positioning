#!/usr/bin/python
# - * - encoding: utf-8 - * -

from iwscanner import IWScanner
from cell import Cell
import pymysql, pymysql.cursors, time
from calibration import Calibration

def do_scan():
    iw = IWScanner()
    c = Calibration()
    for cell in iw.do_scan():
        c.insert(x, y, cell.essid, cell.bssid, cell.rssi, cell.quality[0], cell.quality[1])


x, y = raw_input("Enter position x, y: ").split(",")
for i in range(5):
    do_scan()
