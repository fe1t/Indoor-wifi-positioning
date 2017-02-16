
import subprocess
import re
import struct


class Cell(object):


    def __init__(self, bssid=None):
        if bssid:
            bssid = bssid.replace(":", "").decode('hex')
            self._bssid = bssid
        else:
            self._bssid = None
        self.essid = None
        self.rssi = None
        self.std = None
        self.channel = None
        self.quality = None

    @property
    def bssid(self):
        if not self._bssid: return None
        bssid_sep = struct.unpack("<cccccc", self._bssid)
        bssid_raw = map(lambda x: ord(x), bssid_sep)
        return "{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}".format(*bssid_raw)

    @bssid.setter
    def bssid(self, bssid):
        self._bssid = bssid.replace(":", "").decode('hex')

    def __str__(self):
        return '''ESSID: {}
BSSID: {}
Channel: {}
RSSI: {} dBm
Quality: {}
'''.format(self.essid, self.bssid, self.channel, self.rssi, self.quality)


if __name__ == "__main__":
    c = Cell()
    c.bssid = "FF:FF:FF:FF:FF:FF"
    print c.bssid
