#include "irq.h"
#include <stdio.h>

#define MAX_INTERRUPTS 16 // Reducimos a 16 para simplificar

// Tabla de manejadores de interrupciones
static irq_handler_t irq_handlers[MAX_INTERRUPTS];

// Simulación de datos para E/S
static char io_buffer[256]; // Buffer para leer/escribir datos

// Inicializa el sistema de interrupciones
void irq_init() {
    for (int i = 0; i < MAX_INTERRUPTS; i++) {
        irq_handlers[i] = NULL; // Inicialmente, ninguna interrupción tiene manejador
    }
    printf("[IRQ] Sistema de interrupciones inicializado.\n");
}

// Registra un manejador para una interrupción específica
void irq_register_handler(int irq, irq_handler_t handler) {
    if (irq < 0 || irq >= MAX_INTERRUPTS) {
        printf("[IRQ] Error: IRQ %d está fuera de rango.\n", irq);
        return;
    }
    irq_handlers[irq] = handler;
    printf("[IRQ] Manejador registrado para IRQ %d.\n", irq);
}

// Maneja una interrupción simulada
void irq_handle(int irq) {
    if (irq < 0 || irq >= MAX_INTERRUPTS || irq_handlers[irq] == NULL) {
        printf("[IRQ] Interrupción %d no manejada.\n", irq);
        return;
    }
    printf("[IRQ] Manejando interrupción %d...\n", irq);
    irq_handlers[irq](); // Llama al manejador registrado
}

// Manejador de lectura
void io_read_handler() {
    printf("[IO] Leyendo datos desde el dispositivo...\n");
    snprintf(io_buffer, sizeof(io_buffer), "Datos simulados leídos del dispositivo");
    printf("[IO] Datos leídos: %s\n", io_buffer);
}

// Manejador de escritura
void io_write_handler() {
    printf("[IO] Escribiendo datos en el dispositivo...\n");
    printf("[IO] Escribiendo: %s\n", io_buffer);
    printf("[IO] Escribiendo completado.\n");
}

// Inicialización de interrupciones de E/S
void io_init() {
    irq_register_handler(1, io_read_handler);  // IRQ 1 para lectura
    irq_register_handler(2, io_write_handler); // IRQ 2 para escritura
    printf("[IO] Manejo de E/S inicializado.\n");
}
