import numpy as np
from src.hessenberg import reducao_hessenberg

# Criando uma matriz 4x4 aleatória
np.random.seed(42) # Mantém os mesmos números aleatórios em todo teste
matriz_teste = np.random.rand(4, 4) * 10

print("--- MATRIZ ORIGINAL ---")
print(np.round(matriz_teste, 2))

# Aplicando nossa função
H = reducao_hessenberg(matriz_teste)

print("\n--- MATRIZ DE HESSENBERG ---")
print(np.round(H, 2))