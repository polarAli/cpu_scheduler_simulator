from algorithms.base_algorithm import BaseAlgorithm


class PriorityPreemptive(BaseAlgorithm):

    def __init__(self, processes):
        super().__init__(processes)
        # Queue of processes which are ready to execute. limited to 100 processes
        self.ready_queue = []
        self.running_process = None
        self.time = 0.0
        self.idle_time = 0.0

    def run(self):
        """
        Schedule the processes using Priority Preemptive algorithm and calculate following
        information.
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
                arrived_processes.sort(key=lambda process: process.priority)
                if self.running_process is None:
                    self.running_process = sorted(arrived_processes, key=lambda x: x.priority)[0]
                    self.running_process.start_time = self.time

                elif self.running_process.priority > arrived_processes[0].priority:
                    self.ready_queue.append(self.running_process)
                    self.running_process = arrived_processes[0]
                    self.running_process.start_time = self.time

                self.remove_processes(arrived_processes)
                if self.running_process in arrived_processes:
                    arrived_processes.remove(self.running_process)
                self.ready_queue.extend(arrived_processes)
                arrived_processes.clear()

            # If no process is running, then pick the process from ready queue
            if self.running_process is None and self.ready_queue:
                self.running_process = min(self.ready_queue, key=lambda x: x.priority)
                self.running_process.start_time = self.running_process.start_time or self.time
                self.ready_queue.remove(self.running_process)

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
        return arrived_processes

    def get_next_important_time(self):
        """
        Find next point of time that need a decision
        :return: Int
        """
        processes = [process for process in self.processes if process.arrival_time > self.time]
        if self.running_process is not None:
            if not processes:
                return max(self.time + self.running_process.remaining_time, self.time)

            return min(
                self.time + (self.running_process.remaining_time or 1),
                min(process.arrival_time for process in processes)
            )

        if self.ready_queue:
            return self.time + 1

        if processes:
            return min(process.arrival_time for process in processes)

        return self.time + 1

    def remove_processes(self, processes):
        """
        Remove processes from processes list
        :param processes: list of processes
        :return: None
        """
        for process in processes:
            self.processes.remove(process)
