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
    Simulate the scheduling algorithm and print the following:
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
        self.cpu_total_time = 0

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
                        burst_time=process['burst_time'],
                        priority=process['priority']
                    )
                )
                self.process_num += 1
        self.processes.sort(key=lambda x: x.arrival_time)

    def run(self):
        """
        Run the scheduling algorithm, then save the results.
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
        result = algorithm.run()

        # End python timer
        end_time = time.time()

        # Get the run time
        self.run_time = end_time - start_time

        # Get the results
        self.cpu_utilization = result['cpu_utilization']
        self.throughput = result['throughput']
        self.average_waiting_time = result['average_waiting_time']
        self.average_turnaround_time = result['average_turnaround_time']
        self.average_response_time = result['average_response_time']
        self.processes = result['processes']
        self.cpu_total_time = result['total_time']

    def print(self):
        """
        Plot the following:
        1. Simulation time
        2. CPU utilization
        3. Throughput
        4. Average waiting time
        5. Average turnaround time
        6. Average response time
        """
        print('Simulation time: %.10f s' % self.run_time)
        print('CPU total time: %.0f' % self.cpu_total_time)
        print('CPU utilization: %f%%' % (self.cpu_utilization * 100))
        print('Throughput: %.6f' % self.throughput)
        print('Average waiting time: %.2f' % self.average_waiting_time)
        print('Average turnaround time: %.2f' % self.average_turnaround_time)
        print('Average response time: %.2f' % self.average_response_time)

    def plot_subset(self, processes, name, subplot):
        """
        Plot the processes with given name.
        """
        # Create a list of waiting time
        waiting_time = []
        for process in processes:
            waiting_time.append(process.waiting_time)

        # Create a list of turnaround time
        turnaround_time = []
        for process in processes:
            turnaround_time.append(process.turnaround_time)

        # Create a list of response time
        response_time = []
        for process in processes:
            response_time.append(process.response_time)

        # Construct the box plot
        bp = subplot.boxplot(
            [waiting_time, turnaround_time, response_time],
            labels=['Waiting time', 'Turnaround time', 'Response time'],
            patch_artist=True
        )

        # Set the colors of the boxes
        for box in bp['boxes']:
            box.set(color='#7570b3', linewidth=2)
            box.set(facecolor='#1b9e77')

        # Set the colors of the whiskers
        for whisker in bp['whiskers']:
            whisker.set(color='#7570b3', linewidth=2)

        # Set the colors of the caps
        for cap in bp['caps']:
            cap.set(color='#7570b3', linewidth=2)

        # Set the colors of the medians
        for median in bp['medians']:
            median.set(color='#b2df8a', linewidth=2)

        # Set the colors of the fliers
        for flier in bp['fliers']:
            flier.set(marker='o', color='#e7298a', alpha=0.5)

        # Set axis labels
        subplot.set_xlabel('Processes')
        subplot.set_ylabel('Time')

        # Figure title
        subplot.set_title(name)

        # Figure legend
        subplot.legend()

    def plot(self):
        """
        Box plot the following parameters for three groups of processes:
        1. All processes
        2. Processes with burst time less than or equal to 10
        3. Processes with priority less than or equal to 5
        Parameters:
        1. Waiting time
        2. Turnaround time
        3. Response time
        """
        # Create a figure
        fig = plt.figure()

        # Create a subplot for all processes
        all_processes_subplot = fig.add_subplot(221)

        # Create a subplot for processes with burst time less than or equal to 10
        short_processes_subplot = fig.add_subplot(222, sharey=all_processes_subplot)

        # Create a subplot for processes with priority less than or equal to 5
        high_priority_processes_subplot = fig.add_subplot(223, sharey=all_processes_subplot)

        # Plot the processes
        self.plot_subset(self.processes, 'All processes', all_processes_subplot)
        self.plot_subset(
            [process for process in self.processes if process.burst_time <= 10],
            'Processes with burst time less than or equal to 10',
            short_processes_subplot
        )
        self.plot_subset(
            [process for process in self.processes if process.priority <= 5],
            'Processes with priority less than or equal to 5',
            high_priority_processes_subplot
        )

        # Create box for text results
        fig.text(
            0.5, 0.25,
            'Simulation time: %.10f s\n'
            'CPU total time: %.0f\n'
            'CPU utilization: %.6f%%\n'
            'Throughput: %.6f\n'
            'Average waiting time: %.2f\n'
            'Average turnaround time: %.2f\n'
            'Average response time: %.2f' % (
                self.run_time,
                self.cpu_total_time,
                (self.cpu_utilization * 100),
                self.throughput,
                self.average_waiting_time,
                self.average_turnaround_time,
                self.average_response_time
            ),
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10}
        )

        # Set the figure size
        fig.set_size_inches(18.5, 10.5)

        # Set the figure title
        fig.canvas.manager.set_window_title(self.algorithm)
        fig.suptitle(
            f'{self.algorithm} scheduling algorithm results',
            fontsize=20
        )

        # Show the figure
        plt.show()


if __name__ == '__main__':
    args = parser.parse_args()
    simulate = Simulate(args.process, args.algorithm)
    simulate.run()
    simulate.print()
    simulate.plot()
