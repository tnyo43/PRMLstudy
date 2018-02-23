"""
バイアスバリアンス分解の勉強

正規化項のλが大きいほどバリアンスが小さく、小さいほどバイラスが小さくなる
"""

import sys
import numpy as np
from math import gamma

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('../widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow
from SliderLabel import SliderLabel

sys.path.append("../util")
from RandomData import Sine, randomSine
from BasisFunctions import GaussianBasisFunctions, PolynominalBasisFunctions, model
from MaximumLikelihoodEstimation import SumOfSquareError, shinkage

M = 24
NUM = 100

class BiasVarianceTradeoffGraph(MyQWidget):

    NAME = "Bias-Variance Tradeoff"

    def __init__(self):
        super().__init__("Bias-Variance Tradeoff")

        self.initUI()

    def initUI(self):

        self.Lambda = 0
        self.BASISFUNCTION = GaussianBasisFunctions

        self.graph1 = GraphWindow(self, "Variance Graph")
        self.graph1.setGeometry(0, 0, 600, 600)
        self.graph1.setXRange(0, 1)
        self.graph1.setYRange(-1.3, 1.3)
        self.graph2 = GraphWindow(self, "Bias Graph")
        self.graph2.setGeometry(600, 0, 600, 600)
        self.graph2.setXRange(0, 1)
        self.graph2.setYRange(-1.3, 1.3)

        self.sineX, self.sineY = Sine()

        self.data = []
        for i in range(NUM):
            xs, ts = randomSine(num=25,sigma2=0.09,regularIntervals=True)
            self.data.append([xs, ts])

        self.graph1.show()
        self.graph2.show()
        self.plot()

        self.slL = SliderLabel(self, func=self.changeValueLambda, tag="lnλ=")
        self.slL.setGeometry(20, 0, 280, 30)
        self.show()

    def changeValueLambda(self, value):
        l = (value/99*6-3)
        self.Lambda = np.exp(l)
        self.plot()
        return str('%02.1f' % l)

    def plot(self):
        self.graph1.clear()
        self.graph1.setValue(self.sineX, self.sineY, color='b')
        self.graph2.clear()
        self.graph2.setValue(self.sineX, self.sineY, color='b')

        WS = np.zeros([M+1])
        for datum in self.data[:20]:
            xs, ts = datum
            ws = shinkage(xs, ts, M, self.Lambda, basisFunction=self.BASISFUNCTION)
            ys = [model(x, ws, M, basisFunction=self.BASISFUNCTION) for x in self.sineX]
            WS += np.array(ws)
            self.graph1.setValue(self.sineX, ys, color='r')
        for datun in self.data[20:]:
            xs, ts = datum
            ws = shinkage(xs, ts, M, self.Lambda, basisFunction=self.BASISFUNCTION)
            WS += np.array(ws)

        WS /= NUM
        ys = [model(x, WS, M, basisFunction=self.BASISFUNCTION) for x in self.sineX]
        self.graph2.setValue(self.sineX, ys, color='r')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = BiasVarianceTradeoffGraph()
    sys.exit(app.exec_())