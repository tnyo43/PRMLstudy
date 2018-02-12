
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SliderLabel(QWidget):

    def __init__(self, parent=None, func=None, tag=""):
        super(SliderLabel, self).__init__(parent)
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(0, 0, 190, 30)
        self.sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setGeometry(200, 0, 80, 30)

        self.changeValueFunction = func
        self.value=0
        self.tag = tag

    def changeValue(self, value):
        if self.changeValueFunction:
            self.value = self.changeValueFunction(value)
        else:
            self.value = value

        self.label.setText(self.tag + self.value)

    def setValue(self, value):
        self.sld.setValue(value)