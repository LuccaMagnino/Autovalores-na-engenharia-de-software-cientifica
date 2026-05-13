"""
Módulo para cálculo de autovalores usando redução de Hessenberg e algoritmo QR.

Este módulo implementa a Fase 1 do projeto de Equações Diferenciais Ordinárias:
1. Redução à Forma de Hessenberg (usando Transformações de Householder)
2. Algoritmo QR iterativo para encontrar autovalores
"""

import numpy as np
from typing import Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class EigenvalueSolver:
    """
    Classe para calcular autovalores de matrizes usando métodos numéricos.
    
    Métodos:
        - hessenberg_reduction: Reduz matriz para forma de Hessenberg
        - qr_decomposition: Decompõe matriz em QR
        - qr_algorithm: Encontra autovalores via iteração QR
    """
    
    def __init__(self, tolerance: float = 1e-10, max_iterations: int = 1000):
        """
        Inicializa o solver de autovalores.
        
        Args:
            tolerance: Tolerância de convergência para norma da subdiagonal
            max_iterations: Número máximo de iterações do algoritmo QR
        """
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.iterations_needed = 0
        self.convergence_history = []
    
    def householder_reflection(self, x: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Calcula o vetor de Householder para reflexão.
        
        A transformação de Householder v = x + sign(x[0])*||x||*e1
        reflete o vetor x para eliminar componentes.
        
        Args:
            x: Vetor a ser refletido
            
        Returns:
            Tupla (v normalizado, fator beta para reflexão)
        """
        norm_x = np.linalg.norm(x)
        
        if norm_x < 1e-14:
            return x / (norm_x + 1e-16), 0.0
        
        v = x.copy()
        v[0] = x[0] - np.sign(x[0]) * norm_x if x[0] != 0 else -norm_x
        
        norm_v = np.linalg.norm(v)
        if norm_v < 1e-14:
            return v / (norm_v + 1e-16), 0.0
        
        v = v / norm_v
        beta = 2.0 / (1.0 + np.sum(v[1:] ** 2))
        
        return v, beta
    
    def hessenberg_reduction(self, A: np.ndarray) -> np.ndarray:
        """
        Reduz uma matriz genérica à forma de Hessenberg Superior.
        
        Uma matriz está em forma de Hessenberg se todos os elementos
        abaixo da primeira subdiagonal são zero.
        
        Args:
            A: Matriz quadrada (n x n)
            
        Returns:
            Matriz H na forma de Hessenberg
        """
        n = A.shape[0]
        H = A.astype(np.float64).copy()
        
        for k in range(n - 2):
            # Extrair coluna k abaixo da diagonal
            x = H[k+1:, k].copy()
            
            if np.linalg.norm(x) < 1e-14:
                continue
            
            # Calcular reflexão de Householder
            v, beta = self.householder_reflection(x)
            
            # Aplicar reflexão P*H (lado esquerdo)
            for j in range(k, n):
                dot_product = np.dot(v, H[k+1:, j])
                H[k+1:, j] -= beta * dot_product * v
            
            # Aplicar reflexão H*P (lado direito)
            for i in range(n):
                dot_product = np.dot(H[i, k+1:], v)
                H[i, k+1:] -= beta * dot_product * v
            
            # Zeros explícitos
            H[k+2:, k] = 0.0
        
        return H
    
    def qr_decomposition(self, A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Decomposição QR usando Gram-Schmidt modificado.
        
        Decompõe A = Q*R onde Q é ortonormal e R é triangular superior.
        
        Args:
            A: Matriz quadrada (n x n)
            
        Returns:
            Tupla (Q, R) onde A = Q*R
        """
        n = A.shape[0]
        Q = np.zeros_like(A, dtype=np.float64)
        R = np.zeros((n, n), dtype=np.float64)
        
        for j in range(n):
            # Copiar coluna j
            q = A[:, j].copy()
            
            # Ortogonalizar contra colunas anteriores
            for i in range(j):
                R[i, j] = np.dot(Q[:, i], q)
                q = q - R[i, j] * Q[:, i]
            
            # Normalizar
            R[j, j] = np.linalg.norm(q)
            if R[j, j] > 1e-14:
                Q[:, j] = q / R[j, j]
            else:
                Q[:, j] = q
        
        return Q, R
    
    def subdiagonal_norm(self, H: np.ndarray) -> float:
        """
        Calcula a norma de Frobenius da subdiagonal de uma matriz.
        
        Usada para verificar convergência do algoritmo QR.
        
        Args:
            H: Matriz em forma de Hessenberg
            
        Returns:
            Norma da subdiagonal
        """
        return np.sqrt(np.sum(np.diag(H, -1) ** 2))
    
    def qr_algorithm(self, H: np.ndarray) -> np.ndarray:
        """
        Algoritmo QR iterativo para encontrar autovalores.
        
        Realiza iterações H_{k+1} = R_k * Q_k até convergência da subdiagonal.
        
        Args:
            H: Matriz em forma de Hessenberg
            
        Returns:
            Array dos autovalores
        """
        n = H.shape[0]
        H_k = H.astype(np.float64).copy()
        
        print("\nAlgoritmo QR iterativo:")
        print(f"{'Iteração':<12} {'Norma Subdiagonal':<20}")
        print("-" * 32)
        
        self.convergence_history = []
        
        for iteration in range(self.max_iterations):
            # Decomposição QR
            Q, R = self.qr_decomposition(H_k)
            
            # H_{k+1} = R * Q
            H_k = Q.T @ H_k @ Q
            
            # Verificar convergência
            subdiag_norm = self.subdiagonal_norm(H_k)
            self.convergence_history.append(subdiag_norm)
            
            if iteration < 20 or iteration % 50 == 0:
                print(f"{iteration+1:<12} {subdiag_norm:<20.10e}")
            
            if subdiag_norm < self.tolerance:
                print(f"{iteration+1:<12} {subdiag_norm:<20.10e}")
                print(f"Convergência atingida em {iteration + 1} iterações")
                self.iterations_needed = iteration + 1
                break
        
        # Extrair autovalores da diagonal
        eigenvalues = np.diag(H_k)
        
        return eigenvalues
    
    def compute_eigenvalues(self, A: np.ndarray) -> np.ndarray:
        """
        Calcula os autovalores de uma matriz.
        
        Pipeline completo:
        1. Redução à forma de Hessenberg
        2. Algoritmo QR iterativo
        
        Args:
            A: Matriz quadrada (n x n)
            
        Returns:
            Array dos autovalores
        """
        n = A.shape[0]
        if A.shape != (n, n):
            raise ValueError("A matriz deve ser quadrada")
        
        # Redução à forma de Hessenberg
        H = self.hessenberg_reduction(A)
        
        # Algoritmo QR
        eigenvalues = self.qr_algorithm(H)
        
        return eigenvalues


# ============================================================================
# Funções auxiliares para teste
# ============================================================================

def create_test_matrix(n: int, matrix_type: str = "tridiagonal") -> np.ndarray:
    """
    Cria matrizes teste para validação.
    
    Args:
        n: Tamanho da matriz
        matrix_type: "tridiagonal", "random", "identity"
        
    Returns:
        Matriz teste (n x n)
    """
    if matrix_type == "tridiagonal":
        # Matriz tridiagonal: diagonal=2, sub/super=-1
        A = 2.0 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)
    elif matrix_type == "random":
        np.random.seed(42)
        A = np.random.randn(n, n)
    elif matrix_type == "identity":
        A = np.eye(n)
    else:
        raise ValueError("Tipo de matriz desconhecido")
    
    return A


