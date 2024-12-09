#ifndef GESTOR_MEMORIA_H
#define GESTOR_MEMORIA_H

#include "process.h"
#include <stdbool.h>

typedef struct {
    process_t* proceso; // Apuntador al proceso (NULL si está libre)
    int pagina;         // Número de la página asignada
} Marco;

typedef struct {
    Marco* memoria;           // Memoria física representada como un array de marcos
    int* marcos_libres;       // Array de índices de marcos libres
    int num_marcos;           // Número total de marcos
    int indice_marcos_libres; // Índice para seguimiento de marcos libres
} GestorMemoria;

// Inicializar el gestor de memoria
GestorMemoria* inicializar_gestor(int tamano_memoria, int tamano_pagina);

// Asignar memoria a un proceso
bool asignar_memoria(GestorMemoria* gestor, process_t* proceso, int tamano);

// Liberar memoria de un proceso
void liberar_memoria(GestorMemoria* gestor, process_t* proceso);

// Mostrar el estado actual de la memoria
void mostrar_estado_memoria(GestorMemoria* gestor);

// Liberar el gestor de memoria
void liberar_gestor(GestorMemoria* gestor);

#endif
