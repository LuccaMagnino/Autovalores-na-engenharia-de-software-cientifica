# Inventário de Arquivos - Fase 1

## 📂 Estrutura Completa do Projeto

```
c:\Projetos\EDO\
│
├── 📋 DOCUMENTAÇÃO
│   ├── README.md                   [Instruções gerais de compilação]
│   ├── GUIA_PRATICO.md             [Como usar os códigos - Tutorial]
│   ├── FASE1_RELATORIO.md          [Relatório técnico detalhado]
│   └── FASE1_COMPLETO.md           [Sumário final de conclusão]
│
├── 📁 TESTE_C/                     [Implementação em C]
│   ├── matrix.h                    [Headers e estruturas]
│   ├── matrix.c                    [Implementação do algoritmo]
│   ├── main.c                      [Programa principal + testes]
│   ├── CMakeLists.txt              [Build system CMake]
│   ├── compile.bat                 [Script Windows]
│   ├── compile.sh                  [Script Linux/Mac]
│   └── eigenvalues.exe             [Executável compilado]
│
└── 📁 Python/                      [Implementação em Python]
    ├── eigenvalue_solver_simple.py [Versão pura (PRINCIPAL)]
    ├── eigenvalue_solver.py        [Versão com NumPy]
    ├── test_fase1.py               [Testes completos]
    └── demo_interativa.py          [Demonstrações interativas]
```

## 📊 Estatísticas

| Linguagem | Arquivos | Linhas de Código | Funções |
|-----------|----------|------------------|---------|
| **C** | 4 | ~600 | 8 principais |
| **Python** | 4 | ~800 | 6 principais |
| **Docs** | 4 | ~1000 | N/A |
| **TOTAL** | **12** | **~2400** | **14+** |

## 🔧 Arquivos por Propósito

### Core Implementation

**C:**
- `TESTE_C/matrix.c` - Hessenberg reduction
- `TESTE_C/matrix.c` - QR decomposition
- `TESTE_C/matrix.c` - QR algorithm

**Python:**
- `Python/eigenvalue_solver_simple.py` - Classe EigenvalueSolver
- `Python/eigenvalue_solver_simple.py` - Matrix class
- `Python/eigenvalue_solver_simple.py` - Auxiliar functions

### Testing & Validation

- `Python/test_fase1.py` - Test suite completa
- `Python/demo_interativa.py` - Demo progresivas

### Compilation & Build

- `TESTE_C/CMakeLists.txt` - CMake configuration
- `TESTE_C/compile.bat` - Windows compilation
- `TESTE_C/compile.sh` - Unix compilation

### Documentation

- `README.md` - Overview do projeto
- `GUIA_PRATICO.md` - Tutorial prático
- `FASE1_RELATORIO.md` - Technical report
- `FASE1_COMPLETO.md` - Final summary

## 🎯 Funções Principais Implementadas

### C (`matrix.c`)

1. `matrix_alloc()` - Alocação de memória
2. `matrix_free()` - Liberação de memória
3. `matrix_copy()` - Cópia de matriz
4. `matrix_multiply()` - Multiplicação A×B
5. `hessenberg_reduction()` - Redução Householder
6. `qr_decomposition()` - Fatoração QR
7. `qr_algorithm()` - Algoritmo iterativo
8. `matrix_norm()` - Norma da subdiagonal

### Python (`eigenvalue_solver_simple.py`)

1. `class Matrix` - Operações matriciais
2. `vector_norm()` - Norma Euclidiana
3. `dot_product()` - Produto escalar
4. `matrix_multiply()` - Multiplicação
5. `hessenberg_reduction()` - Redução Householder
6. `qr_decomposition()` - Fatoração QR
7. `qr_algorithm()` - Iteração QR
8. `subdiagonal_norm()` - Norma subdiagonal
9. `phase1_demo()` - Demo completa

## 📥 Arquivos que Precisam de Entrada

Nenhum arquivo requer entrada do usuário por padrão. Mas você pode customizar:

- Tamanho da matriz: `n = 5` → `n = 100`
- Tolerância: `1e-10` → `1e-12`
- Máximo iterações: `1000` → `5000`

## 📤 Arquivos de Saída Esperados

Quando você executa:

**Python:**
- `convergencia_qr.png` - Gráfico de convergência (de `test_fase1.py`)
- `benchmark_tempo.png` - Benchmark vs tamanho (de `test_fase1.py`)

**C:**
- Stdout com autovalores e iterações

## 🔐 Dependências

### C
- GCC (compilador C)
- Biblioteca padrão: `stdio.h`, `stdlib.h`, `math.h`, `string.h`
- ✅ Nenhuma dependência externa

### Python (Versão Simples)
- Python 3.6+
- ✅ Nenhuma dependência! (usa apenas built-ins)

### Python (Versão NumPy)
- numpy
- scipy
- matplotlib

## 🚀 Como Começar (5 minutos)

### Opção 1: Python (Recomendado)
```bash
cd Python
python eigenvalue_solver_simple.py
```
**Tempo:** ~2 segundos  
**Resultado:** Autovalores para matriz 5×5

### Opção 2: C
```bash
cd TESTE_C
gcc -std=c99 -Wall -Wextra -o eigenvalues.exe main.c matrix.c -lm
eigenvalues.exe
```
**Tempo:** ~1 segundo (compilação) + ~0.1s (execução)  
**Resultado:** Mesmos autovalores

### Opção 3: Demonstrações
```bash
cd Python
python demo_interativa.py
```
**Tempo:** ~5 segundos  
**Resultado:** 4 demos diferentes com análises

## 📖 Arquivos para Aprender

**Para entender os algoritmos:**
1. Comece com: `GUIA_PRATICO.md`
2. Depois leia: `FASE1_RELATORIO.md` (seção matemática)
3. Veja o código: `Python/eigenvalue_solver_simple.py` (mais legível)

**Para adaptar para seu uso:**
1. Copie de: `Python/eigenvalue_solver_simple.py`
2. Customize: Tamanho, tipo de matriz, tolerância
3. Execute: `python seu_script.py`

**Para Fase 2 (próximo):**
1. Baseie em: `Python/test_fase1.py`
2. Altere: Gerar múltiplos tamanhos N
3. Adicione: Medição de tempo e memória

## ✅ Checklist de Validação

Todos os arquivos foram validados:

- ✅ C compila sem erros/warnings
- ✅ C executa e produz resultados corretos
- ✅ Python executa sem dependências externas
- ✅ Python produz mesmos resultados que C
- ✅ Validação matemática passou (erro < 1e-8)
- ✅ Documentação está completa
- ✅ Exemplos funcionam

## 🔄 Versionamento

- **Versão:** 1.0
- **Status:** Completo e Validado
- **Data:** 2026-05-13
- **Próximo:** Fase 2

---

Para dúvidas, consulte:
- `GUIA_PRATICO.md` - Troubleshooting
- `FASE1_RELATORIO.md` - Detalhes técnicos
- Comentários nos arquivos de código
