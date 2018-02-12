"""
3次元のディリクレ分布の表示
"""

import sys
import numpy as np
from math import gamma

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow, GraphWindow3D
from SliderLabel import SliderLabel
import pyqtgraph.opengl as gl


corners = np.array([[0, 0], [1, 0], [0, 1]]) #2次平面の三角形の頂点
N = 100 #一辺に表示する点の最大数
ys = np.linspace(0, corners[2,1], num=int(N*corners[2,1])) #y軸
amplitude = 10
offset = 5

def p(alphas):
    """
    ディリクレ分布の確率密度関数
    """
    r = gamma(sum(alphas))/np.prod([gamma(a) for a in alphas])
    def Dirichlet(x, y):
        z = 1-x-y
        vs = list(map(lambda xa : xa[0]**(xa[1]-1), zip([x,y,z], alphas)))
        return np.prod(vs)*r

    data = []

    Y = corners[2][1]
    for y in ys:
        Xmin = 0
        Xmax = 1-y
        xs = np.linspace(Xmin, Xmax, num=int(N*(Xmax-Xmin)))
        for x in xs:
            pD = Dirichlet(x, y)
            data.append([amplitude*x-offset, amplitude*y-offset, pD/amplitude])
    return np.array(data)

class DirichletDistributionGraph(MyQWidget):

    NAME = "Dirichlet Distribution"

    def __init__(self):
        super().__init__("Dirichlet Distribution")

        self.initUI()
        self.beta = 0

    def initUI(self):

        self.a0, self.a1, self.a2 = 1, 1, 1

        self.slA0 = SliderLabel(self, func=self.changeValueA0, tag="a0=")
        self.slA0.setGeometry(20, 0, 250, 30)
        self.slA1 = SliderLabel(self, func=self.changeValueA1, tag="a1=")
        self.slA1.setGeometry(20, 30, 250, 30)
        self.slA2 = SliderLabel(self, func=self.changeValueA2, tag="a2=")
        self.slA2.setGeometry(20, 60, 250, 30)

        self.setGeometry(70, 300, 280, 90)
        self.setWindowTitle('Dirichlet Distribution')
        self.show()
        self.graph = GraphWindow3D(self, title="hoge")
        points = np.array([[x[0]*amplitude-offset, x[1]*amplitude-offset, 0*amplitude] for x in corners])
        self.graph.setPoints(points)
        self.graph.show()

        self.changeValue()

    def changeValue(self):
        self.graph.clear()
        data = p([self.a0, self.a1, self.a2])

        self.graph.setValue(data)

    def changeValueA0(self, value):
        self.a0 = value/10 + 0.1
        self.changeValue()
        return str('%02.1f' % self.a0)
    def changeValueA1(self, value):
        self.a1 = value/10 + 0.1
        self.changeValue()
        return str('%02.1f' % self.a1)
    def changeValueA2(self, value):
        self.a2 = value/10 + 0.1
        self.changeValue()
        return str('%02.1f' % self.a2)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    beta = DirichletDistributionGraph()
    sys.exit(app.exec_())