#include "GestorMemoria.h"
#include <stdio.h>
#include <stdlib.h>

// Inicializar el gestor de memoria
GestorMemoria* inicializar_gestor(int tamano_memoria, int tamano_pagina) {
    GestorMemoria* gestor = (GestorMemoria*)malloc(sizeof(GestorMemoria));
    gestor->num_marcos = tamano_memoria / tamano_pagina;
    gestor->memoria = (Marco*)malloc(gestor->num_marcos * sizeof(Marco));
    gestor->marcos_libres = (int*)malloc(gestor->num_marcos * sizeof(int));

    for (int i = 0; i < gestor->num_marcos; i++) {
        gestor->memoria[i].proceso = NULL;
        gestor->marcos_libres[i] = i;
    }
    gestor->indice_marcos_libres = 0;

    return gestor;
}

// Asignar memoria a un proceso
bool asignar_memoria(GestorMemoria* gestor, process_t* proceso, int tamano) {
    int paginas_necesarias = (tamano + gestor->num_marcos - 1) / gestor->num_marcos;

    if (gestor->indice_marcos_libres + paginas_necesarias > gestor->num_marcos) {
        printf("No hay suficiente memoria para el proceso %s\n", proceso->name);
        return false;
    }

    for (int i = 0; i < paginas_necesarias; i++) {
        int marco = gestor->marcos_libres[gestor->indice_marcos_libres++];
        gestor->memoria[marco].proceso = proceso;
        gestor->memoria[marco].pagina = i;
    }

    printf("Memoria asignada al proceso %s\n", proceso->name);
    return true;
}

// Liberar memoria de un proceso
void liberar_memoria(GestorMemoria* gestor, process_t* proceso) {
    for (int i = 0; i < gestor->num_marcos; i++) {
        if (gestor->memoria[i].proceso == proceso) {
            gestor->memoria[i].proceso = NULL;
            gestor->marcos_libres[--gestor->indice_marcos_libres] = i;
        }
    }
    printf("Memoria liberada para el proceso %s\n", proceso->name);
}

// Mostrar el estado actual de la memoria
void mostrar_estado_memoria(GestorMemoria* gestor) {
    printf("Estado de la memoria:\n");
    for (int i = 0; i < gestor->num_marcos; i++) {
        if (gestor->memoria[i].proceso != NULL) {
            printf("Marco %d: Proceso %s, Página %d\n", i, gestor->memoria[i].proceso->name, gestor->memoria[i].pagina);
        } else {
            printf("Marco %d: Libre\n", i);
        }
    }
}

// Liberar el gestor de memoria
void liberar_gestor(GestorMemoria* gestor) {
    free(gestor->memoria);
    free(gestor->marcos_libres);
    free(gestor);
}
