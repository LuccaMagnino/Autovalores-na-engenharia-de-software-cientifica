#include "matrix.h"

/*
 * Programa para Fase 1: Cálculo de Autovalores
 * Redução à Forma de Hessenberg + Algoritmo QR
 */

int main() {
    int n = 5;  /* Tamanho da matriz para teste */
    
    /* Criar matriz teste (simétrica para teste) */
    Matrix *A = matrix_alloc(n, n);
    
    /* Inicializar com valores simples (matriz teste) */
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                A->data[i][j] = 2.0;
            } else if (i == j + 1 || i == j - 1) {
                A->data[i][j] = -1.0;
            } else {
                A->data[i][j] = 0.0;
            }
        }
    }
    
    printf("========== FASE 1: CÁLCULO DE AUTOVALORES ==========\n");
    matrix_print(A, "Matriz A Original");
    
    /* Passo 1: Redução à forma de Hessenberg */
    printf("\n--- Passo 1: Redução à Forma de Hessenberg ---");
    Matrix *H = hessenberg_reduction(A);
    matrix_print(H, "Matriz H (Hessenberg)");
    
    /* Passo 2: Algoritmo QR */
    printf("\n--- Passo 2: Algoritmo QR para Autovalores ---");
    double *eigenvalues = (double *)malloc(n * sizeof(double));
    qr_algorithm(H, eigenvalues, 1000, 1e-10);
    
    /* Impressão dos autovalores */
    printf("\nAutovalores encontrados:\n");
    for (int i = 0; i < n; i++) {
        printf("λ_%d = %.10f\n", i + 1, eigenvalues[i]);
    }
    
    /* Limpeza de memória */
    matrix_free(A);
    matrix_free(H);
    free(eigenvalues);
    
    printf("\n========== FIM DA FASE 1 ==========\n");
    
    return 0;
}
