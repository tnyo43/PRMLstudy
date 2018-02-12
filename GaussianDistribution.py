"""
Plot Bayesian inference by GaussianDistribution.
σが既知の状態で未知の平均μを推定する

MU0, SIGMA0_2：μを推定するために定めた任意の変数μ0, σ0^2
Prior graph : μの事前分布。μ0、σ0^2によって決まる
Likelihood graph：観測データxベクトルに対してμの尤度の分布。観測データxとμ0、σ0^2によって決まる
Posterior graph：μの事後分布。事前分布と尤度関数の積に比例する（計算上、そうなるのは確認した）。観測データxとμ0、σ0^2によって決まる。
"""


import sys
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.append('widgets')
from MyQWidget import MyQWidget
from GraphWindow import GraphWindow
from SliderLabel import SliderLabel

sys.path.append('util')
from ProbabilityDensity import N

MU = 0 #unknown value
SIGMA2 = 4 #known value

MU0 = 0
SIGMA0_2 = 2

min_, max_, num = -1, 1, 100

def randn(mu=0, sigma2=1.0):
    """
    平均mu、分散sigma2の正規分布のランダムな値を返す
    """
    return np.random.randn()*np.sqrt(sigma2)+mu


def pL(xs, mu_=[min_, max_, num]): #尤度関数
    """
    正規化している訳ではなく、最大を1としている
    """
    min_, max_, num = mu_
    mus = [1/num*(max_-min_)*x+min_ for x in range(num+1)]

    def p(mu):
        ps = list(map(lambda x : N(x, mu, SIGMA2), xs))
        return np.prod(ps)
    likelihood = np.array([p(mu) for mu in mus])
    if xs:
        likelihood /= likelihood.max()
    else:
        pass
    return mus, likelihood


def pPrior(mu_=[min_, max_, num], mu0=MU0, sigma0_2=SIGMA0_2): #事前分布
    """
    平均MU, 分散SIGMA2の標準分布でのmusの分布

    mu_ : [最小値, 最大値, 分割数]
    """
    min_, max_, num = mu_
    mus = [1/num*(max_-min_)*x+min_ for x in range(num+1)]

    return mus, [N(mu, mu0, sigma0_2) for mu in mus]

def pPosterior(xs, mu_=[min_, max_, num], mu0=MU0, sigma0_2=SIGMA0_2): #事後分布
    Num = len(xs)
    muML = np.average(xs)
    muN = SIGMA2/(Num*sigma0_2 + SIGMA2)*mu0 + Num*sigma0_2/(Num*sigma0_2+SIGMA2)*muML
    sigmaN_2 = 1/(1/sigma0_2 + Num/SIGMA2)

    min_, max_, num = mu_
    mus = [1/num*(max_-min_)*x+min_ for x in range(num+1)]
    ps = [N(x=mu, mu=muN, sigma2=sigmaN_2) for mu in mus]
    return mus, ps

