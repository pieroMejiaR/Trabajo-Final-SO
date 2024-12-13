import tkinter as tk
from tkinter import simpledialog
import os
from scheduler import ProcessScheduler
from file_system import FileSystem
from memory_manager import MemoryManager
from process import Process

# Instancias globales
scheduler = ProcessScheduler()
memory_manager = MemoryManager(memory_size=50, page_size=4)
file_system = FileSystem()

# Colores y estilos modernos
COLORS = {
    'primary': "#4A90E2",    # Azul principal
    'secondary': "#2ECC71",  # Verde secundario
    'background': "#F5F6FA", # Fondo claro
    'text': "#2C3E50",      # Texto oscuro
    'accent': "#E74C3C",    # Acento rojo
    'text_area': "#FFFFFF"   # Fondo áreas de texto
}
# Colores y estilos
BG_COLOR = "#ffffff"  # Fondo principal
BTN_BG_COLOR = "#61afef"  # Fondo de botones
BTN_FG_COLOR = "#ffffff"  # Texto de botones
TEXT_BG_COLOR = "#21252b"  # Fondo de áreas de texto
TEXT_FG_COLOR = "#abb2bf"  # Texto de áreas de texto

# Configuración de estilos
STYLES = {
    'title': ("Segoe UI", 16, "bold"),
    'button': ("Segoe UI", 11),
    'text': ("Consolas", 11),
    'label': ("Segoe UI", 12)
}

# Estilos de botones
BUTTON_STYLE = {
    'bg': COLORS['primary'],
    'fg': 'white',
    'font': STYLES['button'],
    'relief': 'flat',
    'padx': 15,
    'pady': 8,
    'borderwidth': 0,
    'cursor': 'hand2'  # Cursor tipo mano
}

def create_styled_button(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, **BUTTON_STYLE)
    btn.bind('<Enter>', lambda e: btn.configure(bg=COLORS['secondary']))
    btn.bind('<Leave>', lambda e: btn.configure(bg=COLORS['primary']))
    return btn

