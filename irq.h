#ifndef IRQ_H
#define IRQ_H

// Definimos el tipo de función para un manejador de interrupciones
typedef void (*irq_handler_t)(void);

// Funciones básicas del sistema de interrupciones
void irq_init();                      // Inicializa el sistema
void irq_register_handler(int irq, irq_handler_t handler); // Registra un manejador
void irq_handle(int irq);             // Maneja una interrupción simulada

#endif
