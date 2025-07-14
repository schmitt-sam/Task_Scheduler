import unittest
import time
from task_scheduler import Task, run_tasks

class TestExecution(unittest.TestCase):

    def test_run_tasks_runtime(self):
        tasks = {
            "taskA": Task("taskA", 3, []),
            "taskB": Task("taskB", 2, ["taskA"]),
            "taskC": Task("taskC", 4, ["taskA"]),
            "taskD": Task("taskD", 1, ["taskB", "taskC"]),
        }

        for task in tasks.values():
            for dep in task.dependencies:
                tasks[dep].dependents.append(task.name)
                
        expected_runtime = 8  # Critical path: A(3) -> B(4) -> D(1) = 8s

        start = time.time()
        run_tasks(tasks, expected_runtime)
        actual_runtime = time.time() - start

        # Allow ~1s tolerance for timing
        self.assertTrue(abs(actual_runtime - expected_runtime) < 1.0)

if __name__ == '__main__':
    unittest.main()