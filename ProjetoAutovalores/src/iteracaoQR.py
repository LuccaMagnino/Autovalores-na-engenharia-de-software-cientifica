import numpy as np

def givens_rotation(a, b):
 
    # s = seno, c = cosseno
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

def passo_qr_hessenberg(H):

    n = H.shape[0]
    
 
    R = np.copy(H)
    
    #Armazena os c e s
    c_list = []
    s_list = []
    
    
    for i in range(n - 1):
        
        c, s = givens_rotation(R[i, i], R[i+1, i])
        
       
        c_list.append(c)
        s_list.append(s)
        

        for j in range(i, n):
            temp1 = c * R[i, j] + s * R[i+1, j]
            temp2 = -s * R[i, j] + c * R[i+1, j]
            R[i, j] = temp1
            R[i+1, j] = temp2
            
    #Construir a nova Matriz H = R * Q
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

def iteracao_qr(H, tol=1e-10, max_iter=2000):

    H_iter = np.copy(H).astype(float)
    n = H_iter.shape[0]
    
    m = n 
    
    for iteracao in range(max_iter):

        if m == 1:
            print(f"\n[+] Convergência total alcançada!")
            break
            
        H_ativa = H_iter[:m, :m]
        
        # Deslocamento de Rayleigh

        mu = H_ativa[-1, -1] 
        for i in range(m):
            H_ativa[i, i] -= mu
            
        H_ativa = passo_qr_hessenberg(H_ativa)
        
        for i in range(m):
            H_ativa[i, i] += mu
            
        H_iter[:m, :m] = H_ativa
        
        # Deflação: Verifica se a subdiagonal é pequena o suficiente para considerar o autovalor convergido
        if abs(H_iter[m-1, m-2]) < tol:
            H_iter[m-1, m-2] = 0.0  
            m -= 1                  
            
    
    autovalores = np.sort(np.diag(H_iter))
    return autovalores