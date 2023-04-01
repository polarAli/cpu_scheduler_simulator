"""
Process class for the scheduler simulation.
"""

from state import State


class Process:
    """
    Process class for the scheduler simulation.
    """

    def __init__(self, pid, arrival_time, service_time, disk_i_o_time, disk_i_o_inter):
        """
        Initialize a process.
        """
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.remaining_time = service_time
        self.disk_i_o_time = disk_i_o_time
        self.disk_i_o_inter = disk_i_o_inter
        self.start_time = None
        self.end_time = None
        self.io_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.state = State.READY

    @property
    def response_time(self):
        """
        Return the response time of the process.
        """
        return self.start_time - self.arrival_time

    def __str__(self):
        """
        Return a string representation of the process.
        """
        return "pid: {}, arrival_time: {}, priority: {}, remaining_time: {}".format(
            self.pid, self.arrival_time, self.priority, self.remaining_time
        )

    def __lt__(self, other):
        return getattr(self, self.compare_prop) < getattr(other, self.compare_prop)
