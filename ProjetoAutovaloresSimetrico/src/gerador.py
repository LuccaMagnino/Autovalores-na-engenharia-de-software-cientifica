import numpy as np

def gerar_matriz_generica_real(n):

    A = np.random.randint(-5, 6, size=(n, n))
    
    # Tornando a matriz simétrica
    A = A + A.T

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

def gerar_matriz_reatores():
    
    N = 100
    
    diag_principal = -2.5
    diag_secundaria = 1.0
    
    A = np.zeros((N,N))
    
    for i in range(N):
        
        A[i, i] = diag_principal
        
        if i > 0:
            A[i, i-1] = diag_secundaria
            
        if i < N - 1:
            A[i, i + 1] = diag_secundaria
    print("\n")    
    print(A)
    return A