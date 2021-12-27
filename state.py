class State:
    """
    Enum for process states
    """
    RUNNING = 0
    READY = 1
    WAITING = 2
    TERMINATED = 3
    BLOCKED = 4
    SUSPENDED = 5
    UNKNOWN = 6

    def __init__(self):
        self.state = State.UNKNOWN

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def __str__(self):
        if self.state == State.RUNNING:
            return "RUNNING"
        elif self.state == State.READY:
            return "READY"
        elif self.state == State.WAITING:
            return "WAITING"
        elif self.state == State.TERMINATED:
            return "TERMINATED"
        elif self.state == State.BLOCKED:
            return "BLOCKED"
        elif self.state == State.SUSPENDED:
            return "SUSPENDED"
        else:
            return "UNKNOWN"