# Funciones de Planificación de Procesos
def open_process_scheduler():
    scheduler_window = tk.Toplevel()
    scheduler_window.title("Planificación de Procesos")
    scheduler_window.geometry("700x600")
    scheduler_window.configure(bg=COLORS['background'])
    
    # Frame principal
    main_frame = tk.Frame(scheduler_window, bg=COLORS['background'])
    main_frame.pack(padx=20, pady=20, fill='both', expand=True)

    # Título
    title_label = tk.Label(main_frame, 
                          text="Planificación de Procesos",
                          font=STYLES['title'],
                          bg=COLORS['background'],
                          fg=COLORS['text'])
    title_label.pack(pady=(0,20))

    # Área de texto con scroll
    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')
    
    text_widget = tk.Text(text_frame,
                         height=10,
                         width=60,
                         font=STYLES['text'],
                         bg=COLORS['text_area'],
                         fg=COLORS['text'],
                         wrap='word',
                         borderwidth=1,
                         relief='solid')
    text_widget.pack(side='left', fill='both', expand=True)
    
    scrollbar.config(command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Frame para botones
    button_frame = tk.Frame(main_frame, bg=COLORS['background'])
    button_frame.pack(pady=20)

    def actualizar_estado_memoria():
        memoria_estado = "Estado de Memoria:\n"
        for i, proceso in enumerate(memory_manager.pages):
            memoria_estado += f"Frame {i}: {'Vacío' if proceso == -1 else f'Proceso {proceso}'}\n"
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, memoria_estado)

    def add_process():
        process_id = simpledialog.askstring("Agregar Proceso", "Id de proceso:")
        name = simpledialog.askstring("Agregar Proceso", "Nombre del proceso:")
        burst_time = simpledialog.askinteger("Agregar Proceso", "Tiempo de ráfaga:")
        priority = simpledialog.askinteger("Agregar Proceso", "Prioridad:")
        process_size = simpledialog.askinteger("Agregar Proceso", "Tamaño del proceso (en KB):")

        if name and burst_time and priority is not None and process_size is not None:
            new_process = Process(process_id, process_size, name, burst_time, priority)

            if memory_manager.allocate(new_process):
                scheduler.add_process(process_id, process_size, name, burst_time, priority)
                text_widget.insert(tk.END, f"✓ Proceso '{name}' agregado exitosamente\n")
                text_widget.insert(tk.END, f"  → ID: {process_id}\n")
                text_widget.insert(tk.END, f"  → Tamaño: {process_size} KB\n")
                text_widget.insert(tk.END, f"  → Tiempo de ráfaga: {burst_time}\n")
                text_widget.insert(tk.END, f"  → Prioridad: {priority}\n\n")
            else:
                # Manejar el fallo de memoria utilizando FIFO
                evicted_process_id = memory_manager.handle_page_fault_fifo(new_process)
                if memory_manager.allocate(new_process):
                    scheduler.add_process(process_id, process_size, name, burst_time, priority)
                    scheduler.remove_process(evicted_process_id)
                    text_widget.insert(tk.END, f"✓ Proceso '{name}' agregado después de liberar memoria con FIFO\n")
                    text_widget.insert(tk.END, f"  → ID: {process_id}\n")
                    text_widget.insert(tk.END, f"  → Tamaño: {process_size} KB\n")
                    text_widget.insert(tk.END, f"  → Tiempo de ráfaga: {burst_time}\n")
                    text_widget.insert(tk.END, f"  → Prioridad: {priority}\n\n")
                else:
                    text_widget.insert(tk.END, f"❌ Error: Memoria insuficiente para '{name}' incluso después de liberar espacio con FIFO\n\n")
        else:
            text_widget.insert(tk.END, "❌ Error: Datos inválidos para el proceso\n\n")

    
    def execute_fifo():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "📊 Planificación FIFO:\n" + "="*40 + "\n\n")
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        for process in scheduler.processes:
            wait_time = current_time
            turnaround_time = wait_time + process.burst_time
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time
            text_widget.insert(tk.END, f"→ Proceso {process.name}:\n")
            text_widget.insert(tk.END, f"  • Tiempo de espera: {wait_time}\n")
            text_widget.insert(tk.END, f"  • Tiempo de retorno: {turnaround_time}\n\n")
            current_time += process.burst_time

        n = len(scheduler.processes)
        if n > 0:
            text_widget.insert(tk.END, "="*40 + "\n")
            text_widget.insert(tk.END, f"📈 Promedios:\n")
            text_widget.insert(tk.END, f"  • Espera: {total_wait_time/n:.2f}\n")
            text_widget.insert(tk.END, f"  • Retorno: {total_turnaround_time/n:.2f}\n")

    def execute_sjf():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "📊 Planificación SJF:\n" + "="*40 + "\n\n")
        sorted_processes = sorted(scheduler.processes, key=lambda x: x.burst_time)
        total_wait_time = 0
        total_turnaround_time = 0
        current_time = 0

        for process in sorted_processes:
            wait_time = current_time
            turnaround_time = wait_time + process.burst_time
            total_wait_time += wait_time
            total_turnaround_time += turnaround_time
            text_widget.insert(tk.END, f"→ Proceso {process.name}:\n")
            text_widget.insert(tk.END, f"  • Tiempo de espera: {wait_time}\n")
            text_widget.insert(tk.END, f"  • Tiempo de retorno: {turnaround_time}\n\n")
            current_time += process.burst_time

        n = len(sorted_processes)
        if n > 0:
            text_widget.insert(tk.END, "="*40 + "\n")
            text_widget.insert(tk.END, f"📈 Promedios:\n")
            text_widget.insert(tk.END, f"  • Espera: {total_wait_time/n:.2f}\n")
            text_widget.insert(tk.END, f"  • Retorno: {total_turnaround_time/n:.2f}\n")

    def execute_rr():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Planificación Round Robin:\n")
        quantum = simpledialog.askinteger("Round Robin", "Quantum:")
        
        if quantum:
            from collections import deque
            # Crear copias independientes de los procesos
            process_copies = [
                {
                    "name": process.name,
                    "burst_time": process.burst_time,
                    "original_burst_time": process.burst_time,
                    "id": process.process_id
                } for process in scheduler.processes
            ]
            queue = deque(process_copies)
            
            current_time = 0

            while queue:
                process = queue.popleft()
                if process["burst_time"] > quantum:
                    current_time += quantum
                    process["burst_time"] -= quantum
                    queue.append(process)
                else:
                    current_time += process["burst_time"]
                    process["burst_time"] = 0
                    resultado = (
                        f"Proceso {process['name']} (ID: {process['id']}) -> "
                        f"Completado en el tiempo: {current_time}\n"
                    )
                    text_widget.insert(tk.END, resultado)
        else:
            text_widget.insert(tk.END, "Error: Quantum inválido.\n")

    # Botones con nuevo estilo
    add_btn = create_styled_button(button_frame, "Agregar Proceso", add_process)
    add_btn.pack(side='left', padx=5)
    
    fifo_btn = create_styled_button(button_frame, "Ejecutar RR", execute_rr)
    fifo_btn.pack(side='left', padx=5)

    fifo_btn = create_styled_button(button_frame, "Ejecutar FIFO", execute_fifo)
    fifo_btn.pack(side='left', padx=5)
    
    sjf_btn = create_styled_button(button_frame, "Ejecutar SJF", execute_sjf)
    sjf_btn.pack(side='left', padx=5)
    
    memory_btn = create_styled_button(button_frame, "Ver Estado Memoria", actualizar_estado_memoria)
    memory_btn.pack(side='left', padx=5)