def verify_eigenvalues(A: np.ndarray, eigenvalues: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Verifica se os autovalores encontrados estão corretos (verificação parcial).
    
    Args:
        A: Matriz original
        eigenvalues: Autovalores encontrados
        tol: Tolerância de verificação
        
    Returns:
        True se verificação passou
    """
    # Comparar com np.linalg.eigvals
    np_eigenvalues = np.linalg.eigvals(A)
    np_eigenvalues_sorted = np.sort(np.real(np_eigenvalues))
    found_eigenvalues_sorted = np.sort(np.real(eigenvalues))
    
    error = np.max(np.abs(np_eigenvalues_sorted - found_eigenvalues_sorted))
    
    print(f"\nErro máximo vs numpy: {error:.2e}")
    print(f"Verificação: {'✓ PASSOU' if error < tol else '✗ FALHOU'}")
    
    return error < tol


if __name__ == "__main__":
    # Exemplo básico de uso
    print("=" * 60)
    print("FASE 1: CÁLCULO DE AUTOVALORES")
    print("=" * 60)
    
    # Criar matriz teste
    n = 5
    A = create_test_matrix(n, "tridiagonal")
    
    print(f"\nMatriz Original A ({n}x{n}):")
    print(A)
    
    # Calcular autovalores
    solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
    eigenvalues = solver.compute_eigenvalues(A)
    
    # Exibir resultados
    print("\n" + "=" * 60)
    print("AUTOVALORES ENCONTRADOS:")
    print("=" * 60)
    for i, lam in enumerate(eigenvalues):
        print(f"λ_{i+1} = {lam:15.10f}")
    
    # Verificação
    verify_eigenvalues(A, eigenvalues)