class GaussianDistributionGraph(MyQWidget):

    NAME = "Gaussian Distribution"
    
    def __init__(self):
        super().__init__("Gaussian Distribution")

        self.initUI()

    def initUI(self):

        self.graphPrior = GraphWindow(self, title="Prior graph")
        self.graphPrior.setGeometry(0, 0, 600, 600)
        self.graphPrior.setYRange(0, 5)

        self.graphLikelihood = GraphWindow(self, title="Likelihood graph")
        self.graphLikelihood.setGeometry(0, 0, 600, 600)
        self.graphLikelihood.setYRange(0, 1)

        self.graphPosterior = GraphWindow(self, title="Posterior graph")
        self.graphPosterior.setGeometry(0, 0, 600, 600)
        self.graphPosterior.setYRange(0, 5)
        self.graphPosterior.setXRange(min_, max_)


        self.sl_sigma0_2 = SliderLabel(self, func=self.changeValueSigma0_2, tag="σ0^2=")
        self.sl_sigma0_2.setGeometry(20, 40, 1000, 30)

        self.sl_mu0 = SliderLabel(self, func=self.changeValueMu0, tag="mu0=")
        self.sl_mu0.setGeometry(20, 70, 1000, 30)

        self.btn_data = QPushButton('Add Data',self)
        self.btn_data.setGeometry(20, 0, 120, 30)
        self.btn_data.clicked.connect(self.clickedAddData)

        self.btn_reset = QPushButton('Reset Data',self)
        self.btn_reset.setGeometry(140, 0, 120, 30)
        self.btn_reset.clicked.connect(self.clickedResetData)


        self.labelNum = QLabel(self)
        self.labelNum.setGeometry(20, 100, 200, 30)

        labelMU = QLabel(self)
        labelMU.setGeometry(300, 100, 200, 30)
        labelMU.setText("Actual MU : " + str('%01.4f' % MU))
        labelMU.setStyleSheet('color: red')

        self.labelAverage = QLabel(self)
        self.labelAverage.setGeometry(20, 130, 300, 30)
        self.labelAverage.setStyleSheet('color: orange')

        self.labelPostMode = QLabel(self)
        self.labelPostMode.setGeometry(20, 160, 300, 30)
        self.labelPostMode.setStyleSheet('color: blue')

        self.labelAveDiff = QLabel(self)
        self.labelAveDiff.setGeometry(300, 130, 300, 30)
        self.labelAveDiff.setStyleSheet('color: orange')

        self.labelPMDiff = QLabel(self)
        self.labelPMDiff.setGeometry(300, 160, 300, 30)
        self.labelPMDiff.setStyleSheet('color: blue')

        self.setGeometry(700, 300, 560, 200)
        self.setWindowTitle('GaussianDistribution')

        self.show()

        self.sigma0_2 = SIGMA0_2
        self.mu0 = MU0

        self.xs = []
        self.sl_sigma0_2.setValue(10)
        self.sl_mu0.setValue(50)
        self.ValueChanged()

    def ValueChanged(self):
        mus, psPrior = pPrior(mu0=self.mu0, sigma0_2=self.sigma0_2)
        self.graphPrior.clear()
        self.graphPrior.setValue(mus, psPrior)
        self.graphPrior.show()

        mus, psLikelihood = pL(self.xs)
        self.graphLikelihood.clear()
        self.graphLikelihood.setValue(mus, psLikelihood)
        self.graphLikelihood.show()

        mus, psPosterior = pPosterior(self.xs, mu0=self.mu0, sigma0_2=self.sigma0_2) #理論上の事後関数
        self.graphPosterior.clear()
        self.graphPosterior.setValue(mus, psPosterior)
        self.graphPosterior.setValue([MU, MU], [0, 10], 'r')
        #事後分後∝事前分布*尤度関数から求めた事後分布。理論上の事後分布と完全に一致して草
        """
        psPrior, psLikelihood = list(map(np.array, [psPrior, psLikelihood]))
        psPosteriorCalc = psPrior* psLikelihood #計算して出した事後分布
        psPosteriorCalc *= max(psPosterior) / max(psPosteriorCalc)
        self.graphPosterior.setValue(mus, psPosteriorCalc)
        """
        self.graphPosterior.show()

        mode = mus[psPosterior.index(max(psPosterior))] #確率密度が最大の点
        self.graphPosterior.setValue([mode, mode], [0, 10], 'b')
        self.labelPostMode.setText("Posterior Distribution Mode : " + str('%01.4f' % mode))
        self.labelPMDiff.setText("diff : " + str('%01.4f' % abs(mode-MU)))
        if self.xs:
            average = sum(self.xs)/len(self.xs)
            self.labelAverage.setText("Data simple average : " + str('%01.4f' % average))
            self.labelAveDiff.setText("diff : " + str('%01.4f' % abs(average-MU)))
            self.graphPosterior.setValue([average, average], [0, 10], 'y')
        else:
            self.labelAverage.setText("Data simple average : -")
            self.labelAveDiff.setText("diff : -")

        self.labelNum.setText("Data Num : " + str(len(self.xs)))

    def changeValueSigma0_2(self, value):
        self.sigma0_2 = value/99*4.99+0.01
        self.ValueChanged()
        return str('%02.2f' % self.sigma0_2)

    def changeValueMu0(self, value):
        self.mu0 = (value/99-0.5)*2
        self.ValueChanged()
        return str('%02.1f' % self.mu0)

    def clickedAddData(self):
        x = randn(mu=MU, sigma2=SIGMA2)
        self.xs.append(x)
        self.ValueChanged()

    def clickedResetData(self):
        self.xs = []
        self.ValueChanged()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    graph = GaussianDistributionGraph()
    sys.exit(app.exec_())