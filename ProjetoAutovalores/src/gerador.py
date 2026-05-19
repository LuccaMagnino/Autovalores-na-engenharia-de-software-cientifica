import numpy as np

def gerar_matriz_generica_real(n):

    autovalores = (np.random.rand(n) - 0.5) * 20
    D = np.diag(autovalores)
    
    V = np.random.rand(n, n)

    V_inv = np.linalg.inv(V)
    A = np.dot(V, np.dot(D, V_inv))
    
    return A

def gerar_matriz_padrao():

    A = np.array([
        [4.0, 1.0, -2.0, 2.0],
        [1.0, 2.0, 0.0, 1.0],
        [-2.0, 0.0, 3.0, -2.0],
        [2.0, 1.0, -2.0, -1.0]
    ])
    return A