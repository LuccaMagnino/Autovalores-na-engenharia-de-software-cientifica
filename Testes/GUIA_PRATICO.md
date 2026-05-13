# Guia Prático - Como Usar os Código da Fase 1

## Execução Rápida

### Python (Recomendado para Desenvolvimento)

```bash
cd Python
python eigenvalue_solver_simple.py
```

Esperado: Matriz 5×5 com autovalores encontrados ✓

### C (Recomendado para Performance)

```bash
cd TESTE_C

# Windows
compile.bat

# Linux/Mac
bash compile.sh

# Ou manualmente
gcc -std=c99 -Wall -Wextra -o eigenvalues.exe main.c matrix.c -lm
./eigenvalues.exe
```

---

## Estrutura do Código

### Python: `eigenvalue_solver_simple.py`

**Classe Principal:**
```python
solver = EigenvalueSolver(tolerance=1e-10, max_iterations=1000)
eigenvalues = solver.compute_eigenvalues(A)
```

**Funções Auxiliares:**
- `Matrix` - Classe simples para operações matriciais
- `create_test_matrix(n, type)` - Cria matrizes de teste
- `hessenberg_reduction(A)` - Reduz à forma de Hessenberg
- `qr_decomposition(A)` - Decomposição QR
- `qr_algorithm(H)` - Iteração QR

### C: `matrix.c` + `matrix.h`

**Estrutura Principal:**
```c
typedef struct {
    double **data;  /* Dados */
    int rows;       /* Linhas */
    int cols;       /* Colunas */
} Matrix;
```

**Funções Principais:**
```c
Matrix* matrix_alloc(int rows, int cols);
Matrix* hessenberg_reduction(Matrix *a);
void qr_decomposition(Matrix *a, Matrix *q, Matrix *r);
void qr_algorithm(Matrix *h, double *eigenvalues, int max_iter, double tol);
```

---

## Customizações Comuns

### 1. Mudar Tamanho da Matriz

**Python:**
```python
# Em phase1_demo()
n = 10  # Mudar de 5 para 10
A = Matrix.tridiagonal(n)
```

**C:**
```c
// Em main()
int n = 10;  // Mudar de 5 para 10
```

### 2. Mudar Tolerância de Convergência

**Python:**
```python
solver = EigenvalueSolver(tolerance=1e-12, max_iterations=1000)
```

**C:**
```c
qr_algorithm(H, eigenvalues, 1000, 1e-12);  // 3º parâmetro
```

### 3. Usar Matriz Diferente

**Python:**
```python
# Criar matriz aleatória
n = 10
A_random = [[float(i+j) for j in range(n)] for i in range(n)]
A = Matrix(A_random)
```

**C:**
```c
// Preencher manualmente A->data
for(int i = 0; i < n; i++) {
    for(int j = 0; j < n; j++) {
        A->data[i][j] = i + j;  // exemplo
    }
}
```

### 4. Salvar Resultados em Arquivo

**Python:**
```python
import json

# Após calcular eigenvalues
with open('eigenvalues.json', 'w') as f:
    json.dump({
        'n': len(eigenvalues),
        'eigenvalues': eigenvalues,
        'iterations': solver.iterations_needed
    }, f, indent=2)
```

**C:**
```c
// Após calcular eigenvalues
FILE *f = fopen("eigenvalues.txt", "w");
fprintf(f, "n=%d\n", n);
for(int i = 0; i < n; i++) {
    fprintf(f, "lambda_%d = %.15f\n", i+1, eigenvalues[i]);
}
fclose(f);
```

---

## Verificação e Debugging

### Como Verificar se está Correto

1. **Verificar convergência:**
   - Norma da subdiagonal deve atingir ~1e-11 ou melhor
   - Deve acontecer em ~100-200 iterações para n≤10

2. **Verificar autovalores:**
   - Devem estar em ordem (não necessariamente, mas útil)
   - Para matriz tridiagonal: λ = 2 + 2·cos(k·π/(n+1))

3. **Verificar forma de Hessenberg:**
   - Todos os elementos H[i][j] = 0 para i > j+1
   - Imprimir matriz após redução

