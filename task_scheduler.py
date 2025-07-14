# Imports
import argparse
import csv
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque


# Task class initialization
class Task:
    def __init__(self, name, duration, dependencies):
        self.name = name
        self.duration = duration
        self.dependencies = dependencies #list of task names
        self.dependents = []
        self.completed = threading.Event()

# Parse input file (assumed to be csv)
def parse_task_file(file_path):
    tasks = {}
    with open(file_path, 'r') as f:
        task_file = csv.reader(f)
        for row in task_file:
            name = row[0].strip()
            duration = int(row[1].strip())
            depends = [dep.strip() for dep in row[2].split()] if len(row) >2 else []
            tasks[name] = Task(name, duration, depends)
    # List dependents for each task
    for task in tasks.values():
        for dep in task.dependencies:
            tasks[dep].dependents.append(task.name)
    return tasks


