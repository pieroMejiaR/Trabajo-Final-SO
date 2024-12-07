#include "os_event.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// Crear un nuevo evento
os_event_t* create_event() {
    os_event_t* event = malloc(sizeof(os_event_t));
    event->completed = 0; // Inicialmente no completado
    event->waiting_process = NULL; // Ningún proceso esperando
    return event;
}

// Disparar (completar) un evento
void trigger_event(os_event_t* event) {
    if (event) {
        event->completed = 1; // Marca el evento como completado
        printf("[EVENT] Evento disparado.\n");
        if (event->waiting_process) {
            printf("[EVENT] Proceso %d ahora está listo.\n", event->waiting_process->pid);
            scheduler_add_process(event->waiting_process->pid, event->waiting_process->name);
            free(event->waiting_process);
        }
    }
}

// Asignar un proceso para esperar un evento
void wait_for_event(os_event_t* event, process_t* process) {
    if (event && process) {
        printf("[EVENT] Proceso %d está esperando un evento.\n", process->pid);
        event->waiting_process = process;
    }
}