def open_memory_manager():
    memory_window = tk.Toplevel()
    memory_window.title("Administración de Memoria")
    memory_window.geometry("400x600")
    memory_window.configure(bg=COLORS['background'])

    # Frame principal
    main_frame = tk.Frame(memory_window, bg=COLORS['background'])
    main_frame.pack(padx=20, pady=20, fill='both', expand=True)

     # Título
    title_label = tk.Label(main_frame, 
                          text="Administración de Memoria",
                          font=STYLES['title'],
                          bg=COLORS['background'],
                          fg=COLORS['text'])
    title_label.pack(pady=(0,20))

    # Widget de texto para mostrar el estado de memoria
    # Área de texto con scroll
    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')
    
    text_widget = tk.Text(text_frame,
                         height=20,
                         width=20,
                         font=STYLES['text'],
                         bg=COLORS['text_area'],
                         fg=COLORS['text'],
                         wrap='word',
                         borderwidth=1,
                         relief='solid')
    text_widget.pack(side='left', fill='both', expand=True)
    
    scrollbar.config(command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    # Frame para botones
    button_frame = tk.Frame(main_frame, bg=COLORS['background'])
    button_frame.pack(pady=20)
    # Función para mostrar el estado de la memoria
    def show_memory_state():
        text_widget.delete(1.0, tk.END)  # Limpia el área de texto
        text_widget.insert(tk.END, "Estado de Memoria:\n" + "=" * 40 + "\n")

        for i, process_id in enumerate(memory_manager.pages):
            if process_id == -1:
                state = f"Frame {i}: Vacío\n"
            else:
                # Busca el nombre del proceso asociado al ID
                process = next((p for p in scheduler.processes if p.process_id == process_id), None)
                state = f"Frame {i}: Proceso {process.name if process else 'Desconocido'}\n"

            text_widget.insert(tk.END, state)

        text_widget.insert(tk.END, "=" * 40 + "\n")
    
    # Botones
    add_btn = create_styled_button(button_frame, "Mostrar Estado de Memoria", show_memory_state)
    add_btn.pack(side='left', padx=5)
    add_btn = create_styled_button(button_frame, "Cerrar", memory_window.destroy)
    add_btn.pack(side='left', padx=5)
"""manejo de archivos"""
def open_file_system():
    fs_window = tk.Toplevel(bg=COLORS['background'])
    fs_window.title("Sistema de Archivos")
    fs_window.geometry("600x700")
    fs_window.resizable(False, False)

    # Main container frame
    main_frame = tk.Frame(fs_window, bg=COLORS['background'])
    main_frame.pack(padx=20, pady=20, fill='both', expand=True)

    # Title
    title_label = tk.Label(main_frame, 
                           text="Sistema de Archivos (Físico)", 
                           font=STYLES['title'], 
                           bg=COLORS['background'], 
                           fg=COLORS['text'])
    title_label.pack(pady=(0, 20))

    # Text area with scroll
    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')
    
    text_widget = tk.Text(text_frame,
                          height=20,
                          width=60,
                          font=STYLES['text'],
                          bg=COLORS['text_area'],
                          fg=COLORS['text'],
                          wrap='word',
                          borderwidth=1,
                          relief='solid')
    text_widget.pack(side='left', fill='both', expand=True)
    
    scrollbar.config(command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Button frame
    button_frame = tk.Frame(main_frame, bg=COLORS['background'])
    button_frame.pack(pady=20)

    # File system operations
    def safe_operation(operation):
        try:
            operation()
        except Exception as e:
            text_widget.insert(tk.END, f"❌ Error: {str(e)}\n")

    def create_directory_safe():
        name = simpledialog.askstring("Crear Directorio", "Nombre del directorio:")
        if name:
            safe_operation(lambda: os.makedirs(name, exist_ok=False))
            text_widget.insert(tk.END, f"✓ Directorio '{name}' creado.\n")

    def create_file_safe():
        name = simpledialog.askstring("Crear Archivo", "Nombre del archivo:")
        if name:
            safe_operation(lambda: open(name, 'x').close())
            text_widget.insert(tk.END, f"✓ Archivo '{name}' creado.\n")

    def write_file_safe():
        name = simpledialog.askstring("Escribir en Archivo", "Nombre del archivo:")
        if name:
            content = simpledialog.askstring("Escribir en Archivo", "Contenido:")
            if content is not None:
                safe_operation(lambda: open(name, 'w').write(content))
                text_widget.insert(tk.END, f"✓ Contenido escrito en '{name}'.\n")

    def read_file_safe():
        name = simpledialog.askstring("Leer Archivo", "Nombre del archivo:")
        if name:
            def read_operation():
                with open(name, 'r') as f:
                    content = f.read()
                text_widget.insert(tk.END, f"📄 Contenido de '{name}':\n{content}\n")
            
            safe_operation(read_operation)

    def delete_file_or_dir_safe():
        name = simpledialog.askstring("Eliminar", "Nombre del archivo/directorio:")
        if name:
            def delete_operation():
                if os.path.isdir(name):
                    os.rmdir(name)
                else:
                    os.remove(name)
            
            safe_operation(delete_operation)
            text_widget.insert(tk.END, f"✓ '{name}' eliminado correctamente.\n")

    def list_contents_safe():
        def list_operation():
            contents = os.listdir(".")
            text_widget.insert(tk.END, "📁 Contenido del directorio:\n")
            for item in contents:
                text_widget.insert(tk.END, f"  • {item}\n")
        
        safe_operation(list_operation)

    # Create styled buttons for file operations
    buttons_config = [
        ("Crear Directorio", create_directory_safe),
        ("Crear Archivo", create_file_safe),
        ("Escribir en Archivo", write_file_safe),
        ("Leer Archivo", read_file_safe),
        ("Eliminar", delete_file_or_dir_safe),
        ("Listar Contenidos", list_contents_safe),
        ("Cerrar", fs_window.destroy)
    ]

    for text, command in buttons_config:
        btn = create_styled_button(button_frame, text, command)
        btn.pack(side='left', padx=5, pady=5)
"""fin"""

# Crear ventana principal
root = tk.Tk()
root.title("Sistema Operativo Simulado")
root.geometry("500x400")
root.configure(bg=COLORS['background'])
# Forzar a las ventanas emergentes a estar al frente


# Frame principal
main_frame = tk.Frame(root, bg=COLORS['background'])
main_frame.pack(expand=True)

# Título principal
title_label = tk.Label(main_frame,
                      text="Sistema Operativo Simplificado",
                      font=STYLES['title'],
                      bg=COLORS['background'],
                      fg=COLORS['text'])
title_label.pack(pady=20)
def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)
# Botón principal
scheduler_btn = create_styled_button(main_frame, "Abrir Planificador de Procesos", open_process_scheduler)
memory_btn = create_styled_button(main_frame, "Administración de Memoria", open_memory_manager)
file_btn = create_styled_button(main_frame, "Sistema de Archivos (Físico)", open_file_system)
scheduler_btn.pack(pady=10)
memory_btn.pack(pady=10)
file_btn.pack(pady=10)
root.mainloop()