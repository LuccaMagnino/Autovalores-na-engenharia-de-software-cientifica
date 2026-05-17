import numpy as np

def iteracao_qr(H, tol=1e-10):
    """
    Aplica o algoritmo QR iterativo em uma matriz de Hessenberg H.
    O loop continua até que os elementos da subdiagonal convirjam para zero.
    """
    # Cópia para não alterar a H original
    A_k = np.copy(H)
    n = A_k.shape[0]
    
    # DICA: Aqui entrará um loop (while) que vai rodar infinitamente 
    # até que a condição de tolerância seja atingida.
    # Dentro do loop, você fará a fatoração QR e inverterá a ordem: A_k+1 = R * Q
    
    return np.diag(A_k) # Retorna apenas a diagonal principal (os autovalores)