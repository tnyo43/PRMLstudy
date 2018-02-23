"""
多項式曲線フィッティング

t = sin(2πx) + e （eは正規分布）のデータに沿った曲線を求める
{{M}}次の多項式y(x) = w^T(.)x がtに近くなるような{{M+1}}次元のベクトルwを求める
左のグラフは二乗和誤差を最小にするwを求める
右のグラフは二乗和誤差と正規化項が最小になるwを求める
"""

import sys
import numpy as np
from math import gamma

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow
from SliderLabel import SliderLabel

sys.path.append("util")
from RandomData import Sine, randomSine
from BasisFunctions import PolynominalBasisFunctions, model
from MaximumLikelihoodEstimation import SumOfSquareError, shinkage

def eye(M):
    """
    w0の大きさを無視するために(1,1)の項の値を0にした
    """
    e = np.eye(M)
    e[0][0] = 0
    return e

class CurveFittingGraph(MyQWidget):

    NAME = "Curve Fiting"
    def __init__(self):
        super().__init__("Curve Fiting")

        self.initUI()

    def initUI(self):

        self.M = 1
        self.NUM = 10
        self.Lambda = 0

        self.graph1 = GraphWindow(self)
        self.graph1.setGeometry(0, 0, 600, 600)
        self.graph1.setXRange(0, 1)
        self.graph1.setYRange(-1.3, 1.3)
        self.graph2 = GraphWindow(self)
        self.graph2.setGeometry(600, 0, 600, 600)
        self.graph2.setXRange(0, 1)
        self.graph2.setYRange(-1.3, 1.3)

        self.sineX, self.sineY = Sine()
        self.xs, self.ts = list(map(np.array, randomSine(num=self.NUM,sigma2=0.3, regularIntervals=False)))
        self.graph1.show()
        self.graph2.show()

        self.plot()

        self.slM = SliderLabel(self, func=self.changeValueM, tag="M=")
        self.slM.setGeometry(20, 0, 280, 30)
        self.slN = SliderLabel(self, func=self.changeValueNum, tag="NUM=")
        self.slN.setGeometry(20, 30, 280, 30)
        self.slL = SliderLabel(self, func=self.changeValueLambda, tag="lnλ=")
        self.slL.setGeometry(20, 60, 280, 30)

        self.show()


    def changeValueM(self, value):
        m = int(value/99*24+1)
        if m < self.NUM:
            self.M = m
            self.plot()
        return str(self.M)

    def changeValueNum(self, value):
        n = int(value+2)
        if n > self.M:
            self.NUM = n
            self.xs, self.ts = list(map(np.array, randomSine(num=self.NUM,sigma2=0.3, regularIntervals=False)))
            self.plot()
        return str(self.NUM)

    def changeValueLambda(self, value):
        l = (value/99*30-20)
        self.Lambda = np.exp(l)
        self.plot()
        return str('%02.1f' % l)


    def plot(self):
        self.graph1.clear()
        self.graph1.setValue(self.xs, self.ts, line=False)
        self.graph1.setValue(self.sineX, self.sineY, color='b')
        self.graph2.clear()
        self.graph2.setValue(self.xs, self.ts, line=False)
        self.graph2.setValue(self.sineX, self.sineY, color='b')

        ws1 = SumOfSquareError(self.xs, self.ts, self.M)
        ys = [model(x, ws1, self.M) for x in self.sineX]
        self.graph1.setValue(self.sineX, ys, color='r')
        ws2 = shinkage(self.xs, self.ts, self.M, self.Lambda)
        ys = [model(x, ws2, self.M) for x in self.sineX]
        self.graph2.setValue(self.sineX, ys, color='r')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = CurveFittingGraph()
    sys.exit(app.exec_())