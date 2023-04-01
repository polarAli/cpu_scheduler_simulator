from algorithms.base_algorithm import BaseAlgorithm
from state import State
from collections import deque


class FCFS(BaseAlgorithm):
    """
    FCFS algorithm for scheduling processes
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
        time = 0.0
        processes = []
        executed_processes = deque([])
        while self.processes:
            process = self.processes.pop(0)
            #print(process)
            if process.state == State.READY:
                # Set process start and initial response time
                if process.start_time =='n/a' :
                    process.start_time = time
                    process.response_time = process.start_time - process.arrival_time

                # Process next 'chunk' of work
                if process.disk_i_o_inter!= []:
                    next_inter = process.disk_i_o_inter.pop(0)
                    if next_inter < process.service_time:
                        completed = next_inter - (process.service_time - process.remaining_time)
                        time += completed
                        process.remaining_time -= completed
                        process.arrival_time += time+process.disk_i_o_time
                        self.processes.append(process)
                        self.processes.sort(key=lambda x: x.arrival_time)
                else:
                    time += process.remaining_time
                    process.finish_time = time
                    process.turnaround_time = process.finish_time - process.start_time
                    process.turnaround_over_service = process.turnaround_time / process.service_time
                    process.state = State.EXECUTED
                    executed_processes.append(process)
                
        # Calculate throughput
        throughput = len(executed_processes) / time
        return {
            "average_response_time": self.average_response_time(executed_processes),
            "average_turnaround_time": self.average_turnaround_time(executed_processes),
            "average_turnaround_over_service": self.average_turnaround_over_service(executed_processes),
            "throughput": throughput,
            "processes": executed_processes,
            "total_time": time
        }
       
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
    
    def average_turnaround_over_service(self, processes):
        """
        Calculate average ratio of turnaround over service
        :param processes: list of executed processes
        :return: average ratio of turnaround over service
        """
        total_ratio = 0
        for process in processes:
            total_ratio += process.turnaround_over_service
        return total_ratio / len(processes)
