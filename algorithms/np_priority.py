import bisect
from collections import deque

from algorithms.base_algorithm import BaseAlgorithm


class NonPreemptivePriority(BaseAlgorithm):
    process_compare_prop = 'priority'

    def __init__(self, processes):
        processes.sort(key=lambda process: (process.arrival_time, process.priority))
        super().__init__(processes)
        self.ready_queue = deque([])
        self.running_process = None
        self.time = 0
        self.idle_time = 0

    def run(self):
        """
        Run the algorithm.
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

        while self.processes or self.ready_queue or self.running_process:

            if self.running_process and self.running_process.remaining_time == 0:
                self.running_process.end_time = self.time
                self.running_process.turnaround_time = self.running_process.end_time - self.running_process.arrival_time
                self.running_process.waiting_time = self.running_process.turnaround_time - self.running_process.burst_time
                executed_processes.append(self.running_process)
                self.running_process = None

                if not self.processes and not self.ready_queue:
                    break

            arrived_processes = self.get_arrived_processes()
            if arrived_processes:
                highest_priority_process = min(arrived_processes, key=lambda process: process.priority)
                if self.running_process is None:
                    self.running_process = highest_priority_process
                    self.running_process.start_time = self.time

                for _ in range(len(arrived_processes)):
                    self.processes.popleft()

                if self.running_process in arrived_processes:
                    arrived_processes.remove(self.running_process)
                for process in arrived_processes:
                    self.append_to_ready_queue(process)
                arrived_processes.clear()

            # If no process is running, then pick the process from ready queue
            if self.running_process is None and self.ready_queue:
                self.running_process = self.ready_queue.popleft()
                self.running_process.start_time = self.running_process.start_time or self.time

            # If process is running, then get next important time and update the time
            next_time = self.get_next_important_time()
            if self.running_process:
                self.running_process.remaining_time -= next_time - self.time
            else:
                self.idle_time += next_time - self.time
            self.time = next_time

        # Calculate total time, CPU utilization, throughput, average waiting time, average turnaround time,
        # average response time
        total_time = self.time
        cpu_utilization = (total_time - self.idle_time) / total_time
        throughput = len(executed_processes) / total_time
        average_waiting_time = sum(process.waiting_time for process in executed_processes) / len(executed_processes)
        average_turnaround_time = sum(process.turnaround_time for process in executed_processes) / len(
            executed_processes)
        average_response_time = sum(process.start_time - process.arrival_time for process in executed_processes) / len(
            executed_processes)
        return {
            "processes": executed_processes,
            "total_time": total_time,
            "cpu_utilization": cpu_utilization,
            "throughput": throughput,
            "average_waiting_time": average_waiting_time,
            "average_turnaround_time": average_turnaround_time,
            "average_response_time": average_response_time
        }

    def get_arrived_processes(self):
        """
        Get processes which arrived at current time.
        :return: list of arrived processes
        """
        arrived_processes = []
        for process in self.processes:
            if process.arrival_time == self.time:
                arrived_processes.append(process)
            else:
                break
        return arrived_processes

    def append_to_ready_queue(self, process):
        """
        Append process to ready queue based on priority.
        :param process: process to be appended
        """
        bisect.insort(self.ready_queue, process)

    def get_next_important_time(self):
        """
        Find next point of time that need a decision
        :return: Int
        """
        if self.running_process is not None:
            if not self.processes:
                return max(self.time + self.running_process.remaining_time, self.time)

            return min(
                self.time + (self.running_process.remaining_time or 1),
                self.processes[0].arrival_time
            )

        if self.ready_queue:
            return self.time + 1

        if self.processes:
            return self.processes[0].arrival_time

        return self.time + 1

    def remove_processes(self, processes):
        """
        Remove processes from processes list
        :param processes: list of processes
        :return: None
        """
        for process in processes:
            self.processes.remove(process)
