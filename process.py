class Process:
    def __init__(self, process_id, process_size, name, burst_time, priority):
        """
        Initialize a Process object.

        :param process_id: Unique identifier for the process (int).
        :param process_size: Size of the process in memory (int).
        :param name: Name of the process (str).
        :param burst_time: CPU burst time required for the process (int).
        :param priority: Priority level of the process (int).
        """
        self.process_id = process_id
        self.process_size = process_size
        self.name = name
        self.burst_time = burst_time
        self.priority = priority

    def __str__(self):
        """Returns a string representation of the process."""
        return (f"Process ID: {self.process_id}\n"
                f"Name: {self.name}\n"
                f"Size: {self.process_size} KB\n"
                f"Burst Time: {self.burst_time} ms\n"
                f"Priority: {self.priority}")
