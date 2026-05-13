"""
Versão simplificada de Solver de Autovalores usando apenas bibliotecas padrão Python.
Implementa os mesmos algoritmos da Fase 1 sem dependências externas.
"""

import math
from typing import List, Tuple


class Matrix:
    """Classe simples para operações com matrizes"""
    
    def __init__(self, data: List[List[float]]):
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
        self.data = [row[:] for row in data]
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def copy(self):
        """Retorna uma cópia da matriz"""
        return Matrix(self.data)
    
    def print(self, name="Matrix"):
        """Imprime a matriz"""
        print(f"\n{name} ({self.rows}x{self.cols}):")
        for row in self.data:
            print("  " + "  ".join(f"{x:12.6f}" for x in row))
    
    @staticmethod
    def identity(n: int):
        """Cria matriz identidade n x n"""
        data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        return Matrix(data)
    
    @staticmethod
    def tridiagonal(n: int):
        """Cria matriz tridiagonal: diagonal=2, sub/super=-1"""
        data = [[0.0] * n for _ in range(n)]
        for i in range(n):
            data[i][i] = 2.0
            if i > 0:
                data[i][i-1] = -1.0
            if i < n-1:
                data[i][i+1] = -1.0
        return Matrix(data)


def vector_norm(v: List[float]) -> float:
    """Calcula a norma Euclidiana de um vetor"""
    return math.sqrt(sum(x*x for x in v))


def dot_product(a: List[float], b: List[float]) -> float:
    """Calcula o produto escalar entre dois vetores"""
    return sum(x*y for x, y in zip(a, b))


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """Multiplica duas matrizes: result = A * B"""
    if A.cols != B.rows:
        raise ValueError("Dimensões incompatíveis")
    
    result_data = []
    for i in range(A.rows):
        row = []
        for j in range(B.cols):
            val = sum(A[i][k] * B[k][j] for k in range(A.cols))
            row.append(val)
        result_data.append(row)
    
    return Matrix(result_data)


def hessenberg_reduction(A: Matrix) -> Matrix:
    """
    Reduz uma matriz à forma de Hessenberg usando Transformações de Householder.
    
    Uma matriz de Hessenberg tem zeros abaixo da primeira subdiagonal.
    """
    H = A.copy()
    n = H.rows
    
    print(f"\nRedução à Forma de Hessenberg (n={n})...")
    
    for k in range(n - 2):
        # Extrair coluna k abaixo da diagonal
        x = [H[i][k] for i in range(k+1, n)]
        
        norm_x = vector_norm(x)
        if norm_x < 1e-14:
            continue
        
        # Construir vetor de Householder
        v = x[:]
        sign_x0 = 1.0 if x[0] >= 0 else -1.0
        v[0] = x[0] - sign_x0 * norm_x
        
        norm_v = vector_norm(v)
        if norm_v < 1e-14:
            continue
        
        v = [vi / norm_v for vi in v]
        
        # Aplicar reflexão H = I - 2*v*v^T
        # Lado esquerdo: H * H
        for j in range(k, n):
            dot_prod = sum(v[i] * H[k+1+i][j] for i in range(len(v)))
            for i in range(len(v)):
                H[k+1+i][j] -= 2.0 * v[i] * dot_prod
        
        # Lado direito: H * H^T
        for i in range(n):
            dot_prod = sum(H[i][k+1+j] * v[j] for j in range(len(v)))
            for j in range(len(v)):
                H[i][k+1+j] -= 2.0 * dot_prod * v[j]
        
        # Zeros explícitos abaixo
        for i in range(k+2, n):
            H[i][k] = 0.0
        
        print(f"  Coluna {k}: norma subdiagonal = {vector_norm([H[i][k] for i in range(k+2, n)]):.2e}")
    
    return H


def qr_decomposition(A: Matrix) -> Tuple[Matrix, Matrix]:
    """
    Decomposição QR usando Gram-Schmidt (clássico).
    Retorna Q (ortonormal) e R (triangular superior) tal que A = Q*R
    """
    n = A.rows
    Q_data = [[0.0] * n for _ in range(n)]
    R_data = [[0.0] * n for _ in range(n)]
    
    for j in range(n):
        # Copiar coluna j
        q = [A[i][j] for i in range(n)]
        
        # Ortogonalizar contra colunas anteriores
        for i in range(j):
            dot_prod = sum(Q_data[k][i] * q[k] for k in range(n))
            R_data[i][j] = dot_prod
            q = [q[k] - dot_prod * Q_data[k][i] for k in range(n)]
        
        # Normalizar
        norm_q = vector_norm(q)
        R_data[j][j] = norm_q
        
        if norm_q > 1e-14:
            q = [qi / norm_q for qi in q]
        
        for i in range(n):
            Q_data[i][j] = q[i]
    
    return Matrix(Q_data), Matrix(R_data)


