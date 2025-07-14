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

# Validate tasks and compute expected runtime (DAG)
def validate_tasks(tasks):
    visited, stack = set(), set()

    def dfs(task_name):
        if task_name in stack:
            raise ValueError(f"cycle at {task_name}")
        if task_name in visited:
            return 0
        stack.add(task_name)
        visited.add(task_name)
        max_dep_time = max((dfs(dep) for dep in tasks[task_name].dependencies), default=0)
        stack.remove(task_name)
        return max_dep_time + tasks[task_name].duration
    
    total_runtime = max(dfs(task.name) for task in tasks.values())
    print(f"Expected total runtime: {total_runtime}s.")
    return total_runtime