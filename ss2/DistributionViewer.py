"""
いろんな分布を見れるプラットフォーム

Viewerを開くためのボタンと説明が書いてある
今度作る
"""

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from BetaFunction import BetaFunctionGraph
from DirichletDistribution import DirichletDistributionGraph
from GaussianDistribution import GaussianDistributionGraph
from tDistribution import tDistributionGraph
from vonMisesDistribution import vonMisesDistributionGraph
from NonParametric import NonParametricGraph
from BayesianInference import BayesianInferenceGraph

sys.path.append('../widgets')
from MyQWidget import MyQPushButton

class DistributionViewer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        Graphs = [
            BetaFunctionGraph,
            DirichletDistributionGraph,
            GaussianDistributionGraph,
            tDistributionGraph,
            vonMisesDistributionGraph,
            NonParametricGraph,
            BayesianInferenceGraph
        ]

        for i, graph in enumerate(Graphs):
            self.graph = graph
            button = MyQPushButton(self, graph.NAME, i, self.graph)
            button.setGeometry(20, 30*i, 180, 30)
        self.show()

        #self.



if __name__ == '__main__':

    app = QApplication(sys.argv)
    viewer = DistributionViewer()
    sys.exit(app.exec_())