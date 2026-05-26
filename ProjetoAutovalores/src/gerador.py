import numpy as np

def gerar_matriz_generica_real(n):
    
    A = np.random.randint(-10, 11, size=(n, n))
    
    A = A.astype(np.float64) 
    return A

def gerar_matriz_padrao():
    A = np.array([
        [4, 1, -2, 2],
        [1, 2, 0, 1],
        [-2, 0, 3, -2],
        [2, 1, -2, -1]
    ], dtype=np.float64)
    
    return A


