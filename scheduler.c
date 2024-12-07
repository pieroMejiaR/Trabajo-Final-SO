#include "scheduler.h"
#include "irq.h"
#include <stdio.h>

#define TIME_QUANTUM 2 // Tiempo de ejecución por proceso (en ticks)

// Variables del scheduler
static process_t process_table[MAX_PROCESSES];
static int current_process = -1;
static int total_processes = 0;

// Inicializa el scheduler
void scheduler_init() {
    total_processes = 0;
    current_process = -1;

    // Registra el manejador para interrupciones del temporizador
    irq_register_handler(0, scheduler_tick);
    printf("[SCHEDULER] Inicializado con Round Robin (quantum = %d).\n", TIME_QUANTUM);
}

// Agrega un nuevo proceso al scheduler
void scheduler_add_process(const char* name) {
    if (total_processes >= MAX_PROCESSES) {
        printf("[SCHEDULER] No se pueden agregar más procesos.\n");
        return;
    }
    process_table[total_processes].pid = total_processes;
    snprintf(process_table[total_processes].name, sizeof(process_table[total_processes].name), "%s", name);
    process_table[total_processes].state = READY;
    total_processes++;
    printf("[SCHEDULER] Proceso '%s' agregado con PID %d.\n", name, total_processes - 1);
}

// Cambia al siguiente proceso en la cola
void scheduler_schedule() {
    if (total_processes == 0) {
        printf("[SCHEDULER] No hay procesos para planificar.\n");
        return;
    }

    // Encuentra el siguiente proceso listo
    int next_process = (current_process + 1) % total_processes;
    while (process_table[next_process].state != READY) {
        next_process = (next_process + 1) % total_processes;
        if (next_process == current_process) {
            printf("[SCHEDULER] No hay procesos listos para ejecutar.\n");
            return;
        }
    }

    // Cambia al proceso encontrado
    current_process = next_process;
    printf("[SCHEDULER] Cambiando al proceso PID %d ('%s').\n",
           process_table[current_process].pid,
           process_table[current_process].name);
}

// Manejador para la interrupción del temporizador
void scheduler_tick() {
    printf("[TICK] Interrupción del temporizador recibida. Planificando...\n");
    scheduler_schedule();
}

// Actualización del estado de procesos en E/S
void scheduler_handle_io(int irq) {
    if (current_process == -1) {
        printf("[SCHEDULER] No hay proceso en ejecución para manejar E/S.\n");
        return;
    }

    if (irq == 1) { // Lectura completada
        process_table[current_process].state = READY;
        printf("[SCHEDULER] Proceso PID %d ('%s') listo tras completar lectura.\n",
               current_process,
               process_table[current_process].name);
    } else if (irq == 2) { // Escritura completada
        process_table[current_process].state = READY;
        printf("[SCHEDULER] Proceso PID %d ('%s') listo tras completar escritura.\n",
               current_process,
               process_table[current_process].name);
    }

    // Planificar el siguiente proceso
    scheduler_schedule();
}