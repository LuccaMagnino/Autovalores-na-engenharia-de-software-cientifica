@echo off
REM Script de compilação para Windows

cd TESTE_C

echo Compilando com gcc...
gcc -std=c99 -Wall -Wextra -o eigenvalues.exe main.c matrix.c -lm

if exist eigenvalues.exe (
    echo Compilação bem-sucedida!
    echo.
    echo Executando...
    eigenvalues.exe
) else (
    echo Erro na compilação
    exit /b 1
)
