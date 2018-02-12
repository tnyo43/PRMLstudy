
from PyQt5.QtWidgets import *

class MyQWidget(QWidget):

    def __init__(self, name):
        super().__init__()
        self.name = name

class MyQPushButton(QPushButton):

    def __init__(self, parent, title, number, graph=None, textarea=None, text=None):
        """
        DistributionViewer専用のボタン

        グラフ表示用にgraphを設定。graphはMyQWidget
        """

        super().__init__(title, parent)
        self.number = number    
        self.graph = graph
        self.clicked.connect(lambda : self.graph())