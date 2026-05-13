#ifndef MATRIX_H
#define MATRIX_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* Estrutura para representar uma matriz */
typedef struct {
    double **data;  /* Dados da matriz */
    int rows;       /* Número de linhas */
    int cols;       /* Número de colunas */
} Matrix;

/* Funções de manipulação de matrizes */
Matrix* matrix_alloc(int rows, int cols);
void matrix_free(Matrix *m);
void matrix_copy(Matrix *dst, Matrix *src);
void matrix_print(Matrix *m, const char *name);
void matrix_zeros(Matrix *m);

/* Operações básicas */
void matrix_add(Matrix *result, Matrix *a, Matrix *b);
void matrix_multiply(Matrix *result, Matrix *a, Matrix *b);
double matrix_norm(Matrix *m);

/* Funções para Hessenberg e QR */
Matrix* hessenberg_reduction(Matrix *a);
void qr_algorithm(Matrix *h, double *eigenvalues, int max_iter, double tol);
void qr_decomposition(Matrix *a, Matrix *q, Matrix *r);

#endif /* MATRIX_H */
