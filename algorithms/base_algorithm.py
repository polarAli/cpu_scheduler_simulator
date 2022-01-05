from collections import deque


class BaseAlgorithm:
    """
    Base class for all algorithms.
    """
    process_compare_prop = 'arrival_time'

    def __init__(self, processes):
        """
        Initialize the algorithm.
        :param processes: list of processes to be executed.
        """
        self.processes = deque(processes)

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
        raise NotImplementedError
