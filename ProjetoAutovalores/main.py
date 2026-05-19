import numpy as np
import time
import os
import tracemalloc
from src.hessenberg import reducao_hessenberg
from src.iteracaoQR import iteracao_qr
from src.gerador import gerar_matriz_generica_real, gerar_matriz_padrao

def rodar_teste(A, nome_teste):
    print(f"\n{'='*60}")
    print(f"[{nome_teste}] - Iniciando...")
    n = A.shape[0]
    
    if n <= 10:
        print("\n--- MATRIZ ORIGINAL (A) ---")
        print(np.round(A, 4))
    
    inicio_tempo = time.time()
    tracemalloc.start()
    
    H = reducao_hessenberg(A)
    
    if n <= 10:
        print("\n--- MATRIZ DE HESSENBERG  ---")
        print(np.round(H, 4))
        
    autovalores = iteracao_qr(H)
    
    _, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    fim_tempo = time.time()
    tempo_total = fim_tempo - inicio_tempo
    pico_mb = pico_memoria / (1024 * 1024)
    
    print("\n" + "-" * 60)
    print(f"Tempo de Execução Computacional: {tempo_total:.4f} segundos")
    print(f"Pico de Consumo de Memória RAM: {pico_mb:.4f} MB")
    print("-" * 60)
    
    if n <= 10:
        print("\n--- AUTOVALORES ENCONTRADOS ---")
        print(np.sort(np.round(autovalores, 4)))
        print(f"{'='*60}")
    else:

        pasta_resultados = "resultados"
        os.makedirs(pasta_resultados, exist_ok=True)
        
        sufixo_nome = nome_teste.lower().replace(" ", "_").replace("x", "_")
        arq_original = os.path.join(pasta_resultados, f"{sufixo_nome}_matriz_original.csv")
        arq_hessenberg = os.path.join(pasta_resultados, f"{sufixo_nome}_matriz_hessenberg.csv")
        arq_autovalores = os.path.join(pasta_resultados, f"{sufixo_nome}_autovalores.csv")
        
        np.savetxt(arq_original, A, delimiter=";", fmt="%.6f")
        np.savetxt(arq_hessenberg, H, delimiter=";", fmt="%.6f")
        np.savetxt(arq_autovalores, np.sort(autovalores), delimiter=";", fmt="%.6f")
        
        print(f"[+] Sucesso: {n} autovalores fornecidos.")
        print(f"[+] Planilhas exportadas para a pasta './{pasta_resultados}/':")
        print(f"    1. {os.path.basename(arq_original)}")
        print(f"    2. {os.path.basename(arq_hessenberg)}")
        print(f"    3. {os.path.basename(arq_autovalores)}")
        print(f"{'='*60}")

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("   PROJETO AUTOVALORES - MENU PRINCIPAL")
        print("="*40)
        print("Escolha o tamanho da matriz (N) para testar:")
        print("[1] Teste Padrão (Matriz 4x4)")
        print("[2] N = 10")
        print("[3] N = 50")
        print("[4] N = 100")
        print("[5] N = 250")
        print("[6] N = 500")
        print("[7] N = 1000")
        print("[0] Sair do Programa")
        
        escolha = input("\nDigite a opção desejada: ")
        
        if escolha == '0':
            print("Encerrando o programa.")
            break
            
        elif escolha == '1':
            A = gerar_matriz_padrao()
            rodar_teste(A, "Matriz_4x4")
            
        elif escolha in ['2', '3', '4', '5', '6', '7']:
            tamanhos = {'2': 10, '3': 50, '4': 100, '5': 250, '6': 500, '7': 1000}
            n = tamanhos[escolha]
            
            A = gerar_matriz_generica_real(n)
            rodar_teste(A, f"Matriz_{n}x{n}")
            
        else:
            print("Opção inválida! Digite um número de 0 a 7.")
            
        input("\nPressione ENTER para voltar ao menu e fazer outro teste...")

if __name__ == "__main__":
    np.set_printoptions(suppress=True, linewidth=120)
    menu_principal()