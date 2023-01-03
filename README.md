# CPU Scheduler Simulator
## Description
This is a CPU scheduler simulator that simulates the behavior of different CPU scheduling algorithms.
The simulator is written in Python and uses matplotlib to plot the results.
Following algorithms are implemented:
* First Come First Serve (FCFS) or First In First Out (FIFO)
* Shortest Job First (SJF) (Preemptive)
* Shortest Job First (SJF) (Non-Preemptive)
* Round Robin (RR)
* Priority (Preemptive)
* Priority (Non-Preemptive)

## Usage
After cloning the repository and [setting up the environment](#environment-setup),
you can run the simulator can be run by executing the following command:
```bash
python3 simulate.py -a <algorithm> -p <processes.json>
```
The following arguments are available:
* `-a <algorithm>`: The scheduling algorithm to use. Possible values are
`FIFO`, `PreemptiveSJF`, `NonPreemptiveSJF`, `RR`,
`PreemptivePriority` and `NonPreemptivePriority`.
* `-p <processes.json>`: The path to the JSON file containing the processes to schedule. See the section [below](#processesjson) for more information.

### processes.json
The processes JSON file contains the processes to schedule. It is a JSON array of objects. Each object represents a process and has the following properties:
* `pid`: The process ID. This is a string.
* `arrival_time`: The arrival time of the process. This is an integer.
* `burst_time`: The burst time of the process. This is an integer.
* `priority`: The priority of the process. This is an integer.
This property is only required for the priority algorithms.
Smaller values indicate higher priority.

### Example for processes.json
```json
[
  {
    "pid": "P1",
    "arrival_time": 0,
    "burst_time": 5,
    "priority": 1
  },
  {
    "pid": "P2",
    "arrival_time": 1,
    "burst_time": 3,
    "priority": 2
  },
  {
    "pid": "P3",
    "arrival_time": 2,
    "burst_time": 2,
    "priority": 3
  }
]
```

## Output
The simulator will output the following information:
* The average waiting time
* The average turnaround time
* The average response time
* Throughput
* CPU utilization
* A box plot for three metrics:
    * Waiting time
    * Turnaround time
    * Response time

## Environment Setup
The simulator requires Python 3.6 or higher. Required Python packages are listed in `requirements.txt`.
They can be installed by executing the following command:
```bash
pip3 install -r requirements.txt
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
