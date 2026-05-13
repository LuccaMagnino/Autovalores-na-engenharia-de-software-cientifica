#!/bin/bash
# Script de compilação para Linux/Mac

cd TESTE_C

echo "Compilando com gcc..."
gcc -std=c99 -Wall -Wextra -o eigenvalues main.c matrix.c -lm

if [ -f eigenvalues ]; then
    echo "Compilação bem-sucedida!"
    echo ""
    echo "Executando..."
    ./eigenvalues
else
    echo "Erro na compilação"
    exit 1
fi
