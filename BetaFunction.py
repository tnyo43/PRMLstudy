"""
ベータ分布の表示
2つの超パラメータa, bを変更できる
"""

import sys
from numpy import array
from math import gamma

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow
from SliderLabel import SliderLabel


def p(a, b, x=[0, 1, 100]):
    """
    ベータ分布の関数
    a, b：ベータ分布の超パラメータ
    x：[min, max, num]
    """
    Beta = lambda t : gamma(a+b)/gamma(a)/gamma(b) *t**(a-1)*(1-t)**(b-1)

    min_, max_, num = x
    xs = [1/num*(0.5+(max_-min_)*x+min_) for x in range(num)]
    ys = [Beta(x) for x in xs]

    return xs, ys


class BetaFunctionGraph(MyQWidget):

    NAME = "Beta Distribution"
    
    def __init__(self):
        super().__init__("Beta Distribution")

        self.initUI()
        self.beta = 0

    def initUI(self):      

        self.a, self.b = 3, 3

        self.slA = SliderLabel(self, func=self.changeValueA, tag="a=")
        self.slA.setGeometry(20, 0, 250, 30)
        self.slB = SliderLabel(self, func=self.changeValueB, tag="b=")
        self.slB.setGeometry(20, 30, 250, 30)

        self.graph = GraphWindow(self)
        self.graph.setGeometry(0, 0, 600, 600)
        self.graph.show()
        self.graph.setXRange(0, 1)
        self.graph.setYRange(0, 4)

        self.setGeometry(700, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()

    def changeValue(self):
        xs, ys = p(self.a, self.b)
        self.graph.clear()
        self.graph.setValue(xs, ys)
        self.graph.show()

    def changeValueA(self, value):
        self.a = value/10+0.1
        self.changeValue()
        return str('%02.1f' % self.a)

    def changeValueB(self, value):
        self.b = value/10+0.1
        self.changeValue()
        return str('%02.1f' % self.b)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    beta = BetaFunctionGraph()
    sys.exit(app.exec_())