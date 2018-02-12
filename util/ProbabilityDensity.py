
import numpy as np

def N(x, mu, sigma2):
    """
    平均mu、分散sigma2の正規分布でのxの出現する確率密度を返す
    """
    return 1/(2*np.pi*sigma2)**(0.5)*np.exp(-1/(2*sigma2) * (x-mu)**2)

def Ns(xs, mus, sigma2):
    return np.prod([N(x, mu, sigma2) for x, mu in zip(xs, mus)])

