"""
Process class for the scheduler simulation.
"""

import logging

from state import State


class Process:
    """
    Process class for the scheduler simulation.
    """

    def __init__(self, pid, arrival_time, priority, burst_time):
        """
        Initialize a process.
        """
        self.pid = pid
        self.arrival_time = arrival_time
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.io_time = 0
        self.turnaround_time = 0
        self.state = State.READY
        self.logger = logging.getLogger(__name__)

    @property
    def waiting_time(self):
        """
        Return the waiting time of the process.
        """
        return self.start_time - self.arrival_time
