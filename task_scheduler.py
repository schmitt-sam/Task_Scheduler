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

    # List each task's dependents for reverse lookup
    for task in tasks.values():
        for dep in task.dependencies:
            tasks[dep].dependents.append(task.name)
    return tasks

# Validate tasks and compute expected runtime (DAG + dfs)
def validate_tasks(tasks):
    visited, stack = set(), set() # Track visited nodes and current dfs path

    # Recursively sum dependency runtimes
    def dfs(task_name):
        if task_name in stack:
            # Revisiting node in current path -> cycle
            raise ValueError(f"cycle at {task_name}")
        if task_name in visited:
            # Already validated, skip
            return 0
        stack.add(task_name)
        visited.add(task_name)

        # Find longest runtime among dependencies
        max_dep_time = max((dfs(dep) for dep in tasks[task_name].dependencies), default=0) 
        stack.remove(task_name)

        # Add this task duration to longest dependency path
        return max_dep_time + tasks[task_name].duration 
    
    # Run dfs on all tasks
    total_runtime = max(dfs(task.name) for task in tasks.values())
    print(f"Expected total runtime: {total_runtime:.2f}s.")
    return total_runtime

# Run tasks
def run_tasks(tasks, expected_runtime):
    start_time = time.time()

    def run_task(task):
        # Wait for all dependencies to complete before starting
        for dep in task.dependencies:
            tasks[dep].completed.wait()
        print(f"Starting {task.name} (expected duration: {task.duration}s)")
        time.sleep(task.duration) # Simulate task by sleeping for expected duration
        print(f"Completed {task.name}")
        task.completed.set() # Denotes task completion

    # Use thread pool to run multiple tasks in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_task, task) for task in tasks.values()]
        for future in as_completed(futures):
            future.result()

    #Measure actual runtime
    actual_runtime = time.time() - start_time
    print(f"\nExpected runtime: {expected_runtime:.2f}s")
    print(f"Actual runtime: {actual_runtime:.2f}")

# CLI handler
def main():
    parser = argparse.ArgumentParser(description="Task Scheduler CLI")
    parser.add_argument('file', help="Path to task list file")
    parser.add_argument('--validate', action='store_true', help="Validate task list and print expected runtime")
    parser.add_argument('--run', action='store_true', help="Run tasks and compare actual vs expected runtime")
    args = parser.parse_args()
    tasks = parse_task_file(args.file)  # Build the task object list from file
    expected_runtime = validate_tasks(tasks)  # Check DAG & compute max expected runtime

    if args.run:
        run_tasks(tasks, expected_runtime)

# Entry point
if __name__ == "__main__":
    main()