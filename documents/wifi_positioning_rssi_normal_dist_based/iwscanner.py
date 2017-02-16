import subprocess
import re
import struct
from cell import Cell

class IWScanner(object):

    def __init__(self, interface="wlan0"):
        self.interface = interface

    def do_scan(self):
        proc = subprocess.Popen("iwlist {} scan".format(self.interface), shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        if "wlan0     Scan completed :" not in output[0]:
            raise "scan failed"

        output = map(lambda x: x.lstrip(" ").rstrip("\n").rstrip(" "), output)[1:-1]
        return self._do_parse('\n'.join(output))

    def _do_parse(self, raw_text):
        top_stack = -1
        cells = []
        lines = raw_text.split('\n')
        for line in lines:
            m = re.match("Cell [0-9]+ - Address: (.*)", line)
            if m:
                cells.append(Cell(m.group(1)))
                top_stack += 1
            m = re.match("Channel:(.*)", line)
            if m: cells[top_stack].channel = int(m.group(1))
            m = re.match("ESSID:\"(.*)\"", line)
            if m: cells[top_stack].essid = m.group(1)
            m = re.match("Quality=([0-9]+)/([0-9]+)  Signal level=(.*) dBm", line)
            if m:
                cells[top_stack].quality = m.group(1), m.group(2)
                cells[top_stack].rssi = int(m.group(3))




        return cells

