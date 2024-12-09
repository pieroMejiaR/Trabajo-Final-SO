#ifndef SCHEDULER_H
#define SCHEDULER_H
#include "process.h"

#define MAX_PROCESSES 10 // Número máximo de procesos permitidos

// Funciones del scheduler
void io_init(void);
void scheduler_init();
void scheduler_add_process(const char* name);
void scheduler_schedule();
void scheduler_tick(); // Manejador para interrupciones del temporizador

#endif
