cmake_minimum_required(VERSION 3.10)
project(Eigenvalues C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -lm")

add_executable(eigenvalues main.c matrix.c matrix.h)
target_link_libraries(eigenvalues m)

# Para compilação com gcc/clang
# gcc -std=c99 -Wall -Wextra -o eigenvalues main.c matrix.c -lm
