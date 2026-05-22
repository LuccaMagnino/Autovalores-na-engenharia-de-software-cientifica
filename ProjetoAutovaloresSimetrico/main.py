import numpy as np
import time
import os
import tracemalloc
from src.hessenberg import reducao_hessenberg
from src.iteracaoQR import iteracao_qr
from src.gerador import gerar_matriz_generica_real, gerar_matriz_padrao

def calcular_multiplicidades(A, autovalores, tol=1e-4):
    n = A.shape[0]
    valores_arredondados = np.round(autovalores, 5)
    unicos = np.unique(valores_arredondados)
    
    resultados = []
    calcular_mg = n <= 50 
    
    for val in unicos:
        ma = np.sum(valores_arredondados == val)
        
        if calcular_mg:
            I = np.eye(n, dtype=np.float64)
            rank = np.linalg.matrix_rank(A - val * I, tol=tol)
            mg = n - rank
        else:
            mg = "N/A"
            
        resultados.append((val, ma, mg))
        
    return resultados

def rodar_teste(A, nome_teste):
    print(f"\n{'='*70}")
    print(f"[{nome_teste}] - Iniciando Fase 3 (Matriz Simétrica)...")
    n = A.shape[0]
    
    if n <= 5:
        print("\n--- MATRIZ ORIGINAL (A) ---")
        print(np.round(A, 2))
    
    inicio_tempo = time.time()
    tracemalloc.start()
    
    H = reducao_hessenberg(A)
    
    if n == 5:
        print("\n--- [ITEM 3.2] DEMONSTRAÇÃO EMPÍRICA: REDUÇÃO TRIDIAGONAL ---")
        print("Matriz H após as reflexões de Householder (arredondada para 4 casas):")
        print(np.round(H, 4))
        
        acima_superdiagonal = np.triu(H, k=2)
        abaixo_subdiagonal = np.tril(H, k=-2)
        
        is_hessenberg = np.allclose(abaixo_subdiagonal, 0, atol=1e-7)
        is_tridiagonal = np.allclose(acima_superdiagonal, 0, atol=1e-7)
        is_simetrica = np.allclose(H, H.T, atol=1e-7)
        
        print("\nLaudo Estrutural da Matriz:")
        print(f"1. Adoção da Forma de Hessenberg (zeros abaixo da 1ª subdiagonal) : {'[V] COMPROVADO' if is_hessenberg else '[X] FALHOU'}")
        print(f"2. Colapso Tridiagonal (zeros acima da 1ª superdiagonal)        : {'[V] COMPROVADO' if is_tridiagonal else '[X] FALHOU'}")
        print(f"3. Preservação da Simetria (H = H^T)                            : {'[V] COMPROVADO' if is_simetrica else '[X] FALHOU'}")
        print("-" * 70)
    elif n < 5:
        print("\n--- MATRIZ DE HESSENBERG / TRIDIAGONAL ---")
        print(np.round(H, 2))
        
    autovalores = iteracao_qr(H)
    
    _, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    fim_tempo = time.time()
    tempo_total = fim_tempo - inicio_tempo
    pico_mb = pico_memoria / (1024 * 1024)
    
    print("\n" + "-" * 70)
    print(f"Tempo de Execução Computacional: {tempo_total:.4f} segundos")
    print(f"Pico de Consumo de Memória RAM: {pico_mb:.4f} MB")
    print("-" * 70)
    
    if n <= 5:
        print("\n--- AUTOVALORES E MULTIPLICIDADES ---")
        mults = calcular_multiplicidades(A, autovalores)
        
        print(f"{'Autovalor (λ)':>20} | {'M. Algébrica':>15} | {'M. Geométrica':>15}")
        print("-" * 57)
        
        for val, ma, mg in mults:
            print(f"{val:20.2f} | {ma:15} | {mg:15}")
            
        print(f"{'='*70}")
    else:
        pasta_resultados = "resultados_fase3"
        os.makedirs(pasta_resultados, exist_ok=True)
        
        sufixo_nome = nome_teste.lower().replace(" ", "_").replace("x", "_")
        arq_original = os.path.join(pasta_resultados, f"{sufixo_nome}_matriz_original.csv")
        arq_hessenberg = os.path.join(pasta_resultados, f"{sufixo_nome}_matriz_tridiagonal.csv")
        arq_autovalores = os.path.join(pasta_resultados, f"{sufixo_nome}_autovalores.csv")
        
        np.savetxt(arq_original, A, delimiter=";", fmt="%.2f")
        np.savetxt(arq_hessenberg, H, delimiter=";", fmt="%.2f")
        
        mults = calcular_multiplicidades(A, autovalores)
        
        with open(arq_autovalores, 'w') as f:
            f.write("Autovalor;Multiplicidade Algebrica;Multiplicidade Geometrica\n")
            for val, ma, mg in mults:
                f.write(f"{val:.2f};{ma};{mg}\n")
        
        print(f"[+] Sucesso: {n} autovalores processados (Estritamente Reais).")
        if n > 50:
            print("[!] Aviso: Multiplicidade Geometrica omitida no CSV para evitar complexidade O(N^4).")
            
        print(f"[+] Planilhas exportadas para a pasta './{pasta_resultados}/'.")
        print(f"{'='*70}")

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("   PROJETO AUTOVALORES - MENU PRINCIPAL")
        print("="*40)
        print("[1] Teste Padrão (Matriz fixa 4x4)")
        print("[2] Gerar Matriz Aleatória (Escolher tamanho N)")
        print("[3] Demonstração Empírica (Redução de N=5)")
        print("[0] Sair do Programa")
        
        escolha = input("\nDigite a opção desejada: ")
        
        if escolha == '0':
            print("Encerrando o programa.")
            break
            
        elif escolha == '1':
            A = gerar_matriz_padrao()
            rodar_teste(A, "Matriz_4x4")
            
        elif escolha == '2':
            try:
                n = int(input("Digite o tamanho desejado para a matriz (N): "))
                if n <= 0:
                    print("[!] Erro: O tamanho da matriz deve ser um número inteiro positivo maior que zero.")
                    continue
                
                A = gerar_matriz_generica_real(n)
                rodar_teste(A, f"Matriz_{n}x{n}")
                
            except ValueError:
                print("[!] Erro: Entrada inválida. Por favor, digite apenas números inteiros (ex: 10, 50, 1000).")
                
        elif escolha == '3':

            A = gerar_matriz_generica_real(5)
            rodar_teste(A, "Demonstracao_N=5")
            
        else:
            print("Opção inválida! Digite um número do menu.")
            
        input("\nPressione ENTER para voltar ao menu e fazer outro teste...")

if __name__ == "__main__":
    np.set_printoptions(suppress=True, linewidth=120)
    menu_principal()