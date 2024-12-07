#ifndef SCHEDULER_H
#define SCHEDULER_H

#define MAX_PROCESSES 10 // Número máximo de procesos permitidos

typedef enum { READY, RUNNING, WAITING } process_state_t;

// Estructura de un proceso
typedef struct {
    int pid;                     // ID del proceso
    char name[50];               // Nombre del proceso
    process_state_t state;       // Estado del proceso
} process_t;

// Funciones del scheduler
void io_init(void);
void scheduler_init();
void scheduler_add_process(const char* name);
void scheduler_schedule();
void scheduler_tick(); // Manejador para interrupciones del temporizador

#endif
