import unittest
from task_scheduler import parse_task_file, validate_tasks, Task

class TestValidation(unittest.TestCase): # Unit tests for validate_tasks function

    # Tests a valid DAG with dependencies and calulates critical path
    def test_valid_task_list(self):
        tasks = {
            "taskA": Task("taskA", 3, []),
            "taskB": Task("taskB", 2, ["taskA"]),
            "taskC": Task("taskC", 4, ["taskA"]),
            "taskD": Task("taskD", 1, ["taskB", "taskC"]),
        }

        for task in tasks.values():
            for dep in task.dependencies:
                tasks[dep].dependents.append(task.name)
                
        runtime = validate_tasks(tasks)
        self.assertEqual(runtime, 8)

    # Test detection of a cyclic dependency
    def test_cycle_detection(self):
        tasks = {
            "taskA": Task("taskA", 3, ["taskB"]),
            "taskB": Task("taskB", 2, ["taskA"]),
        }
        with self.assertRaises(ValueError):
            validate_tasks(tasks)

    # Test a graph with disconnected tasks
    def test_disconnected_graph(self):
        tasks = {
            "taskA": Task("taskA", 3, []),
            "taskB": Task("taskB", 2, []),
        }
        runtime = validate_tasks(tasks)
        self.assertEqual(runtime, 3)  # Longest standalone task

if __name__ == '__main__':
    unittest.main()