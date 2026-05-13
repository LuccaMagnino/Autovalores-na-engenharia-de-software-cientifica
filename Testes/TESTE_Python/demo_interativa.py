#!/usr/bin/env python3
"""
Demo Interativa - Fase 1: Cálculo de Autovalores

Este script demonstra como usar o solver de autovalores
com exemplos progressivamente mais complexos.
"""

from eigenvalue_solver_simple import (
    Matrix, 
    hessenberg_reduction, 
    qr_algorithm,
    subdiagonal_norm
)


def demo_basica():
    """Demo 1: Exemplo Básico com Matriz Tridiagonal"""
    print("\n" + "="*70)
    print("DEMO 1: Matriz Tridiagonal Simples (3x3)")
    print("="*70)
    
    # Criar matriz 3x3 tridiagonal
    A = Matrix.tridiagonal(3)
    print("\nMatriz Original A:")
    print("┌         ┐")
    print("│  2 -1  0│")
    print("│ -1  2 -1│")
    print("│  0 -1  2│")
    print("└         ┘")
    
    # Reduzir para Hessenberg
    H = hessenberg_reduction(A)
    print("\nMatriz H (Hessenberg):")
    print("Nota: Como A é simétrica, H = A")
    
    # Encontrar autovalores
    eigenvalues = qr_algorithm(H, max_iter=1000, tol=1e-10)
    
    print("\nAutovalores: ", [f"{x:.6f}" for x in sorted(eigenvalues)])
    print("✓ Demo 1 concluída")


def demo_maior():
    """Demo 2: Matriz Maior (7x7)"""
    print("\n" + "="*70)
    print("DEMO 2: Matriz Tridiagonal Maior (7x7)")
    print("="*70)
    
    A = Matrix.tridiagonal(7)
    print(f"Criada matriz {A.rows}x{A.cols} tridiagonal")
    
    # Mostrar primeiras 3 linhas
    print("\nPrimeiras 3 linhas de A:")
    for i in range(min(3, A.rows)):
        print("  " + "  ".join(f"{A[i][j]:6.1f}" for j in range(min(5, A.cols))))
    
    # Reduzir
    H = hessenberg_reduction(A)
    subdiag_before = subdiagonal_norm(H)
    print(f"\nNorma da subdiagonal inicial: {subdiag_before:.6e}")
    
    # Encontrar autovalores
    eigenvalues = qr_algorithm(H, max_iter=1000, tol=1e-10)
    
    print("\nAutovalores ordenados:")
    for i, lam in enumerate(sorted(eigenvalues, reverse=True)):
        print(f"  λ_{i+1:2d} = {lam:10.6f}")
    
    print("✓ Demo 2 concluída")


def demo_convergencia():
    """Demo 3: Visualizar Convergência do Algoritmo QR"""
    print("\n" + "="*70)
    print("DEMO 3: Análise de Convergência")
    print("="*70)
    
    A = Matrix.tridiagonal(5)
    H = hessenberg_reduction(A)
    
    print("\nExecutando algoritmo QR com histórico:")
    print(f"{'Iter':<6} {'Norma Subdiag':<18} {'Log10':<10}")
    print("-" * 34)
    
    # Executar manualmente para mostrar convergência
    H_k = H.copy()
    import math
    
    for iteration in range(20):
        from eigenvalue_solver_simple import qr_decomposition
        Q, R = qr_decomposition(H_k)
        H_k_new = Matrix([
            [sum(R[i][k] * Q[k][j] for k in range(5)) for j in range(5)]
            for i in range(5)
        ])
        H_k = H_k_new
        
        norm = subdiagonal_norm(H_k)
        log10_norm = math.log10(norm) if norm > 0 else -999
        
        print(f"{iteration+1:<6} {norm:<18.10e} {log10_norm:<10.2f}")
        
        if norm < 1e-10:
            print(f"{'':6} ✓ Convergência atingida!")
            break
    
    print("✓ Demo 3 concluída")


def demo_comparacao_tamanhos():
    """Demo 4: Comparação de Tamanhos"""
    print("\n" + "="*70)
    print("DEMO 4: Impacto do Tamanho da Matriz")
    print("="*70)
    
    import time
    
    sizes = [3, 5, 10, 20]
    print(f"\n{'Tamanho':<10} {'Iters QR':<12} {'Min Subdiag':<15}")
    print("-" * 37)
    
    for n in sizes:
        A = Matrix.tridiagonal(n)
        H = hessenberg_reduction(A)
        
        # Contar iterações
        H_k = H.copy()
        from eigenvalue_solver_simple import qr_decomposition
        
        iterations = 0
        for i in range(1000):
            Q, R = qr_decomposition(H_k)
            H_k_new = Matrix([
                [sum(R[i][k] * Q[k][j] for k in range(n)) for j in range(n)]
                for i in range(n)
            ])
            H_k = H_k_new
            norm = subdiagonal_norm(H_k)
            
            if norm < 1e-10:
                iterations = i + 1
                break
        
        print(f"{n:<10} {iterations:<12} {norm:<15.3e}")
    
    print("✓ Demo 4 concluída")


def main():
    """Menu Principal"""
    print("\n" + "="*70)
    print("DEMOS INTERATIVAS - FASE 1: CÁLCULO DE AUTOVALORES")
    print("="*70)
    print("""
Escolha uma demo:
  1. Matriz Tridiagonal Simples (3x3)
  2. Matriz Tridiagonal Maior (7x7)
  3. Análise de Convergência
  4. Comparação de Tamanhos
  5. Executar todas
  
  0. Sair
""")
    
    while True:
        try:
            choice = input("Escolha (0-5): ").strip()
            
            if choice == "0":
                print("\nFim das demos!")
                break
            elif choice == "1":
                demo_basica()
            elif choice == "2":
                demo_maior()
            elif choice == "3":
                demo_convergencia()
            elif choice == "4":
                demo_comparacao_tamanhos()
            elif choice == "5":
                demo_basica()
                demo_maior()
                demo_convergencia()
                demo_comparacao_tamanhos()
            else:
                print("❌ Opção inválida! Tente novamente.")
                continue
            
            # Pergunta se quer continuar
            cont = input("\nContinuar? (s/n): ").strip().lower()
            if cont != 's':
                break
                
        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    # Executar automaticamente todas as demos
    print("""
╔════════════════════════════════════════════════════════════════════╗
║           FASE 1: CÁLCULO DE AUTOVALORES - DEMONSTRAÇÕES           ║
║                                                                    ║
║  Algoritmo: Redução de Hessenberg + QR Iterativo                  ║
║  Tolerância: 1e-10                                                 ║
║  Máximo iterações: 1000                                            ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    # Executar todas as demos automaticamente
    demo_basica()
    demo_maior()
    demo_convergencia()
    demo_comparacao_tamanhos()
    
    print("\n" + "="*70)
    print("✓ TODAS AS DEMONSTRAÇÕES CONCLUÍDAS COM SUCESSO!")
    print("="*70)
    print("""
Próximas etapas:

1. Revisar os resultados acima
2. Comparar com valores teóricos
3. Preparar-se para Fase 2 (escalabilidade)

Para usar interativamente, descomente a linha:
    main()
""")
