
import numpy as np

def PolynominalBasisFunctions(M, x):
    """
    多項式の基底関数
    """
    return np.array([[x**i for i in range(M+1)]])


def GaussianBasisFunctions(M, x, sigma2=0.04):
    """
    ガウス関数の基底関数
    """
    xs = [1]
    mus = [i/(M-1) for i in range(M)]

    def phi(mu):
        return np.exp(-(x-mu)**2/(2*sigma2))

    xs.extend([phi(mu) for mu in mus])
    return np.array([xs])

def model(x, ws, M, basisFunction=PolynominalBasisFunctions):
    xs = basisFunction(M, x)
    return np.dot(ws, xs.T)[0]
