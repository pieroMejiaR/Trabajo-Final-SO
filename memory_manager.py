# Administración de Memoria
from process import Process

class MemoryManager:
    def __init__(self, memory_size, page_size):
        self.memory_size = memory_size
        self.page_size = page_size
        self.pages = [-1] * (memory_size // page_size)
        self.page_queue = []  # Para FIFO

    def allocate(self, process: Process):
        """Asigna memoria para un proceso si hay suficiente espacio."""
        num_pages_needed = (process.process_size + self.page_size - 1) // self.page_size
        allocated_pages = 0

        for i in range(len(self.pages)):
            if self.pages[i] == -1:  # Si el marco está vacío
                self.pages[i] = process.process_id
                self.page_queue.append(process.process_id)
                allocated_pages += 1
                if allocated_pages == num_pages_needed:
                    print(f"Proceso {process.name} asignado exitosamente.")
                    return True  # Asignación exitosa

        # Si no hay suficiente espacio, revertimos los cambios
        for i in range(len(self.pages)):
            if self.pages[i] == process.process_id:
                self.pages[i] = -1
        print(f"No hay suficiente espacio para el proceso {process.name}.")
        return False  # No hay espacio suficiente

    def load_page(self, process: Process, page_number):
        """Carga una página en memoria con manejo de reemplazo."""
        if process.process_id in self.pages:
            print(f"Page {page_number} of Process {process.name} already in memory.")
            return

        if -1 in self.pages:
            # Espacio disponible
            free_index = self.pages.index(-1)
            self.pages[free_index] = process.process_id
            self.page_queue.append(process.process_id)
            self.page_access[process.process_id] = free_index
            print(f"Loaded Page {page_number} of Process {process.name} into Frame {free_index}.")
        else:
            # Reemplazo FIFO
            self.handle_page_fault_fifo(process, page_number)

    def handle_page_fault_fifo(self, process: Process):
        """
        Maneja un fallo de página utilizando la estrategia FIFO.
        Libera espacio en memoria para un proceso completo si es necesario.
        """
        num_pages_needed = (process.process_size + self.page_size - 1) // self.page_size

        while num_pages_needed > self.pages.count(-1):
            # No hay suficientes marcos libres, liberar espacio con FIFO
            evicted_process_id = self.page_queue.pop(0)
            for i in range(len(self.pages)):
                if self.pages[i] == evicted_process_id:
                    self.pages[i] = -1  # Libera el marco

            print(f"Proceso {evicted_process_id} expulsado para liberar espacio.")
            return evicted_process_id

        print(f"Espacio liberado para el proceso {process.name}.")