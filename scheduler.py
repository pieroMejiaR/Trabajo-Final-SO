from process import Process

class ProcessScheduler:
    def __init__(self):
        self.processes = []

    def add_process(self, process_id, process_size, name, burst_time, priority):
        """Agrega un nuevo proceso a la lista."""
        process = Process(process_id, process_size, name, burst_time, priority)
        self.processes.append(process)

    def fifo(self):
        """Planificación FIFO: procesa en orden de llegada."""
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        print("\nFIFO Scheduling:")
        for process in self.processes:
            wait_time = current_time
            turnaround_time = wait_time + process.burst_time
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time

            print(f"Process {process.name} -> Wait Time: {wait_time}, Turnaround Time: {turnaround_time}")
            current_time += process.burst_time

        n = len(self.processes)
        print(f"Average Wait Time: {total_wait_time / n}, Average Turnaround Time: {total_turnaround_time / n}")

    def sjf(self):
        """Planificación SJF: procesa el de menor tiempo de ráfaga."""
        sorted_processes = sorted(self.processes, key=lambda p: p.burst_time)
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        print("\nSJF Scheduling:")
        for process in sorted_processes:
            wait_time = current_time
            turnaround_time = wait_time + process.burst_time
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time

            print(f"Process {process.name} -> Wait Time: {wait_time}, Turnaround Time: {turnaround_time}")
            current_time += process.burst_time

        n = len(sorted_processes)
        print(f"Average Wait Time: {total_wait_time / n}, Average Turnaround Time: {total_turnaround_time / n}")

    def round_robin(self, quantum):
        """Planificación Round Robin."""
        from collections import deque
        queue = deque(self.processes)
        current_time = 0
        total_wait_time = 0
        total_turnaround_time = 0

        print("\nRound Robin Scheduling:")
        while queue:
            process = queue.popleft()
            if process.burst_time > quantum:
                current_time += quantum
                process.burst_time -= quantum
                queue.append(process)
            else:
                current_time += process.burst_time
                wait_time = current_time - process.burst_time
                turnaround_time = current_time
                total_wait_time += wait_time
                total_turnaround_time += turnaround_time

                print(f"Process {process.name} -> Wait Time: {wait_time}, Turnaround Time: {turnaround_time}")

        n = len(self.processes)
        print(f"Average Wait Time: {total_wait_time / n}, Average Turnaround Time: {total_turnaround_time / n}")

    def remove_process(self, process_id):
        """Elimina un proceso del scheduler y libera su memoria."""
        # Busca el proceso en la lista
        process = next((p for p in self.processes if p.process_id == process_id), None)
        if process:
            # Elimina el proceso de la lista
            self.processes.remove(process)
            print(f"Proceso {process.name} eliminado exitosamente.")
            return True
        else:
            print(f"Proceso con ID {process_id} no encontrado.")
            return False