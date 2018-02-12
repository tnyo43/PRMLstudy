
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import pyqtgraph.opengl as gl

class GraphWindow(QMainWindow):

    def __init__(self, parent = None, title=""):
        super(GraphWindow, self).__init__(parent)
        pw = pg.PlotWidget()
        self.setCentralWidget(pw)
        self.setWindowTitle(title)
        
        self.p1 = pw.plotItem
        self.p2 = pw.plotItem
        self.p3 = pw.plotItem

        self.p3.setXRange(-1, 1)
        self.p3.setYRange(-1, 1)

    def clear(self):
        self.p1.clear()
        self.p2.clear()
        self.p3.clear()

    def setValue(self, x, y, color="w", line=True):
        """
        x, yの組を通る線をプロット
        """
        if line: #plot lines
            self.p1.addItem(pg.PlotCurveItem(x = x,  y = y, pen=pg.mkPen(color=color)))
        else: # plot points
            self.p1.addItem(pg.ScatterPlotItem(x = x,  y = y, pen=pg.mkPen(color=color)))

    def setYRange(self, min_, max_):
        for p in [self.p1, self.p2, self.p3]:
            p.setYRange(min_, max_)

    def setXRange(self, min_, max_):
        for p in [self.p1, self.p2, self.p3]:
            p.setXRange(min_, max_)

    def setHistgram(self, values, range_, bins=40, brush=(0, 0, 255, 80)):
        y,x = np.histogram(values, bins=bins, range=range_)
        L = range_[1] - range_[0]
        hist = pg.PlotCurveItem(x, y/len(values)/L*bins, stepMode=True, fillLevel=0, brush=brush)
        self.p2.addItem(hist)

    def setValuePolar(self, thetas, rs=None, color="w"):
        """
        θの列を単位円の円周上にプロット
        rsがNoneでないとき、極座標の線をプロット
        """
        if rs:
            x = [value[0]*np.cos(value[1]) for value in zip(rs, thetas)]
            y = [value[0]*np.sin(value[1]) for value in zip(rs, thetas)]
            self.p3.addItem(pg.PlotCurveItem(x=x, y=y, pen=pg.mkPen(color=color)))
        else:
            x = [np.cos(value) for value in thetas]
            y = [np.sin(value) for value in thetas]
            self.p3.addItem(pg.ScatterPlotItem(x=x, y=y))

    def setHistPolar(self, values, bins=200):
        """
        円状にヒストグラムを表示する
        valuesは[0, 2π)
        """
        num = len(values)
        y_, x_ = np.histogram(values, bins=bins, range=(0, 2*np.pi))
        x_, y_ = list(map(list, [x_, y_]))
        x_.append(x_[0])
        y_.append(y_[0])
        x,y = np.array([v[1]*np.cos(v[0]) for v in zip(x_, y_)]), np.array([v[1]*np.sin(v[0]) for v in zip(x_, y_)])

        L = 2*np.pi
        hist = pg.PlotCurveItem(np.array(x)/len(values)/L*bins, np.array(y)/len(values)/L*bins, fillLevel=0, brush=(0, 0, 255, 80))
        self.p1.addItem(hist)
        


class GraphWindow3D(QMainWindow):
    
    def __init__(self, parent = None, title=""):
        super(GraphWindow3D, self).__init__(parent)

        self.graph = gl.GLViewWidget()
        self.xgrid = gl.GLGridItem()
        self.ygrid = gl.GLGridItem()
        self.zgrid = gl.GLGridItem()
        self.graph.addItem(self.xgrid)
        self.graph.addItem(self.ygrid)
        self.graph.addItem(self.zgrid)
        self.items = []
        self.points = []

    def setPoints(self, points, color=(1,0,0,1), size=0.3):
        """
        常に表示しておきたい点を設定
        """
        self.points.append(gl.GLScatterPlotItem(pos=points, size=size, color=color, pxMode=False))

    def _plotPoints(self):
        for point in self.points:
            self.graph.addItem(point)

    def clear(self):
        for item in self.items:
            self.graph.removeItem(item)
        self.graph.show()
        self._plotPoints()

        self.items = []

    def setValue(self, values):
        """
        valuesは3次元データ
        """
        color = (1,1,1,1)
        size = 0.1
        scttrPlt = gl.GLScatterPlotItem(pos=values, size=size, color=color, pxMode=False)

        self.graph.addItem(scttrPlt)
        self.graph.show()

        self.items.append(scttrPlt)

    def show(self):
        self.graph.show()
