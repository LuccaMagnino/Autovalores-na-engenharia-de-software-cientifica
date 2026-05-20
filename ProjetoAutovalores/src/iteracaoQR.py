import numpy as np
from numba import njit

@njit
def givens_rotation(a, b):
    if b == 0:
        c = 1.0
        s = 0.0
    else:
        if abs(b) > abs(a):
            r = a / b
            s = 1.0 / np.sqrt(1 + r**2)
            c = s * r
        else:
            r = b / a
            c = 1.0 / np.sqrt(1 + r**2)
            s = c * r
    return c, s

@njit
def passo_qr_hessenberg(H):
    n = H.shape[0]
    R = np.copy(H)
    
    c_list = np.zeros(n - 1)
    s_list = np.zeros(n - 1)
    
    for i in range(n - 1):
        c, s = givens_rotation(R[i, i], R[i+1, i])
        c_list[i] = c
        s_list[i] = s
        
        for j in range(i, n):
            temp1 = c * R[i, j] + s * R[i+1, j]
            temp2 = -s * R[i, j] + c * R[i+1, j]
            R[i, j] = temp1
            R[i+1, j] = temp2
            
    H_nova = np.copy(R)
    for i in range(n - 1):
        c = c_list[i]
        s = s_list[i]
        
        for j in range(i + 2):
            temp1 = c * H_nova[j, i] + s * H_nova[j, i+1]
            temp2 = -s * H_nova[j, i] + c * H_nova[j, i+1]
            H_nova[j, i] = temp1
            H_nova[j, i+1] = temp2
            
    return H_nova

@njit
def iteracao_qr(H, tol=1e-10, max_iter=2000):
    n = H.shape[0]
    
    H_atual = np.copy(H)
    autovalores = np.zeros(n)
    
    m = n
    while m > 1:
        for iteracao in range(max_iter):
            # Critério de deflação
            if abs(H_atual[m-1, m-2]) < tol:
                autovalores[m-1] = H_atual[m-1, m-1]
                m -= 1
                break
                
            # Shift (Deslocamento)
            mu = H_atual[m-1, m-1]
            
            for i in range(m):
                H_atual[i, i] -= mu
                
            sub_H = np.ascontiguousarray(H_atual[:m, :m])
            H_atual[:m, :m] = passo_qr_hessenberg(sub_H)
            
            for i in range(m):
                H_atual[i, i] += mu
                
        else:
            print("Aviso: Limite maximo de iteracoes atingido.")
            break
            
    autovalores[0] = H_atual[0, 0]
    
    return autovalores