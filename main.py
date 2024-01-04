import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib import colors
from PIL import Image
import io
import os

'''

1. Load tasks
2. Send both the matrix and the image to OpenAI Vision
3. Abstract things out and scale them

'''


# Load Task logic
'''

The task jsons are structured like:
{
    'train' : [{input: [], output: []}],
    'test': [{input: [], output: []}]
}

so it makes sense to 
1. read the json, 
2. construct TaskCase objects with types as TRAINING and TEST
3. generate and save their images
4. store them in the parent class Task

* we need to be able to load different directories
  so the method should take in the directory we want to read

'''
from pathlib import Path
from task import Task, TaskCase, TaskCaseType
import json

root_folder = "./abstraction-and-reasoning-challenge-data"
tasks = []

def load_tasks(folder_name: str):
    full_path = f"{root_folder}/{folder_name}"

    for child in Path(full_path).glob("*.json"):
        with open(child) as f:
            data = json.load(f)
            task = Task(child.name.split('.')[0])

            train_data = data["train"]
            test_data = data["test"]

            task.cases.extend([
                (TaskCase(case_type=TaskCaseType.TRAIN, input_matrix=json_object["input"], output_matrix=json_object["output"])).generate_and_save_as_image()
                for json_object in train_data
            ])           

            task.cases.extend([
                (TaskCase(case_type=TaskCaseType.TEST, input_matrix=json_object["input"], output_matrix=json_object["output"])).generate_and_save_as_image()
                for json_object in test_data
            ])
            
            print(task.id)
            tasks.append(task)
        break

load_tasks("training")
