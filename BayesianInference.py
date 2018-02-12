"""
m勝n敗したときの勝率のベイズ推定
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

def p(beta, win, lose, x=[0, 1, 100]):
    """
    ベイズ推定で事後分布を表示
    β（超パラメータ）、勝ち数、負け数から事後分布を算出する
    """
    N = win + lose
    _p = lambda x : gamma(N + 2*beta)/gamma(win+beta)/gamma(lose+beta)*x**(win+beta-1)*(1-x)**(lose+beta-1)
    min_, max_, num = x
    xs = [1/num*(max_-min_)*x+min_ for x in range(num+1)]
    ys = [_p(x) for x in xs]

    return xs, ys

class BayesianInferenceGraph(MyQWidget):

    NAME = "Bayesian Inference"
    def __init__(self):
        super().__init__("Bayesian Inference")

        self.initUI()

    def initUI(self):

        self.graph = GraphWindow(self)
        self.graph.setGeometry(0, 0, 600, 600)
        self.graph.setXRange(0, 1)
        self.graph.setYRange(0, 12)

        self.sl_beta = SliderLabel(self, func=self.changeValueBeta, tag="beta=")
        self.sl_beta.setGeometry(20, 40, 1000, 30)

        self.sl_win = SliderLabel(self, func=self.changeValueWin, tag="win :")
        self.sl_win.setGeometry(20, 70, 1000, 30)

        self.sl_lose = SliderLabel(self, func=self.changeValueLose, tag="lose :")
        self.sl_lose.setGeometry(20, 100, 1000, 30)

        self.label_mode = QLabel(self)
        self.label_mode.setGeometry(200, 128, 80, 30)
        self.label_mode.setStyleSheet('color: red')

        self.label_rate = QLabel(self)
        self.label_rate.setGeometry(200, 158, 80, 30)
        self.label_rate.setStyleSheet('color: blue')

        self.setGeometry(700, 300, 280, 200)
        self.setWindowTitle('BayesianInference')
        self.show()

        self.beta = 2
        self.win = 0
        self.lose = 0
        self.ValueChanged()

    def ValueChanged(self):
        xs, ys = p(self.beta, self.win, self.lose)
        mode = xs[ys.index(max(ys))]
        rate = 0.5
        if self.win+self.lose is not 0:
            rate = self.win/(self.win+self.lose)

        self.graph.clear()
        self.graph.setValue(xs, ys)
        self.graph.setValue([mode, mode], [0, 100], 'r')
        self.graph.setValue([rate, rate], [0, 100], 'b')
        self.graph.show()
        self.label_mode.setText("mode:" + str('%01.2f' % mode))
        self.label_rate.setText("rate:" + str('%01.2f' % rate))

    def changeValueBeta(self, value):
        self.beta = value/11+1
        self.ValueChanged()
        return str('%02.1f' % self.beta)

    def changeValueWin(self, value):
        self.win = int(value/99*30)
        self.ValueChanged()
        return str(self.win)

    def changeValueLose(self, value):
        self.lose = int(value/99*30)
        self.ValueChanged()
        return str(self.lose)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = BayesianInferenceGraph()
    sys.exit(app.exec_())