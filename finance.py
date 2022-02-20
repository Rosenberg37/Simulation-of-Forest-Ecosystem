import numpy as np
from config import *
from solution1 import CT_now, V_now

def carbon(CT):
    delta = []
    for i in range(1, len(CT)):
        delta.append(CT[i] - CT[i - 1])
    price = params['Pc'] * delta
    npv = 0
    ceof = (1 + params['p']) ** params['TPL']
    mo = (1 + params['p']) ** (0.5 * params['TPL'])
    for p in price:
        npv += p / mo
        mo *= ceof
    return npv

def timber(V, X):   # X:方案，二维数组，（coh, t）， V：数量，二维数组，（coh,  t）
    PVt = []
    COL, T = np.array(X).shape[0], np.array(X).shape[1]
    for t in range(T):
        HV = 0
        for co in range(COL):
            for prod in range(params['prod_cnt']):
                HV += V[co][t] * params['cohort'][co]['area'] * params['cohort'][ co] ['prod'][prod] * \
                      X[co][t] * (params['price'][prod] - params['Lc'])
        PVt.append(HV)
    npv = 0
    ceof = (1 + params['p']) ** params['TPL']
    mo = (1 + params['p']) ** (0.5 * params['TPL'])
    for p in PVt:
        npv += p / mo
        mo *= ceof


def finance(x):
   X  = np.array(x).reshape(params['cohort_cnt'], params['TPL'])
   ret = carbon(CT_now) + timber(V_now, X)
   return ret


if __name__ == "__main__":
    CT = range(100)
    print(carbon(CT))

