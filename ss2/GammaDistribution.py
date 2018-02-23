"""
ガンマ分布の表示

2つの超パラメータa,bを変化させたときのガンマ分布を表示する
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

def Gam(a, b, l=[0.01, 2, 100]):
    def p(lambda_):
        return 1/gamma(a)*b**a*lambda_**(a-1)*np.exp(-b*lambda_)

    min_, max_, num = l
    lambdas = [1/num*(max_-min_)*x+min_ for x in range(num+1)]
    ps = [p(l) for l in lambdas]
    return lambdas, ps

def EGam(a, b):
    return a/b

def varGam(a, b):
    return a/b**2

class GammaDistributionGraph(MYQWidget):

    NAME = "Gamma DistributionGraph"
    
    def __init__(self):
        super().__init__("Gamma DistributionGraph")

        self.initUI()

    def initUI(self):

        self.graphGamma = GraphWindow(self, title="Gamma Distribution")
        self.graphGamma.setGeometry(0, 0, 600, 600)
        self.graphGamma.setYRange(0, 2)

        self.sl_a = SliderLabel(self, func=self.ValueChangedA, tag="a=")
        self.sl_a.setGeometry(20, 40, 300, 30)

        self.sl_b = SliderLabel(self, func=self.ValueChangedB, tag="b=")
        self.sl_b.setGeometry(20, 70, 300, 30)

        self.a = 1
        self.b = 1
        self.show()
        self.ValueChanged()

    def ValueChanged(self):
        lambdas, ps = Gam(self.a, self.b)
        self.graphGamma.clear()
        self.graphGamma.setValue(lambdas, ps)
        self.graphGamma.show()
        pass

    def ValueChangedA(self, value):
        self.a = value/99*9.9+0.1
        self.ValueChanged()
        return str('%02.2f' % self.a)

    def ValueChangedB(self, value):
        self.b = value/99*9.9+0.1
        self.ValueChanged()
        return str('%02.2f' % self.b)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = GammaDistributionGraph()
    sys.exit(app.exec_())