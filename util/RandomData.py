
import numpy as np
from numpy.random import rand, normal

def Sine(num=200):
    xs = []
    ys = []

    for i in range(num):
        x = i/num
        y = np.sin(2*np.pi*x)
        xs.append(x)
        ys.append(y)

    return xs, ys

    
def randomSine(num=100, sigma2=0.1, regularIntervals=False):
    """
    y=sin(2πx) ( 0 <= x <= 1) + e
    eは平均0、分散sigma2に従う正規分布による確率変数
    {{num}}個のデータを返す
    regularIntervalsがTrueならxは等間隔、Falseならランダムに作られる
    """
    xs = []
    ys = []

    for i in range(num):
        if regularIntervals:
            x = (i+0.5)/num
        else:
            x = rand()

        e = normal(0, sigma2)
        y = np.sin(2*np.pi*x) + e
        xs.append(x)
        ys.append(y)

    return xs, ys

def Linear(ws, std=0.2):
    """
    y =ws*xs + N(0, std**2)
    """
    x = rand()
    t = sum([w*x**i for i, w in enumerate(ws)])+normal(0, std**2)
    return x, t
    