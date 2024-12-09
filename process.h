#ifndef PROCESS_H
#define PROCESS_H

#define PROCESS_NAME_MAX_LEN 32

typedef enum { READY, RUNNING, WAITING } process_state_t;

typedef struct process {
    int pid;                      // ID del proceso
    int time_remaining;           // Tiempo restante para completar
    char name[PROCESS_NAME_MAX_LEN]; // Nombre del proceso
    process_state_t state;       // Estado del proceso
    struct process* next;         // Siguiente proceso en la cola
} process_t;

// Funciones para manejar procesos
process_t* create_process(int pid, const char* name);
void enqueue_process(process_t** queue, process_t* process);
process_t* dequeue_process(process_t** queue);

#endif
