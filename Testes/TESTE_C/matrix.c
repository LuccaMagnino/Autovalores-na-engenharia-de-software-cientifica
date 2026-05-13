#include "matrix.h"

/* Alocação de memória para matriz */
Matrix* matrix_alloc(int rows, int cols) {
    Matrix *m = (Matrix *)malloc(sizeof(Matrix));
    m->rows = rows;
    m->cols = cols;
    m->data = (double **)malloc(rows * sizeof(double *));
    for (int i = 0; i < rows; i++) {
        m->data[i] = (double *)malloc(cols * sizeof(double));
    }
    return m;
}

/* Liberação de memória */
void matrix_free(Matrix *m) {
    if (m == NULL) return;
    for (int i = 0; i < m->rows; i++) {
        free(m->data[i]);
    }
    free(m->data);
    free(m);
}

/* Cópia de matriz */
void matrix_copy(Matrix *dst, Matrix *src) {
    if (dst->rows != src->rows || dst->cols != src->cols) {
        return;
    }
    for (int i = 0; i < src->rows; i++) {
        for (int j = 0; j < src->cols; j++) {
            dst->data[i][j] = src->data[i][j];
        }
    }
}

/* Inicializar matriz com zeros */
void matrix_zeros(Matrix *m) {
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            m->data[i][j] = 0.0;
        }
    }
}

/* Impressão de matriz */
void matrix_print(Matrix *m, const char *name) {
    printf("\n%s (%d x %d):\n", name, m->rows, m->cols);
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            printf("%12.6f ", m->data[i][j]);
        }
        printf("\n");
    }
}

/* Adição de matrizes */
void matrix_add(Matrix *result, Matrix *a, Matrix *b) {
    for (int i = 0; i < a->rows; i++) {
        for (int j = 0; j < a->cols; j++) {
            result->data[i][j] = a->data[i][j] + b->data[i][j];
        }
    }
}

/* Multiplicação de matrizes: result = a * b */
void matrix_multiply(Matrix *result, Matrix *a, Matrix *b) {
    matrix_zeros(result);
    for (int i = 0; i < a->rows; i++) {
        for (int j = 0; j < b->cols; j++) {
            for (int k = 0; k < a->cols; k++) {
                result->data[i][j] += a->data[i][k] * b->data[k][j];
            }
        }
    }
}

/* Norma de Frobenius da subdiagonal */
double matrix_norm(Matrix *m) {
    double norm = 0.0;
    for (int i = 1; i < m->rows; i++) {
        norm += m->data[i][i-1] * m->data[i][i-1];
    }
    return sqrt(norm);
}

/* 
 * Redução à Forma de Hessenberg usando Transformações de Householder
 * A transformação de Householder é uma reflexão que zeros os elementos abaixo do primeiro
 */
