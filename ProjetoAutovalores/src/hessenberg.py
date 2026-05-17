import numpy as np

def reducao_hessenberg(A):
    """
    Reduz uma matriz quadrada genérica A à forma de Hessenberg Superior 
    usando reflexões de Householder.
    """
    n = A.shape[0]
    
    # Criamos uma cópia e garantimos que os números tenham casas decimais (float)
    H = np.copy(A).astype(float) 
    
    # O loop vai até n-2 porque não precisamos zerar a última coluna
    for k in range(n - 2):
        
        # 1. Extrai o vetor 'x' (os elementos abaixo da subdiagonal da coluna k)
        x = H[k+1:, k]
        
        # Calcula o tamanho (norma euclidiana) desse vetor
        norm_x = np.linalg.norm(x)
        
        # Se os elementos já forem zero, pulamos para a próxima coluna
        if norm_x == 0:
            continue
            
        # 2. Cria o vetor de Householder 'v'
        v = np.copy(x)
        
        # O sinal ajuda a evitar erros de arredondamento (estabilidade numérica)
        sinal = np.sign(x[0]) if x[0] != 0 else 1.0
        v[0] = v[0] + (sinal * norm_x)
        
        # Normaliza o vetor v (divide pelo seu próprio tamanho)
        v = v / np.linalg.norm(v)
        
        # 3. Aplica a reflexão pela Esquerda (Muda as linhas)
        # H = Q * H
        H[k+1:, k:] = H[k+1:, k:] - 2.0 * np.outer(v, np.dot(v, H[k+1:, k:]))
        
        # 4. Aplica a reflexão pela Direita (Muda as colunas)
        # H = H * Q
        H[:, k+1:] = H[:, k+1:] - 2.0 * np.outer(np.dot(H[:, k+1:], v), v)
        
    # Limpa possíveis "sujeiras" numéricas (valores minúsculos tipo 1e-16 que deveriam ser 0)
    for i in range(2, n):
        for j in range(i - 1):
            H[i, j] = 0.0
            
    return H