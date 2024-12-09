#include "process.h"
#include <stdlib.h>
#include <string.h>

// Crear un nuevo proceso
process_t* create_process(int pid, const char* name) {
    process_t* process = malloc(sizeof(process_t));
    process->pid = pid;
    process->time_remaining = 10; // Simulación: todos los procesos comienzan con 10 segundos
    strncpy(process->name, name, PROCESS_NAME_MAX_LEN);
    process->next = NULL;
    return process;
}

// Encolar un proceso
void enqueue_process(process_t** queue, process_t* process) {
    if (*queue == NULL) {
        *queue = process;
    } else {
        process_t* temp = *queue;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = process;
    }
}

// Desencolar un proceso
process_t* dequeue_process(process_t** queue) {
    if (*queue == NULL) {
        return NULL;
    }
    process_t* process = *queue;
    *queue = (*queue)->next;
    process->next = NULL;
    return process;
}