Matrix* hessenberg_reduction(Matrix *a) {
    int n = a->rows;
    Matrix *h = matrix_alloc(n, n);
    matrix_copy(h, a);
    
    /* Aplicar transformações de Householder coluna por coluna */
    for (int k = 0; k < n - 2; k++) {
        /* Construir vetor de Householder para coluna k */
        double norm_x = 0.0;
        for (int i = k + 1; i < n; i++) {
            norm_x += h->data[i][k] * h->data[i][k];
        }
        norm_x = sqrt(norm_x);
        
        if (norm_x < 1e-14) continue;
        
        /* Vetor v de Householder */
        double *v = (double *)malloc(n * sizeof(double));
        for (int i = 0; i < k + 1; i++) v[i] = 0.0;
        
        v[k + 1] = h->data[k + 1][k] - (h->data[k + 1][k] < 0 ? -norm_x : norm_x);
        double norm_v = v[k + 1] * v[k + 1];
        
        for (int i = k + 2; i < n; i++) {
            v[i] = h->data[i][k];
            norm_v += v[i] * v[i];
        }
        norm_v = sqrt(norm_v);
        
        if (norm_v < 1e-14) {
            free(v);
            continue;
        }
        
        for (int i = k + 1; i < n; i++) {
            v[i] /= norm_v;
        }
        
        /* Aplicar reflexão: H = I - 2*v*v^T */
        /* Primeiro: calcular H * H */
        for (int i = k + 1; i < n; i++) {
            double dot = 0.0;
            for (int j = k; j < n; j++) {
                dot += v[i] * h->data[i][j];
            }
            for (int j = k; j < n; j++) {
                h->data[i][j] -= 2.0 * v[i] * dot;
            }
        }
        
        /* Segundo: calcular H * H^T */
        for (int i = 0; i < n; i++) {
            double dot = 0.0;
            for (int j = k + 1; j < n; j++) {
                dot += h->data[i][j] * v[j];
            }
            for (int j = k + 1; j < n; j++) {
                h->data[i][j] -= 2.0 * dot * v[j];
            }
        }
        
        /* Limpar elementos abaixo da subdiagonal */
        for (int i = k + 2; i < n; i++) {
            h->data[i][k] = 0.0;
        }
        
        free(v);
    }
    
    return h;
}

/*
 * Decomposição QR usando Gram-Schmidt
 * Decompõe A = QR onde Q é ortogonal e R é triangular superior
 */
void qr_decomposition(Matrix *a, Matrix *q, Matrix *r) {
    int n = a->rows;
    matrix_zeros(q);
    matrix_zeros(r);
    
    for (int j = 0; j < n; j++) {
        /* Copiar coluna j de a para q */
        for (int i = 0; i < n; i++) {
            q->data[i][j] = a->data[i][j];
        }
        
        /* Ortogonalizar contra colunas anteriores */
        for (int k = 0; k < j; k++) {
            double dot = 0.0;
            for (int i = 0; i < n; i++) {
                dot += q->data[i][k] * q->data[i][j];
            }
            r->data[k][j] = dot;
            for (int i = 0; i < n; i++) {
                q->data[i][j] -= dot * q->data[i][k];
            }
        }
        
        /* Normalizar */
        double norm = 0.0;
        for (int i = 0; i < n; i++) {
            norm += q->data[i][j] * q->data[i][j];
        }
        norm = sqrt(norm);
        r->data[j][j] = norm;
        
        if (norm > 1e-14) {
            for (int i = 0; i < n; i++) {
                q->data[i][j] /= norm;
            }
        }
    }
}

/*
 * Algoritmo QR para encontrar autovalores
 * Itera até convergência: H_{k+1} = R_k * Q_k
 */
void qr_algorithm(Matrix *h, double *eigenvalues, int max_iter, double tol) {
    int n = h->rows;
    Matrix *H = matrix_alloc(n, n);
    Matrix *Q = matrix_alloc(n, n);
    Matrix *R = matrix_alloc(n, n);
    Matrix *temp = matrix_alloc(n, n);
    
    matrix_copy(H, h);
    
    printf("\nAlgoritmo QR iterativo:\n");
    printf("Iteração\tNorma Subdiagonal\n");
    
    for (int iter = 0; iter < max_iter; iter++) {
        /* Decomposição QR */
        qr_decomposition(H, Q, R);
        
        /* H = R * Q */
        matrix_multiply(temp, R, Q);
        matrix_copy(H, temp);
        
        /* Verificar convergência */
        double subdiag_norm = matrix_norm(H);
        printf("%d\t\t%.10e\n", iter + 1, subdiag_norm);
        
        if (subdiag_norm < tol) {
            printf("Convergência atingida em %d iterações\n", iter + 1);
            break;
        }
    }
    
    /* Extrair autovalores da diagonal */
    for (int i = 0; i < n; i++) {
        eigenvalues[i] = H->data[i][i];
    }
    
    matrix_free(H);
    matrix_free(Q);
    matrix_free(R);
    matrix_free(temp);
}
