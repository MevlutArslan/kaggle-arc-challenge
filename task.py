from enum import Enum
import numpy as np
from image_utils import generate_base64_images

# from model import run_model
class TaskCaseType(Enum):
    TRAIN = "train"
    TEST = "test"

class TaskCase:
    def __init__(self, case_type: TaskCaseType, input_matrix, output_matrix) -> None:
        self.type = case_type
        self.input_matrix = np.array(input_matrix)
        self.output_matrix = np.array(output_matrix)
        pass
    
    def generate_and_save_as_image(self):
        self.input_image = generate_base64_images(self.input_matrix, "Input")
        self.output_image = generate_base64_images(self.output_matrix, "Output")

class Task:
    def __init__(self, id: str) -> None:
        self.id = id
        self.cases = []
    
    # will return true if the model's output matches the test case's output
    def solve(self) -> bool:
        from model import run_model

        expected_output = self.cases[len(self.cases) - 1].output_matrix

        ## Takes forever to solve a large grid and costs alot
        if len(self.cases[0].input_matrix) > 15 or len(self.cases[0].input_matrix[0]) > 15:
            print("Skipping this task to save on API cost because of the size of the grid.")
            return False
        
        model_output = run_model(self)

        if len(expected_output) != len(model_output) or len(expected_output[0]) != len(model_output[0]):
            print(f"Ran solve Task and got size mismatch between expected_output and model_output, registering as False")
            return False

        is_equal = (model_output == expected_output).all()

        print(f"Ran solve Task and got is_equal = {is_equal}")
        return is_equal

    