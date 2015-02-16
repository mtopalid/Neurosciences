import numpy as np

Wmin, Wmax = 0.25, 0.75

def init_weights(L, gain=1, Wmin = Wmin, Wmax = Wmax):

    W = L._weights
    N = np.random.normal(0.5, 0.005, W.shape)
    N = np.minimum(np.maximum(N, 0.0),1.0)
    L._weights = gain*W*(Wmin + (Wmax - Wmin)*N)


def clip(V, Vmin, Vmax):
    return np.minimum(np.maximum(V, Vmin), Vmax)

