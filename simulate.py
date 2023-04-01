"""
Run simulation with given process.json and algorithm, then plot the result.
"""
import argparse
import json
import time

from matplotlib import pyplot as plt

import algorithms
from process import Process

parser = argparse.ArgumentParser(description='Simulate the scheduling algorithm.')
parser.add_argument('-p', '--process', type=str, help='process.json file')
parser.add_argument('-a', '--algorithm', type=str, help='algorithm name')


class Simulate:
    """ 
    Simulate the scheduling algorithm and print the following for each process:
    1. Start time
    2. Finish time
    3. Response time 
    4. Turnaround time (Tr)
    5. Ratio of Turnaround and service time (Tr/Ts)
    
    Print the following for the system:
    1. Average response time
    2. Average turnaround time
    3. Average Tr/Ts
    4. Throughput
    5. CPU total time
    6. Simulation Time
    """

    def __init__(self, process_file, algorithm):
        self.process_file = process_file
        self.algorithm = algorithm
        self.processes = []
        self.process_num = 0
        self.throughput = 0
        self.average_turnaround_time = 0.0
        self.average_response_time = 0.0
        self.run_time = 0
        self.cpu_total_time = 0

        # Get the algorithm class
        try:
            self.AlgorithmClass = getattr(algorithms, self.algorithm)
        except AttributeError:
            print('Algorithm not found.')
            exit(1)
            return

    def read_process(self):
        """
        Read process.json file and store the processes in self.processes.
        """
        with open(self.process_file, 'r') as f:
            data = json.load(f)
            for process in data:
                self.processes.append(
                    Process(
                        pid=process['pid'],
                        arrival_time=process['arrival_time'],
                        service_time=process['service_time'],
                        disk_i_o_time=process['disk_i_o_time'],
                        disk_i_o_inter=process['disk_i_o_interval']
                        #priority=process['priority'],
                        #compare_prop=self.AlgorithmClass.process_compare_prop
                    )
                )
                self.process_num += 1
        self.processes.sort(key=lambda x: x.arrival_time)

    def run(self):
        """
        Run the scheduling algorithm, then save the results.
        """

        self.read_process()

        # Create the algorithm instance
        algorithm = self.AlgorithmClass(self.processes)

        # Start python timer
        start_time = time.time()

        # Run the algorithm
        result = algorithm.run()

        # End python timer
        end_time = time.time()

        # Get the run time
        self.run_time = end_time - start_time

        # Get the results
        self.average_response_time = result['average_response_time']
        self.average_turnaround_time = result['average_turnaround_time']
        self.average_turnaround_over_service = result['avearage_turnaround_over_service']
        self.throughput = result['throughput']
        self.processes = result['processes']
        self.cpu_total_time = result['total_time']

    def print(self):
         """
        Print the following for each process:
        1. Start time
        2. Finish time
        3. Response time 
        4. Turnaround time (Tr)
        5. Ratio of Turnaround and service time (Tr/Ts)
        """
        print('Start time \t Finish_time \t Response_time \t Turnaround_time \t Tr/Ts')
        for process in processes:
            print(process.start_time, ' \t ', process.finish_time, ' \t ', process.response_time, 
                  ' \t ', process.turnaround_time, ' \t ', process.turnaround_over_service)
        """
        Print the following for the system:
        1. Average response time
        2. Average turnaround time
        3. Average Tr/Ts
        4. Throughput
        5. CPU total time
        6. Simulation Time
        """
        print('Average response time: %.2f' % self.average_response_time)
        print('Average turnaround time: %.2f' % self.average_turnaround_time)
        print('Average ratio of turnaround and service time: %.2f", % self.avearage_turnaround_over_service)
        print('Throughput: %.6f' % self.throughput)
        print('CPU total time: %.0f' % self.cpu_total_time)
        print('Simulation time: %.10f s' % self.run_time)
     
   

if __name__ == '__main__':
    args = parser.parse_args()
    simulate = Simulate(args.process, args.algorithm)
    simulate.run()
    simulate.print()
    
