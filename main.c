#include "irq.h"
#include "scheduler.h"
#include "gestorMemoria.h"
#include <stdio.h>
#include <stdlib.h>

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

    //PRUEBA DE GESTOR DE MEMORIA

    const int TAMANO_MEMORIA = 64;  // En KB
    const int TAMANO_PAGINA = 4;   // En KB

    GestorMemoria* gestor = inicializar_gestor(TAMANO_MEMORIA, TAMANO_PAGINA);

    // Crear procesos
    process_t* proceso1 = create_process(1, "Proceso1");
    process_t* proceso2 = create_process(2, "Proceso2");
    process_t* proceso3 = create_process(3, "Proceso3");

    // Simular asignaciones
    asignar_memoria(gestor, proceso1, 10); // Proceso 1 necesita 10 KB
    asignar_memoria(gestor, proceso2, 20); // Proceso 2 necesita 20 KB
    mostrar_estado_memoria(gestor);

    // Liberar memoria del proceso 1
    liberar_memoria(gestor, proceso1);
    mostrar_estado_memoria(gestor);

    // Asignar memoria al proceso 3
    asignar_memoria(gestor, proceso3, 15);
    mostrar_estado_memoria(gestor);

    // Liberar memoria dinámica
    liberar_memoria(gestor, proceso2);
    liberar_memoria(gestor, proceso3);

    free(proceso1);
    free(proceso2);
    free(proceso3);

    liberar_gestor(gestor);

    return 0;
}
