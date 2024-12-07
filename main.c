#include "irq.h"
#include "scheduler.h"
#include <stdio.h>

int main() {
    // Inicializa el sistema de interrupciones
    irq_init();
    io_init();

    // Inicializa el scheduler
    scheduler_init();

    // Agrega procesos
    scheduler_add_process("Proceso 1");
    scheduler_add_process("Proceso 2");
    scheduler_add_process("Proceso 3");

    // Simula ticks del temporizador y operaciones de E/S
    for (int i = 0; i < 10; i++) {
        if (i == 2) {
            printf("[MAIN] Proceso actual solicita operación de lectura.\n");
            irq_handle(1); // Simula IRQ de lectura
        } else if (i == 5) {
            printf("[MAIN] Proceso actual solicita operación de escritura.\n");
            irq_handle(2); // Simula IRQ de escritura
        } else {
            printf("[MAIN] Simulando tick %d...\n", i);
            irq_handle(0); // Simula interrupción del temporizador
        }
    }

    return 0;
}
