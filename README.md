# Task Scheduler CLI

A simple command-line tool to schedule and run tasks with dependencies.  
It can validate a task list and calculate the expected runtime, or execute the tasks in parallel while respecting dependencies.

---

## Features

- Read task list from a text file (CSV format)
- Validate task dependencies (detect cycles, calculate critical path)
- Simulate task execution in parallel
- Compare actual runtime vs. expected runtime

---

## Task List Format

Each line in the task list file should follow this format:

- **name**: Unique task name (string)
- **duration**: Time (in seconds) the task takes to run (integer)
- **dependencies**: Space-separated names of prerequisite tasks (optional)

---

## How to Build and Run

### Requirements

- Python 3.8+
- pytest 7.0.0+ 

---

### Clone the repository

```
git clone https://github.com/your-username/task-scheduler.git
cd task-scheduler
```

---

### Validate Task List and Calculate Expected Runtime

```
python task_scheduler.py sample_tasks.txt --validate
```

### Run Tasks

```
python task_scheduler.py sample_tasks.txt --run
```

### Run Tests

- Install test dependencies
```
pip install -r requirements.txt
```
- Discover/Run tests
```
python -m pytest tests
```