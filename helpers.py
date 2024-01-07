from pathlib import Path
from task import Task, TaskCase, TaskCaseType
import json
import random

root_folder = "./abstraction-and-reasoning-challenge-data"

def load_tasks(folder_name: str, number_of_tasks: int, skip_until: int = 0, pick_randomly: bool = False):
    tasks = []
    i = 0
    full_path = f"{root_folder}/{folder_name}"

    files = list(Path(full_path).glob("*.json"))

    if pick_randomly:
        # Shuffle the list of files randomly
        random.shuffle(files)

    for child in files:
        if i < skip_until:
            i += 1
            continue

        with open(child) as f:
            data = json.load(f)
            task = Task(child.name.split('.')[0])

            train_data = data["train"]
            test_data = data["test"]

            task.cases.extend([
                TaskCase(case_type=TaskCaseType.TRAIN, input_matrix=json_object["input"], output_matrix=json_object["output"])
                for json_object in train_data
            ])           

            task.cases.extend([
                TaskCase(case_type=TaskCaseType.TEST, input_matrix=json_object["input"], output_matrix=json_object["output"])
                for json_object in test_data
            ])

            for case in task.cases:
                case.generate_and_save_as_image()
            
            tasks.append(task)
        
        i += 1
        if i >= number_of_tasks:
            break

    return tasks
