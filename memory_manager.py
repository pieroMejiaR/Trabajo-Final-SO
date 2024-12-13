# Administración de Memoria
class MemoryManager:
    def __init__(self, memory_size, page_size):
        self.memory_size = memory_size
        self.page_size = page_size
        self.pages = [-1] * (memory_size // page_size)
        self.page_queue = []  # Para FIFO
        self.page_access = {}  # Para LRU

    def allocate(self, process_id, process_size):
        """Asigna memoria para un proceso si hay suficiente espacio."""
        num_pages_needed = (process_size + self.page_size - 1) // self.page_size
        allocated_pages = 0

        for i in range(len(self.pages)):
            if self.pages[i] == -1:  # Si el marco está vacío
                self.pages[i] = process_id
                self.page_queue.append(process_id)
                allocated_pages += 1
                if allocated_pages == num_pages_needed:
                    return True  # Asignación exitosa

        # Si no hay suficiente espacio, revertimos los cambios
        for i in range(len(self.pages)):
            if self.pages[i] == process_id:
                self.pages[i] = -1
        return False  # No hay espacio suficiente

    def load_page(self, process_id, page_number):
        """Carga una página en memoria con manejo de reemplazo."""
        if process_id in self.pages:
            print(f"Page {page_number} of Process {process_id} already in memory.")
            return

        if -1 in self.pages:
            # Espacio disponible
            free_index = self.pages.index(-1)
            self.pages[free_index] = process_id
            self.page_queue.append(process_id)
            self.page_access[process_id] = free_index
            print(f"Loaded Page {page_number} of Process {process_id} into Frame {free_index}.")
        else:
            # Reemplazo FIFO
            evicted = self.page_queue.pop(0)
            evict_index = self.pages.index(evicted)
            self.pages[evict_index] = process_id
            self.page_queue.append(process_id)
            self.page_access[process_id] = evict_index
            print(f"Page {page_number} of Process {evicted} evicted. Loaded Process {process_id}.")

    def display_memory(self):
        """Muestra el estado actual de la memoria."""
        print("\nMemory State:")
        for i, process in enumerate(self.pages):
            print(f"Frame {i}: {'Empty' if process == -1 else f'Process {process}'}")