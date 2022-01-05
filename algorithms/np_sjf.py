from algorithms.base_algorithm import BaseAlgorithm


class NonPreemptiveSJF(BaseAlgorithm):
    def __init__(self, processes):
        super().__init__(processes)
        self.time = 0.0
        self.idle_time = 0.0

    def run(self):
        """
        Schedule the processes using Non-Preemptive Shortest Job First
        algorithm and calculate following information.
        :return: {
            "processes": list of executed processes,
            "time": total time of execution,
            "cpu_utilization": total CPU utilization,
            "throughput": total throughput,
            "average_waiting_time": average waiting time,
            "average_turnaround_time": average turnaround time,
            "average_response_time": average response time
        }
        """
        executed_processes = []
        while self.processes:
            # Get the process with the shortest remaining time
            shortest_process = self.get_shortest_process()
            if shortest_process:
                # Execute the process
                shortest_process.start_time = self.time
                self.time += shortest_process.burst_time
                shortest_process.end_time = self.time
                shortest_process.turnaround_time = shortest_process.end_time - shortest_process.arrival_time
                shortest_process.waiting_time = shortest_process.turnaround_time - shortest_process.burst_time
                self.processes.remove(shortest_process)
                executed_processes.append(shortest_process)
            else:
                # Idle time
                self.idle_time += 1
                self.time += 1

        try:
            avg_waiting_time = sum([process.waiting_time for process in executed_processes]) / len(executed_processes)
        except ZeroDivisionError:
            avg_waiting_time = 0

        try:
            avg_turnaround_time = sum([process.turnaround_time for process in executed_processes]) / len(
                executed_processes)
        except ZeroDivisionError:
            avg_turnaround_time = 0

        try:
            avg_response_time = sum([process.start_time for process in executed_processes]) / len(executed_processes)
        except ZeroDivisionError:
            avg_response_time = 0

        return {
            "processes": executed_processes,
            "total_time": self.time,
            "cpu_utilization": (self.time - self.idle_time) / self.time,
            "throughput": len(executed_processes) / self.time,
            "average_waiting_time": avg_waiting_time,
            "average_turnaround_time": avg_turnaround_time,
            "average_response_time": avg_response_time
        }

    def get_shortest_process(self):
        """
        Get the process with the shortest remaining time among arrive processes.
        :return: Process
        """
        min_burst_time = float("inf")
        shortest_process = None
        for process in self.processes:
            if process.arrival_time > self.time:
                break
            if process.burst_time < min_burst_time:
                min_burst_time = process.burst_time
                shortest_process = process
        return shortest_process
