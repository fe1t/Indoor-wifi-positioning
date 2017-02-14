#!/usr/bin/python
# - * - coding: utf-8 - * -

from calibration import Calibration
from calibrate_point_manager import CalibratePointManager
from cell import Cell
from iwscanner import IWScanner
from fractions import Fraction
import decimal
import numpy as np
import sys

# np.mean(array)
# np.std(array)

Kd = 4
def euclidean_distance(cj, sk):
    # assert(len(cj) == len(sk) and type(cj) == type(sk) == list)
    return np.sqrt(reduce(lambda x, y: x + y,  \
            map(lambda x, y:
        (decimal.Decimal(x[0]) - decimal.Decimal(y[0])) ** decimal.Decimal(2)
        , cj, sk)))

def improved_euclidean_distance(cj, sk):
    #dev_k = decimal.Decimal(sk[2])
    #dev_ik = decimal.Decimal(cj[2])
    #sum_dev = dev_k + dev_ik
    #return np.sqrt(reduce(lambda a, b: a + b, \
    #        map(lambda a, b: ((np.abs(decimal.Decimal(a[1]) - decimal.Decimal(b[1])) \
    #            + sum_dev) ** decimal.Decimal(2)), cj, sk)))
    return (reduce(lambda a, b: a + b, \
            map(lambda a, b: ((np.abs(a[1] - b[1]) \
                + a[2] + b[2]) ** decimal.Decimal(2)), cj, sk))).sqrt()

def gaussian_dist(cj, sk):
    x = map(lambda a: a[1], sk)
    sigma = map(lambda a: (a[2]) , cj)
    if 0 in sigma:
        return 0
    mu = map(lambda a: a[1], cj)
#     if not reduce(lambda x, y: x and y,
            #map(lambda x: x != 0, sigma),
            #True):
    print "sigma: ", sigma
    print "x: ", x
    P = map(lambda a, b, c: \
            decimal.Decimal(np.e) ** -((a - c) ** 2 \
                / decimal.Decimal(2* (b ** 2))) \
                / decimal.Decimal(b * decimal.Decimal(2.0 * np.pi).sqrt()) \
                , x, sigma, mu)
    return decimal.Decimal(reduce(lambda a, b: a * b, P))


decimal.getcontext().prec = 128
# gmpy2.get_context().precision= 256

def calculate(s):
    cp = CalibratePointManager()
    cpoints = cp.get_cpoints()
    xy = cp.xy
    d = []
    p = []
    # sort_func = lambda x: x.bssid
    # sorted(cpoints, key=sort_func)
    # sorted(s, key=sort_func)
    for cpoint in cpoints:
        si = s

        # place Pavg instead of -80
        # cpoint = filter(lambda x: x.rssi > np.mean(global_avg), cpoint)
        si = filter(lambda x: x.rssi > np.mean(global_avg), si)
        bssid_list = set(map(lambda x: x.bssid, cpoint))
        bssid_list = bssid_list.intersection(set(map(lambda x: x.bssid, si)))


        c = filter(lambda x: x.bssid in bssid_list, cpoint)
        si = filter(lambda x: x.bssid in bssid_list, si)
        sort_func = lambda x: x.bssid
        c = sorted(c, key=sort_func)
        si = sorted(si, key=sort_func)
        c = map(lambda x: (x.bssid, decimal.Decimal(x.rssi), decimal.Decimal(x.std)), c)
        si = map(lambda x: (x.bssid, decimal.Decimal(x.rssi), decimal.Decimal(x.std)), si)
        assert(len(si) == len(c))
        # print bssid_list
        if len(bssid_list) != 0:
            d.append((improved_euclidean_distance(c, si), len(d)))
            p.append((gaussian_dist(c, si), len(p)))
        else:
            d.append((-1, len(d)))
            p.append((-1, len(p)))
    d = filter(lambda x: x[0] != -1, sorted(d))[:Kd]
    p = filter(lambda x: x[0] != 0 and x[0] != -1, sorted(p))[-Kd:]
    # เอา w = d -> ไปเข้าสูตร weight ได้เลย (x1, y1)
    # เอา w = p -> ไปเข้าสูตรเหมือน d ได้ออกมาเป็น (x2, y2)
    # def get_xy(d, p):
    def get_xy(d, p):
        ex = gx  = decimal.Decimal(0.0)
        ey = gy = decimal.Decimal(0.0)
        sum_d = decimal.Decimal(0.0)
        sum_p = decimal.Decimal(0.0)
        for i in range(len(d)):
            if d[i][0] == -1: continue
            sum_d += decimal.Decimal(1.0)/decimal.Decimal(d[i][0])
            ex += ((xy[d[i][1]][0]) / decimal.Decimal(d[i][0]))
            ey += ((xy[d[i][1]][1]) / decimal.Decimal(d[i][0]))

        for i in range(len(p)):
            if p[i][0] == -1: continue

            w = decimal.Decimal(np.log2(float(p[i][0])))
            sum_p += (w)
            gx += (xy[i][0]) * w
            gy += (xy[i][1]) * w
        # print sum_d
        if sum_d == 0: ox, oy = 0, 0

        ex = ex / sum_d
        ey = ey / sum_d

        gx = gx / sum_p # <<<< here
        gy = gy / sum_p

        return ex, ey, gx, gy

    x1, y1, x2, y2 = get_xy(d, p)
    print "(x1,y1): (%d, %d)" % (x1,y1)
    print "(x2,y2): (%d, %d)" % (x2,y2)


    D1 = np.var(map(lambda x: (x[0]),  d))
    print "p: ", p
    D2 = np.var(map(lambda x: (x[0]), p))
    sum_D = D1 + D2

    print "D1: {} D2: {}".format(D1, D2)
    x = x1 * decimal.Decimal(D1 / sum_D) + x2 * decimal.Decimal(D2 / sum_D)
    y = y1 * decimal.Decimal(D1 / sum_D) + y2 * decimal.Decimal(D2 / sum_D)




    return x , y




# x, y = raw_input("Current position (x, y): ").replace(" ", "").split(",")


# obs[i].bssid, obs[i].rssi (avg), obs[i].std
obs = list()
cells_hash = { }
global_avg = list()

for i in range(10):
    for result in IWScanner().do_scan():
        if result.bssid not in cells_hash:
            cells_hash[result.bssid] = [result]
        else:
            cells_hash[result.bssid].append(result)

for bssid, arr in cells_hash.iteritems():
    rssi_arr = list()
    for item in arr:
        rssi_arr.append(item.rssi)
    cell = Cell(bssid)
    cell.rssi = np.mean(rssi_arr)
    cell.std = np.std(rssi_arr)
    obs.append(cell)

    global_avg.append(cell.rssi)

print "Your position is about: (%d, %d)" % (calculate(obs))
