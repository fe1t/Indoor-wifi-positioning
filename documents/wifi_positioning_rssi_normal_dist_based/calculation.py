#!/usr/bin/python

from calibration import Calibration
from calibrate_point_manager import CalibratePointManager
from cell import Cell
from iwscanner import IWScanner
from fractions import Fraction
import decimal
import gmpy2

# np.mean(array)
# np.std(array)

def euclidean_distance(cj, sk):
    # assert(len(cj) == len(sk) and type(cj) == type(sk) == list)
    print "cj: ",cj
    print "sk: ", sk
    return gmpy2.sqrt(reduce(lambda x, y: x + y,  \
            map(lambda x, y: (gmpy2.mpfr(x[0]) - gmpy2.mpfr(y[0]))**gmpy2.mpfr(2), cj, sk)))


# decimal.getcontext().prec = 128
gmpy2.get_context().precision= 256

def calculate(s):
    cp = CalibratePointManager()
    cpoints = cp.get_cpoints()
    xy = cp.xy
    d = []
    # sort_func = lambda x: x.bssid
    # sorted(cpoints, key=sort_func)
    # sorted(s, key=sort_func)
    for cpoint in cpoints:
        si = s
        cpoint = filter(lambda x: x.rssi > -65, cpoint)
        si = filter(lambda x: x.rssi > -65, si)
        bssid_list = set(map(lambda x: x.bssid, cpoint))
        bssid_list = bssid_list.intersection(set(map(lambda x: x.bssid, si)))


        c = filter(lambda x: x.bssid in bssid_list, cpoint)
        si = filter(lambda x: x.bssid in bssid_list, si)
        sort_func = lambda x: x.bssid
        c = sorted(c, key=sort_func)
        si = sorted(si, key=sort_func)
        c = map(lambda x: (x.rssi, x.bssid), c)
        si = map(lambda x: (x.rssi, x.bssid), si)
        assert(len(si) == len(c))
        # print bssid_list
        if len(bssid_list) != 0:
            d.append(euclidean_distance(c, si))
        else:
            d.append(-1)
    ox = gmpy2.mpfr(0.0)
    oy = gmpy2.mpfr(0.0)
    sum_d = gmpy2.mpfr(0.0)
    for i in range(len(d)):
        if d[i] == -1: continue
        if d[i] == 0:
            d[i] = 0.0000000000000000001
            print xy[i]
        sum_d += gmpy2.mpfr(1.0)/gmpy2.mpfr(d[i])
        ox += ((xy[i][0]) / gmpy2.mpfr(d[i]))
        oy += ((xy[i][1]) / gmpy2.mpfr(d[i]))
    # print sum_d
    if sum_d == 0: ox, oy = 0, 0
    ox = ox / sum_d
    oy = oy / sum_d
    return ox, oy




    # x = int(0)
    # y = int(0)




    """
        algorithm goes here.
    """
    x, y= 0, 1
    return x, y

# x, y = raw_input("Current position (x, y): ").replace(" ", "").split(",")
print "Your position is about: (%d, %d)" % (calculate(IWScanner().do_scan()))
