#ifndef OS_EVENT_H
#define OS_EVENT_H

#include "process.h"

// Estructura del evento del sistema
typedef struct os_event {
    int completed;               // 0: No completado, 1: Completado
    process_t* waiting_process;  // Proceso esperando este evento
} os_event_t;

// Funciones del evento
os_event_t* create_event();
void trigger_event(os_event_t* event);
void wait_for_event(os_event_t* event, process_t* process);

#endif
