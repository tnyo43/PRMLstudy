"""
周期関数のvon Mises distributionの表示

ボタンを押すたびにデータが{{NUM}}個ずつ生成される
"""

import sys
import numpy as np
from math import gamma
from scipy import integrate, special

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('../widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow
from SliderLabel import SliderLabel

from GaussianDistribution import randn

MU = np.pi/3 #生成するデータの平均
NUM = 50 #一回ボタンをおすごとに生成するデータの数

def p(theta0, m, theta_=[0, 2*np.pi, 100]):
    I0m = I0(m)

    def _p(theta):
        return 1/(2*np.pi*I0m)*np.exp(m*np.cos(theta-theta0))

    min_, max_, num = theta_
    thetas = [1/num*(max_-min_)*x+min_ for x in range(num+1)]
    ps = [_p(theta) for theta in thetas]

    return thetas, ps

def thetaMean(thetas):
    """
    角度の分布に対して、その平均の角度θ0を返す
    """

    N = len(thetas)
    if N is 0:
        return 0
    else:
        xs = [np.cos(theta) for theta in thetas]
        ys = [np.sin(theta) for theta in thetas]

    return np.arctan2(sum(ys),sum(xs)) % (2*np.pi)

def I0(m):
    """
    0次の第1種変形ベッセル関数
    
    def i0(x):
        return np.exp(m*np.cos(x))

    return 1/(2*np.pi) * integrate.quad(i0, 0, 2*np.pi)[0]
    でも求まるけど、関数を使うと確実
    """
    return special.iv(0, m)

def A(m):
    I1m = special.iv(1, m) #1次の第1種変形ベッセル関数
    I0m = special.iv(0, m) #0次の第1種変形ベッセル関数
    return I1m/I0m

def AmML(thetas, thetaML):
    """
    mの最尤推定解mMLでの関数Aの値
    すなわち、A_mML(thetaML) = A(mML)
    """
    N = len(thetas)
    coss = [np.cos(theta) for theta in thetas]
    sins = [np.sin(theta) for theta in thetas]

    return (sum(coss)*np.cos(thetaML) + sum(sins)*np.sin(thetaML))/N

def search_mML(thetas, thetaML):
    """
    AmMLの値を求め、それに最も近いmを返す。すなわちmの最尤推定解
    m = [0.05:10] で200分割
    """
    r = AmML(thetas, thetaML)

    mML = 0
    error = 10000
    for i in range(200):
        m = i/20+0.05
        Am = A(m)
        if abs(Am-r) < error:
            mML = m
            error = abs(Am-r)
    return mML


class vonMisesDistributionGraph(MyQWidget):

    NAME = "von Mises Distribution"
    
    def __init__(self):
        super().__init__("von Mises Distribution")

        self.initUI()

    def initUI(self):

        self.m = 5
        self.sigma2 = 1

        self.graphVonMises1 = GraphWindow(self, title=self.name)
        self.graphVonMises1.setGeometry(0, 0, 600, 600)
        self.graphVonMises1.setXRange(-1.3, 1.3)
        self.graphVonMises1.setYRange(-1.3, 1.3)

        self.graphVonMises2 = GraphWindow(self, title="von Mises Distribution")
        self.graphVonMises2.setGeometry(0, 0, 600, 600)
        self.graphVonMises2.setXRange(0, 2*np.pi)
        self.graphVonMises2.setYRange(0, 1.5)

        self.btnData = QPushButton('Add Data',self)
        self.btnData.setGeometry(20, 0, 120, 30)
        self.btnData.clicked.connect(self.clickedAddData)

        self.btnReset = QPushButton('Reset Data',self)
        self.btnReset.setGeometry(150, 0, 120, 30)
        self.btnReset.clicked.connect(self.clickedResetData)

        self.slSigma2 = SliderLabel(self, func=self.changeValueSigma2, tag="σ2=")
        self.slSigma2.setGeometry(20, 30, 300, 30)

        self.label_mML = QLabel(self)
        self.label_mML.setGeometry(300, 30, 80, 30)

        self.xs = []
        for i in range(1000):
            x = randn(MU, self.sigma2)%(2*np.pi)
            self.xs.append(x)


        self.show()
        self.slSigma2.setValue(56)

    def ValueChanged(self):

        thetaML = thetaMean(self.xs)
        mML = search_mML(self.xs, thetaML)
        thetas, ps = p(thetaML, mML) #θの確率密度関数

        self.label_mML.setText("mML=" + str('%02.2f' % mML))

        self.graphVonMises1.clear()
        self.graphVonMises1.setValuePolar(self.xs)
        self.graphVonMises1.setValuePolar(thetas, ps, color='b')
        self.graphVonMises1.setValue([0, 2*np.cos(thetaML)], [0, 2*np.sin(thetaML)], color='y')
        self.graphVonMises1.setValue([0, 2*np.cos(MU)], [0, 2*np.sin(MU)], color='r')
        self.graphVonMises1.setHistPolar(self.xs, bins=40)
        self.graphVonMises1.show()

        self.graphVonMises2.clear()
        self.graphVonMises2.setValue(thetas, ps, color='b')
        self.graphVonMises2.setValue([thetaML,thetaML], [0, 10], color='y')
        self.graphVonMises2.setValue([MU, MU], [0, 10], color='r')
        self.graphVonMises2.setHistgram(self.xs, range_=(0, 2*np.pi), bins=40)
        self.graphVonMises2.show()


    def clickedAddData(self):
        for i in range(NUM):
            x = randn(MU, self.sigma2)%(2*np.pi)
            self.xs.append(x)
        self.xs.append(x)

        self.ValueChanged()

    def clickedResetData(self):
        self.xs = []
        self.ValueChanged()

    def changeValueSigma2(self, value):
        self.sigma2 = 2**(value/99*7-4)
        self.ValueChanged()
        return str('%02.1f' % self.sigma2)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = vonMisesDistributionGraph()
    sys.exit(app.exec_())