def subdiagonal_norm(H: Matrix) -> float:
    """Calcula a norma da subdiagonal de uma matriz de Hessenberg"""
    subdiag = [H[i][i-1] for i in range(1, H.rows)]
    return vector_norm(subdiag)


def qr_algorithm(H: Matrix, max_iter: int = 1000, tol: float = 1e-10) -> List[float]:
    """
    Algoritmo QR iterativo para encontrar autovalores.
    Itera H_{k+1} = R_k * Q_k até convergência.
    """
    H_k = H.copy()
    n = H_k.rows
    
    print(f"\nAlgoritmo QR iterativo:")
    print(f"{'Iteração':<12} {'Norma Subdiagonal':<20} {'Produto Q*R':<20}")
    print("-" * 52)
    
    for iteration in range(max_iter):
        # Decomposição QR
        Q, R = qr_decomposition(H_k)
        
        # H_{k+1} = R * Q
        H_k = matrix_multiply(R, Q)
        
        # Verificar convergência
        subdiag_norm = subdiagonal_norm(H_k)
        
        if iteration < 20 or iteration % 100 == 0:
            print(f"{iteration+1:<12} {subdiag_norm:<20.10e}")
        
        if subdiag_norm < tol:
            print(f"{iteration+1:<12} {subdiag_norm:<20.10e}")
            print(f"✓ Convergência atingida em {iteration + 1} iterações")
            break
    
    # Extrair autovalores da diagonal
    eigenvalues = [H_k[i][i] for i in range(n)]
    
    return eigenvalues


def phase1_demo():
    """Demonstração completa da Fase 1"""
    
    print("=" * 70)
    print("FASE 1: CÁLCULO DE AUTOVALORES")
    print("Redução de Hessenberg + Algoritmo QR")
    print("=" * 70)
    
    # Criar matriz teste
    n = 5
    A = Matrix.tridiagonal(n)
    A.print("Matriz Original (Tridiagonal)")
    
    # Passo 1: Redução à Hessenberg
    H = hessenberg_reduction(A)
    H.print("Matriz H (Forma de Hessenberg)")
    
    # Passo 2: Algoritmo QR
    print("\n--- Passo 2: Algoritmo QR ---")
    eigenvalues = qr_algorithm(H, max_iter=1000, tol=1e-10)
    
    # Resultados
    print("\n" + "=" * 70)
    print("AUTOVALORES ENCONTRADOS:")
    print("=" * 70)
    for i, lam in enumerate(eigenvalues):
        print(f"λ_{i+1:2d} = {lam:15.10f}")
    
    # Comparação com solução teórica (para matriz tridiagonal)
    print("\n" + "=" * 70)
    print("VALIDAÇÃO:")
    print("=" * 70)
    print("Para matriz tridiagonal genérica de tamanho n=5:")
    print("Diagonal=2, Sub/Super-diagonal=-1")
    print("Os autovalores teóricos são: 2 + 2*cos(k*π/(n+1)) para k=1..n")
    
    import math
    theoretical_eigenvalues = []
    for k in range(1, n+1):
        lam = 2.0 + 2.0 * math.cos(k * math.pi / (n + 1))
        theoretical_eigenvalues.append(lam)
    
    theoretical_eigenvalues.sort()
    eigenvalues_sorted = sorted(eigenvalues)
    
    print("\nComparação:")
    print(f"{'k':<4} {'Encontrado':<20} {'Teórico':<20} {'Erro':<15}")
    print("-" * 59)
    
    max_error = 0
    for k in range(n):
        error = abs(eigenvalues_sorted[k] - theoretical_eigenvalues[k])
        max_error = max(max_error, error)
        print(f"{k+1:<4} {eigenvalues_sorted[k]:<20.10f} {theoretical_eigenvalues[k]:<20.10f} {error:<15.2e}")
    
    print(f"\nErro máximo: {max_error:.2e}")
    if max_error < 1e-8:
        print("✓ VALIDAÇÃO PASSOU")
    else:
        print("✗ VALIDAÇÃO FALHOU")
    
    print("\n" + "=" * 70)
    print("FIM DA FASE 1")
    print("=" * 70)


if __name__ == "__main__":
    phase1_demo()
