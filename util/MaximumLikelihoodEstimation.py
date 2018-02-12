
import numpy as np
from BasisFunctions import *

def SumOfSquareError(xs, ts, M, basisFunction=PolynominalBasisFunctions):
    """
    二乗最小誤差を最小にするwsを返す

    xs:観測データのベクトルx
    ts:観測データの値t
    M:基底の次元（バイアスを除く分）
    """
    _Xs = []
    tx = np.zeros([M+1, 1])
    for x, t in zip(xs, ts):
        xn = basisFunction(M, x)
        tx += t*xn.T
        _Xs.append(np.dot(xn.T, xn))
    X = sum(_Xs)
    Xinv = np.linalg.inv(X)
    return np.dot(Xinv, tx).T[0] 

def shinkage(xs, ts, M, Lambda, basisFunction=PolynominalBasisFunctions):
    """
    二乗最小誤差と正規化項の和を最小にするwsを返す
    """
    _Xs = []
    tx = np.zeros([M+1, 1])
    for x, t in zip(xs, ts):
        xn = basisFunction(M, x)
        tx += t*xn.T
        _Xs.append(np.dot(xn.T, xn))
    X = sum(_Xs)
    Xinv = np.linalg.inv(X+Lambda*np.eye(M+1))
    return np.dot(Xinv, tx).T[0] 
