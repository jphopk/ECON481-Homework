import numpy as np
import scipy as sp

def github() -> str:
    return "https://github.com/jphopk/ECON481-Homework/blob/main/ECON481-HW2-JustinHopkins.py"


def simulate_data(seed: int = 481) -> tuple:
    rng = np.random.default_rng(seed=seed)
    x1 = rng.normal(0, 2**(0.5), 1000)
    x2 = rng.normal(0, 2**(0.5), 1000)
    x3 = rng.normal(0, 2**(0.5), 1000)
    X = np.c_[x1, x2, x3]
    e1 = rng.normal(0, 1, 1000)
    y = 5 + 3*x1 + 2*x2 + 6*x3 + e1
    return (y, X)

def estimate_mle(y: np.array, X: np.array) -> np.array:
    def neg_ll(B: np.array, y: np.array, X: np.array) -> float:
        newX = np.c_[np.ones(1000), X]
        #prob = np.log((1/np.sqrt(2*np.pi)))+np.log(np.exp(-0.5*(y-B@newX.T)**2)), original function before simplifying and taking out constants
        prob = (-0.5*(y-B@newX.T)**2)
        return -np.sum(prob)
    
    result = sp.optimize.minimize(
                fun = neg_ll,
                x0 = [0,0,0,0],
                args = (y, X)
            )
    return result.x

def estimate_ols(y: np.array, X: np.array) -> np.array:
    def sumSqResid(B: np.array, y: np.array, X: np.array) -> float:
        newX = np.c_[np.ones(1000), X]
        sqResid = (y-B@newX.T)**2
        return np.sum(sqResid)
    
    newResult = sp.optimize.minimize(
                fun = sumSqResid,
                x0 = [0,0,0,0],
                args = (y, X)
            )
    return newResult.x

