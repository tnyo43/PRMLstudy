"""
ノンパラメトリック法の勉強

ヒストグラム法の密度推定、カーネル密度推定、K近傍法の密度推定を行う
"""

import sys
import numpy as np
from math import gamma
from scipy import integrate, special

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow
from SliderLabel import SliderLabel


m0 = 0.25
s0 = 0.01
r0 = 0.65
m1 = 0.8
s1 = 0.01
r1 = 0.35

def sampleDistribution():
    """
    サンプルデータの確率密度関数
    """
    NUM = 100
    xs = [x/NUM for x in range(NUM+1)]

    def p(x, m, s, r):
        return r / (2*np.pi*s)**0.5 * np.exp(-(x-m)**2/2/s)

    ps = [p(x, m0, s0, r0) + p(x, m1, s1, r1) for x in xs]
    return xs, ps

def sampleData(num = 50):
    """
    上の分布を使って{{num}}個のデータを作る
    """
    xs = []

    for i in range(50):
        r = np.random.rand()
        m, s = 0, 0
        if r < r0:
            m, s = m0, s0
        else:
            m, s = m1, s1

        while True:
            x = np.random.normal(m,np.sqrt(s))
            if 0 < x < 1:
                xs.append(x)
                break
    return xs

def KernelDensity(data, h):
    """
    カーネル密度推定法でxsの分布を推定する

    入力dataとパラメータhに対して[0, 1]のxの大きさを求める
    """
    N = len(data)
    NUM = 100
    xs = [x/NUM for x in range(NUM+1)]

    def p(x):
        gauss = lambda v : 1/(2*np.pi*h**2)**0.5 * np.exp(-((x-v)/(h))**2/2)
        ps = [gauss(d)/N for d in data]
        return sum(ps)

    ps = [p(x) for x in xs]
    return xs, ps

def KNear(data, K):
    """
    K近傍法でxsの分布を推定する

    上のカーネル密度推定法のhの幅をxからデータを{{K}}個含む範囲に広げる
    """
    N = len(data)
    data = np.array(data)
    NUM = 100
    xs = [x/NUM for x in range(NUM+1)]

    def p(x):
        diffs = np.sort(abs(data-x))
        h = diffs[K-1]

        gauss = lambda v : 1/(2*np.pi*h**2)**0.5 * np.exp(-((x-v)/(h))**2/2)
        ps = [gauss(d)/N for d in data]
        return sum(ps)

    ps = [p(x) for x in xs]
    return xs, ps

class NonParametricGraph(MyQWidget):

    NAME = "Non Parametric Method"
    def __init__(self):
        super().__init__("Non Parametric Method")

        self.initUI()

    def initUI(self):

        self.xs, self.ps = sampleDistribution()
        self.Delta = 1/25
        self.h = 0
        self.K = 10
        self.data = sampleData()

        self.graphHist = GraphWindow(self, title="Sample Data")
        self.graphHist.setGeometry(0, 0, 600, 600)
        self.graphHist.setXRange(0, 1)
        self.graphHist.setYRange(0, 5)
        self.graphHist.show()

        self.graphKernelDensity = GraphWindow(self, title="Kernel Density Estimation")
        self.graphKernelDensity.setGeometry(600, 0, 600, 600)
        self.graphKernelDensity.setXRange(0, 1)
        self.graphKernelDensity.setYRange(0, 5)
        self.graphKernelDensity.show()

        self.graphKNear = GraphWindow(self, title="K nearest neighbor method")
        self.graphKNear.setGeometry(300, 300, 600, 600)
        self.graphKNear.setXRange(0, 1)
        self.graphKNear.setYRange(0, 5)
        self.graphKNear.show()

        self.slDelta = SliderLabel(self, func=self.changeValueDelta, tag="Δ=")
        self.slDelta.setGeometry(20, 0, 250, 30)
        self.slH = SliderLabel(self, func=self.changeValueH, tag="h=")
        self.slH.setGeometry(20, 30, 250, 30)
        self.slK = SliderLabel(self, func=self.changeValueK, tag="K=")
        self.slK.setGeometry(20, 60, 250, 30)

        self.show()
        self.changeValue()

    def changeValue(self):
        self.changeValueDelta(50)
        self.changeValueH(50)
        self.changeValueK(50)

    def changeValueDelta(self, value):
        self.Delta = 2**(value/99*7-7)

        self.graphHist.clear()
        self.graphHist.setHistgram(self.data, range_=(0, 1), bins=int(1/self.Delta), brush=(255, 0, 0, 80))
        self.graphHist.setValue(self.xs, self.ps, color='b')
        return str('%02.2f' % self.Delta)

    def changeValueH(self, value):
        self.h = 2**(value/99*7-7)

        xs, psKernel = KernelDensity(self.data, self.h)
        self.graphKernelDensity.clear()
        self.graphKernelDensity.setValue(xs, psKernel, color='r')
        self.graphKernelDensity.setValue(self.xs, self.ps, color='b')
        return str('%02.2f' % self.h)

    def changeValueK(self, value):
        self.K = int(value/99*49)+1

        xs, psKnear = KNear(self.data, self.K)
        self.graphKNear.clear()
        self.graphKNear.setValue(xs, psKnear, color='r')
        self.graphKNear.setValue(self.xs, self.ps, color='b')
        return str(self.K)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = NonParametricGraph()
    sys.exit(app.exec_())