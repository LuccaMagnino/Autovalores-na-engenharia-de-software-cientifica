import numpy as np

## Função para reduzir uma matriz A à forma de Hessenberg usando transformações de Householder, retornando a matriz de Hessenberg H. ##

def reducao_hessenberg(A):
    
    #Pega o N da matriz
    n = A.shape[0]
    
    #Deixa todos os valores em float
    H = np.copy(A).astype(float) 
    
    #Loop desconsidera as ultimas duas colunas e a primeira linha
    for k in range(n - 2):
        
        x = H[k+1:, k]
        
        # Cálculo do tamanho do vetor
        tamanho_x = np.linalg.norm(x)
        
        if tamanho_x == 0:
            continue
#  
        v = np.copy(x)
        
        #Sinal para evitar cancelamento numérico
        sinal = np.sign(x[0]) if x[0] != 0 else 1.0
        v[0] = v[0] + (sinal * tamanho_x)
        
        # Normalização do vetor de Householder
        v = v / np.linalg.norm(v)
        
        # Aplicação da transformação de Householder à direita e à esquerda
        H[k+1:, k:] = H[k+1:, k:] - 2.0 * np.outer(v, np.dot(v, H[k+1:, k:]))
        H[:, k+1:] = H[:, k+1:] - 2.0 * np.outer(np.dot(H[:, k+1:], v), v)
        
    #Limpando os erros do float
    for i in range(2, n):
        for j in range(i - 1):
            H[i, j] = 0.0
            
    return H