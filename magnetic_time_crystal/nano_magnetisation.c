#include <stddef.h>

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