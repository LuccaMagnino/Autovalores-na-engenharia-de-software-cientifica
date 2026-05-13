# Fase 1: Cálculo de Autovalores - Redução de Hessenberg + Algoritmo QR

## Descrição

Implementação da primeira etapa do projeto de Equações Diferenciais Ordinárias:
- **Redução à Forma de Hessenberg** usando Transformações de Householder
- **Algoritmo QR Iterativo** para encontrar autovalores

## Estrutura de Arquivos

```
TESTE_C/
├── matrix.h       # Cabeçalhos e estruturas
├── matrix.c       # Implementação dos algoritmos
├── main.c         # Programa principal com testes
├── CMakeLists.txt # Configuração CMake
└── compile.sh     # Script de compilação

Python/
├── eigenvalue_solver.py  # Classe EigenvalueSolver
└── test_fase1.py         # Testes e validação
```

## Compilação e Execução - C

### Com GCC (Windows/Linux):
```bash
cd TESTE_C
gcc -std=c99 -Wall -Wextra -o eigenvalues main.c matrix.c -lm
./eigenvalues
```

### Com CMake:
```bash
cd TESTE_C
mkdir build
cd build
cmake ..
make
./eigenvalues
```

## Execução - Python

### Requisitos:
```bash
pip install numpy scipy matplotlib
```

### Executar testes:
```bash
cd Python
python eigenvalue_solver.py
```

## Algoritmos Implementados

### 1. Transformação de Householder
- Reduz matriz genérica à forma de Hessenberg
- Elimina elementos abaixo da primeira subdiagonal
- Preserva autovalores

### 2. Decomposição QR (Gram-Schmidt)
- Fatora matriz A = Q*R
- Q: matriz ortonormal
- R: matriz triangular superior

### 3. Algoritmo QR Iterativo
- Itera: H_{k+1} = R_k * Q_k
- Converge até que subdiagonal < tolerância (10^-10)
- Extrai autovalores da diagonal

## Validação

Os autovalores encontrados são comparados com:
- Soluções numéricas de NumPy (`np.linalg.eigvals`)
- Erro máximo aceitável: 10^-8

## Próximas Fases

- **Fase 2**: Análise de escalabilidade (tempo e memória)
- **Fase 3**: Otimização para matrizes simétricas (tridiagonalização)
- **Fase 4**: Aplicação prática em dinâmica de reatores
