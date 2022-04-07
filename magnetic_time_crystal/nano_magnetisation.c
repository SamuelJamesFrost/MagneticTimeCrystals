#include <stddef.h>
#include <stdio.h>

int mod(int x, int N) {
    return (x % N + N) % N;
}

double nano_magnetisation(signed char *lattice, size_t width, size_t height) {
    double stripe = 0;
    size_t row, col;

    for (size_t i = 0; i < width * height; i++) {
        col = i % width;
        row = i / height; 

        stripe -= lattice[height * row + col] * lattice[height * row + (col+1) % width];
        stripe += lattice[height * row + col] * lattice[height * (row+1) % height + col];
    }
    return stripe / (2 * width * height);
}

int nano_energy(signed char *lattice, size_t width, size_t height, size_t i, size_t j) {
    signed char centre = lattice[height * i + j];
    int J = 2;
    int E = 0;
    E += J * centre * lattice[height * i + mod(j+1, width)];
    E += J * centre * lattice[height * i + mod(j-1, width)];
    E -= J * centre * lattice[height * mod(i+1, height) + j];
    E -= J * centre * lattice[height * mod(i-1, height) + j];
    
    return E;
}