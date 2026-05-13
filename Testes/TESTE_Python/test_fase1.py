"""
Testes e validação para a Fase 1: Cálculo de Autovalores

Este script valida os algoritmos implementados em eigenvalue_solver.py
"""

import numpy as np
from eigenvalue_solver import EigenvalueSolver, create_test_matrix, verify_eigenvalues
import matplotlib.pyplot as plt


def test_fase1_basico():
    """Teste básico da Fase 1 com matriz tridiagonal pequena"""
    print("=" * 70)
    print("TESTE 1: Matriz Tridiagonal Pequena (5x5)")
    print("=" * 70)
    
    A = create_test_matrix(5, "tridiagonal")
    print("\nMatriz Original:")
    print(A)
    
    solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
    eigenvalues = solver.compute_eigenvalues(A)
    
    print("\n" + "=" * 70)
    print("AUTOVALORES ENCONTRADOS:")
    print("=" * 70)
    for i, lam in enumerate(eigenvalues):
        print(f"λ_{i+1} = {lam:15.10f}")
    
    verify_eigenvalues(A, eigenvalues, tol=1e-8)
    print()


def test_matriz_aleatoria():
    """Teste com matriz aleatória genérica"""
    print("\n" + "=" * 70)
    print("TESTE 2: Matriz Aleatória Genérica (7x7)")
    print("=" * 70)
    
    A = create_test_matrix(7, "random")
    print("\nMatriz Original:")
    print(A)
    
    solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
    eigenvalues = solver.compute_eigenvalues(A)
    
    print("\n" + "=" * 70)
    print("AUTOVALORES ENCONTRADOS:")
    print("=" * 70)
    for i, lam in enumerate(eigenvalues):
        print(f"λ_{i+1} = {lam:15.10f}")
    
    verify_eigenvalues(A, eigenvalues, tol=1e-6)
    print()


def test_matriz_simetrica():
    """Teste com matriz simétrica (importante para Fase 3)"""
    print("\n" + "=" * 70)
    print("TESTE 3: Matriz Simétrica (6x6)")
    print("=" * 70)
    
    # Criar matriz simétrica
    B = np.random.randn(6, 6)
    A = B + B.T  # Garantir simetria
    
    print("\nMatriz Original (simétrica):")
    print(A)
    print(f"É simétrica? {np.allclose(A, A.T)}")
    
    solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
    eigenvalues = solver.compute_eigenvalues(A)
    
    print("\n" + "=" * 70)
    print("AUTOVALORES ENCONTRADOS:")
    print("=" * 70)
    for i, lam in enumerate(eigenvalues):
        print(f"λ_{i+1} = {lam:15.10f}")
    
    verify_eigenvalues(A, eigenvalues, tol=1e-8)
    
    # Autovalores de matrizes simétricas devem ser reais
    print(f"\nTodos os autovalores são reais? {np.allclose(np.imag(eigenvalues), 0)}")
    print()


def test_convergencia_hessenberg():
    """Visualizar a convergência do algoritmo QR"""
    print("\n" + "=" * 70)
    print("TESTE 4: Análise de Convergência")
    print("=" * 70)
    
    A = create_test_matrix(10, "tridiagonal")
    solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
    eigenvalues = solver.compute_eigenvalues(A)
    
    # Plotar convergência
    plt.figure(figsize=(10, 6))
    plt.semilogy(solver.convergence_history, 'b-', linewidth=2)
    plt.axhline(y=1e-10, color='r', linestyle='--', label='Tolerância')
    plt.xlabel('Iteração', fontsize=12)
    plt.ylabel('Norma da Subdiagonal', fontsize=12)
    plt.title('Convergência do Algoritmo QR', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('convergencia_qr.png', dpi=150)
    print(f"Gráfico salvo em: convergencia_qr.png")
    plt.show()
    print()


def benchmark_tamanhos():
    """Análise de desempenho para diferentes tamanhos de matriz"""
    print("\n" + "=" * 70)
    print("TESTE 5: Benchmark de Desempenho (Preparação para Fase 2)")
    print("=" * 70)
    
    import time
    
    sizes = [10, 20, 50, 100]
    times = []
    
    for n in sizes:
        A = create_test_matrix(n, "tridiagonal")
        solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
        
        start = time.time()
        eigenvalues = solver.compute_eigenvalues(A)
        elapsed = time.time() - start
        
        times.append(elapsed)
        print(f"n={n:3d}: {elapsed:.6f}s ({solver.iterations_needed} iterações QR)")
    
    # Plotar
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Tamanho da Matriz (n)', fontsize=12)
    plt.ylabel('Tempo (s)', fontsize=12)
    plt.title('Tempo de Execução vs Tamanho da Matriz', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('benchmark_tempo.png', dpi=150)
    print(f"Gráfico salvo em: benchmark_tempo.png")
    plt.show()
    print()


if __name__ == "__main__":
    # Executar todos os testes
    test_fase1_basico()
    test_matriz_aleatoria()
    test_matriz_simetrica()
    test_convergencia_hessenberg()
    benchmark_tamanhos()
    
    print("=" * 70)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 70)
