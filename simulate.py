"""
Run simulation with given process.json and algorithm, then plot the result.
"""
import argparse
import json
import time

import algorithms
from process import Process

parser = argparse.ArgumentParser(description='Simulate the scheduling algorithm.')
parser.add_argument('-p', '--process', type=str, help='process.json file')
parser.add_argument('-a', '--algorithm', type=str, help='algorithm name')


class Simulate:
    """
    Simulate the scheduling algorithm and plot the following:
    1. Simulation time
    2. CPU utilization
    3. Throughput
    4. Average waiting time
    5. Average turnaround time
    6. Average response time
    """

    def __init__(self, process_file, algorithm):
        self.process_file = process_file
        self.algorithm = algorithm
        self.processes = []
        self.process_num = 0
        self.cpu_utilization = 0
        self.throughput = 0
        self.average_waiting_time = 0.0
        self.average_turnaround_time = 0.0
        self.average_response_time = 0.0
        self.run_time = 0

    def read_process(self):
        """
        Read process.json file and store the processes in self.processes.
        """
        with open(self.process_file, 'r') as f:
            data = json.load(f)
            for process in data['processes']:
                self.processes.append(
                    Process(
                        pid=process['pid'],
                        arrival_time=process['arrival_time'],
                        burst_time=process['burst_time'],
                        priority=process['priority']
                    )
                )
                self.process_num += 1

    def run(self):
        """
        Run the scheduling algorithm, then save the results and call plot() to plot the result.
        """

        self.read_process()

        # Get the algorithm class
        try:
            AlgorithmClass = getattr(algorithms, self.algorithm)
        except AttributeError:
            print('Algorithm not found.')
            exit(1)
            return

        # Create the algorithm instance
        algorithm = AlgorithmClass(self.processes)

        # Start python timer
        start_time = time.time()

        # Run the algorithm
        algorithm.run()

        # End python timer
        end_time = time.time()

        # Get the run time
        self.run_time = end_time - start_time

        # Get the results
        self.cpu_utilization = algorithm.cpu_utilization
        self.throughput = algorithm.throughput
        self.average_waiting_time = algorithm.average_waiting_time
        self.average_turnaround_time = algorithm.average_turnaround_time
        self.average_response_time = algorithm.average_response_time

    def plot(self):
        """
        Plot the following:
        1. Simulation time
        2. CPU utilization
        3. Throughput
        4. Average waiting time
        5. Average turnaround time
        6. Average response time
        """
        print('Simulation time: %.2f' % self.run_time)
        print('CPU utilization: %.2f%%' % self.cpu_utilization)
        print('Throughput: %.2f' % self.throughput)
        print('Average waiting time: %.2f' % self.average_waiting_time)
        print('Average turnaround time: %.2f' % self.average_turnaround_time)
        print('Average response time: %.2f' % self.average_response_time)
