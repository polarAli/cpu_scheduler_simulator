from base_algorithm import BaseAlgorithm
from state import State


class FIFO(BaseAlgorithm):
    """
    FIFO algorithm for scheduling processes
    """

    def __init__(self, processes):
        super().__init__(processes)
        self.processes = processes
        self.processes.sort(key=lambda x: x.arrival_time)

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
        time = 0
        processes = []
        cpu_idle_time = 0
        while self.processes:
            process = self.processes.pop(0)

            # If we have idle time, add it to the CPU idle time
            if process.arrival_time > time:
                cpu_idle_time += process.arrival_time - time
                time = process.arrival_time

            # Calculate the response time
            process.response_time = time - process.arrival_time
            # Calculate the turnaround time
            process.turnaround_time = process.response_time + process.burst_time
            # Run the process
            process.start_time = time
            time += process.burst_time
            process.end_time = time
            # Change the state of the process
            process.state = State.EXECUTED
            processes.append(process)

        # Calculate CPU utilization
        cpu_utilization = (time - cpu_idle_time) / time
        # Calculate throughput
        throughput = len(processes) / time
        return {
            "processes": processes,
            "time": time,
            "cpu_utilization": cpu_utilization,
            "throughput": throughput,
            "average_waiting_time": self.average_waiting_time(processes),
            "average_turnaround_time": self.average_turnaround_time(processes),
            "average_response_time": self.average_response_time(processes)
        }

    def average_waiting_time(self, processes):
        """
        Calculate average waiting time
        :param processes: list of executed processes
        :return: average waiting time
        """
        total_waiting_time = 0
        for process in processes:
            total_waiting_time += process.waiting_time
        return total_waiting_time / len(processes)

    def average_turnaround_time(self, processes):
        """
        Calculate average turnaround time
        :param processes: list of executed processes
        :return: average turnaround time
        """
        total_turnaround_time = 0
        for process in processes:
            total_turnaround_time += process.turnaround_time
        return total_turnaround_time / len(processes)

    def average_response_time(self, processes):
        """
        Calculate average response time
        :param processes: list of executed processes
        :return: average response time
        """
        total_response_time = 0
        for process in processes:
            total_response_time += process.response_time
        return total_response_time / len(processes)
