"""
スチューデントのt分布の表示

平均MU、分散SIGMA2の正規分布から得たデータと少数の外れ値データに対して、t分布とガウス分布を比較する。
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

from GaussianDistribution import randn, N

MU = 0
SIGMA2 = 1


MIN, MAX, NUM = -5, 10, 200

def getN(xs):
    """
    データxsに対するガウス分布を求める
    平均muと分散sigma2を返す
    """
    mu = np.mean(xs)
    Ex2 = np.mean([x**2 for x in xs])
    sigma2 = Ex2 - mu**2
    return mu, sigma2

def t(x, mu, lambda_, ny):
    """
    平均mu、精度lambda_、自由度nyのt分布でのxの出現する確率密度を返す
    """
    return gamma(ny/2+1/2)/gamma(ny/2)*(lambda_/np.pi/ny)**0.5*(1+lambda_*(x-mu)**2/ny)**(-ny/2-1/2)

class tDistributionGraph(MyQWidget):

    NAME = "t Distribution"
    
    def __init__(self):
        super().__init__("t Distribution")

        self.initUI()

    def initUI(self):

        self.graphT = GraphWindow(self, title="Student's t Distribution")
        self.graphT.setGeometry(0, 0, 600, 600)
        self.graphT.setXRange(MIN, MAX)
        self.graphT.setYRange(0, 1)

        self.btnData = QPushButton('Add Data',self)
        self.btnData.setGeometry(20, 0, 120, 30)
        self.btnData.clicked.connect(self.clickedAddData)

        self.btnNoiseData = QPushButton('Add Noise Data',self)
        self.btnNoiseData.setGeometry(20, 30, 120, 30)
        self.btnNoiseData.clicked.connect(self.clickedAddNoiseData)

        self.btnReset = QPushButton('Reset Data',self)
        self.btnReset.setGeometry(150, 0, 120, 30)
        self.btnReset.clicked.connect(self.clickedResetData)


        self.slNy = SliderLabel(self, func=self.changeValueNy, tag="ν=")
        self.slNy.setGeometry(20, 60, 1000, 30)
        self.slLambda = SliderLabel(self, func=self.changeValueLambda, tag="λ=")
        self.slLambda.setGeometry(20, 90, 1000, 30)

        self.setGeometry(620, 200, 300, 200)
        self.show()
        self.xs = []
        self.lambda_ = 1
        self.ny = 10

        self.ValueChanged()

    def ValueChanged(self):
        mu, sigma2 = getN(self.xs)

        xs = [1/NUM*(MAX-MIN)*x+MIN for x in range(NUM+1)]
        psGauss = [N(x, mu, sigma2) for x in xs]
        psT = [t(x, mu, self.lambda_, self.ny) for x in xs]

        self.graphT.clear()
        self.graphT.setHistgram(self.xs, range_=(MIN, MAX), bins=50)
        self.graphT.setValue(xs, psGauss, color="y")
        self.graphT.setValue(xs, psT, color="r")
        self.graphT.show()

    def clickedAddData(self):
        x = randn(MU, SIGMA2)
        self.xs.append(x)
        self.ValueChanged()

    def clickedAddNoiseData(self):
        x = np.random.rand()*15-5
        self.xs.append(x)
        self.ValueChanged()

    def clickedResetData(self):
        self.xs = []
        self.ValueChanged()

    def changeValueNy(self, value):
        a = value/99*16-8
        self.ny = 2**a
        self.ValueChanged()
        return str('%03.3f' % self.ny)

    def changeValueLambda(self, value):
        self.lambda_ = value/99*9.9+0.1
        self.ValueChanged()
        return str('%02.2f' % self.lambda_)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = tDistributionGraph()
    sys.exit(app.exec_())