### Print Debug (Python)

```python
print("\nMatriz Original:")
A.print("A")

print("\nAntes do QR, Hessenberg é:")
H.print("H")

print(f"\nTolera: {solver.tolerance}")
print(f"Iterações: {solver.iterations_needed}")
print(f"Histórico: {solver.convergence_history[:10]}")  # Primeiras 10
```

### Print Debug (C)

```c
matrix_print(A, "Matriz A");
matrix_print(H, "Matriz H (Hessenberg)");
printf("Norma subdiagonal: %.2e\n", matrix_norm(H));
```

---

## Prototipagem para Fase 2

Para **Fase 2** (Escalabilidade), use este template:

**Python:**
```python
import time

sizes = [10, 50, 100, 250, 500]
times = []

for n in sizes:
    A = Matrix.tridiagonal(n)
    solver = EigenvalueSolver(tolerance=1e-10)
    
    start = time.time()
    eigenvalues = solver.compute_eigenvalues(A)
    elapsed = time.time() - start
    
    times.append(elapsed)
    print(f"n={n:4d}: {elapsed:.6f}s")

# Análise de complexidade
# Se tempo ∝ n^3, então tempo(2n) ≈ 8*tempo(n)
```

**C:**
```c
#include <time.h>

clock_t start = clock();
qr_algorithm(H, eigenvalues, 1000, 1e-10);
clock_t end = clock();
double elapsed = (double)(end - start) / CLOCKS_PER_SEC;

printf("Tempo: %.6f segundos\n", elapsed);
```

---

## Troubleshooting

### Problema: Não Converge

**Solução:**
- Aumentar `max_iterations` (tente 5000)
- Diminuir tolerância (tente 1e-8 em vez de 1e-10)
- Verificar se matriz está em forma de Hessenberg

### Problema: Autovalores Incorretos

**Verificar:**
1. Hessenberg reduction produziu zeros corretos?
2. QR decomposition está ortogonal? (Q^T*Q ≈ I)
3. Tolerância é suficiente pequena?

### Problema: Valores NaN ou Inf

**Causas:**
- Divisão por zero (norm muito pequeno)
- Overflow numérico
- Matriz singular/mal-condicionada

**Fix:**
```c
if (norm > 1e-14) {
    // dividir
} else {
    // tratar caso especial
}
```

---

## Próximas Etapas

### Preparação para Fase 2

Você precisa:
1. ✓ Redimensionar matriz (N até 1000)
2. ✓ Medir tempo de execução
3. ✓ Registrar uso de memória
4. ✓ Criar gráficos N vs Tempo e N vs Memória

### Preparação para Fase 3

Você vai:
1. Verificar se matriz é simétrica: `A == A^T`
2. Se for simétrica, usar redução tridiagonal
3. Comparar performance

### Preparação para Fase 4

Você vai usar:
```python
# Matriz para rede de reatores
diagonal = -2.5
super_diagonal = 1.0
sub_diagonal = 1.0

n = 100
A = criar_matriz_tridiagonal(n, diagonal, super_diagonal, sub_diagonal)

# Calcular autovalores
eigenvalues = solver.compute_eigenvalues(A)

# Razão de rigidez
stiffness_ratio = max(abs(eigenvalues)) / min(abs(eigenvalues))
```

---

## Referências Matemáticas

### Teorema de Householder
Um vetor de Householder $v$ define uma reflexão que zera componentes de um vetor $x$.

### Algoritmo QR
Converge pois: $H^{(k)} \to$ forma triangular superior (autovalores na diagonal)

### Estabilidade
Ambas Householder e QR são backward-stable para matrizes bem-condicionadas.

---

## Contato e Dúvidas

Se houver problemas:
1. Verificar saída do programa (vê os números?)
2. Comparar com soluções teóricas conhecidas
3. Testar com matrizes pequenas primeiro (n=3)
4. Usar printf/print para debug incrementalmente

**Dica:** Sempre teste com matrizes conhecidas antes de usar aleatórias!
