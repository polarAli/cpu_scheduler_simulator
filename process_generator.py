"""
Generate a json dataset for simulation
"""

import argparse
import json
import random

parser = argparse.ArgumentParser(description='Generate a json dataset for simulation')
parser.add_argument('--output', '-o', type=str, default='dataset.json', help='Output file')
parser.add_argument('--size', '-s', type=int, default=100000, help='Number of samples')


class ProcessGenerator:
    def __init__(self, size):
        self.size = size
        self.processes = []

    def generate(self):
        for i in range(self.size):
            self.processes.append({
                'pid': i,
                'arrival_time': random.randint(0, 100),
                'priority': random.randint(0, 10),
                'burst_time': random.randint(0, 100),
            })

    def save(self, output):
        with open(output, 'w') as f:
            json.dump(self.processes, f)


if __name__ == '__main__':
    args = parser.parse_args()
    generator = ProcessGenerator(args.size)
    generator.generate()
    generator.save(args.output)
