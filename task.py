from enum import Enum
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
from model import run_model
class TaskCaseType(Enum):
    TRAIN = "train"
    TEST = "test"

# each example will contain an input_matrix, output_matrix and image 
class TaskCase:
    def __init__(self, case_type: TaskCaseType, input_matrix, output_matrix) -> None:
        self.type = case_type
        self.input_matrix = np.array(input_matrix)
        self.output_matrix = np.array(output_matrix)
        pass
    
    def generate_and_save_as_image(self):
        cmap = colors.ListedColormap(
            ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
             '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
        norm = colors.Normalize(vmin=0, vmax=9)

        # creating a figure with 2 plots
        fig, axs = plt.subplots(1, 2, figsize=(15, 15))
        # plot the input matrix to the first subplot
        axs[0].imshow(self.input_matrix, cmap=cmap, norm=norm)
        axs[0].axis('off')
        axs[0].set_title('Train Input')

        # plot the output matrix to the second subplot
        axs[1].imshow(self.output_matrix, cmap=cmap, norm=norm)
        axs[1].axis('off')
        axs[1].set_title('Train Output')

        plt.tight_layout()

        image_buf = io.BytesIO()
        plt.savefig(image_buf, format="png", bbox_inches='tight', pad_inches=0)

        b64_encoded_image = base64.b64encode(image_buf.getvalue()).decode('utf-8')
        print(b64_encoded_image)

class Task:
    def __init__(self, id: str) -> None:
        self.id = id
        self.cases = []
    
    # will return true if the model's output matches the test case's output
    def solve(self) -> bool:
        expected_output = self.cases[len(self.cases) - 1]
        model_output = run_model(self.cases)

        return model_output == expected_output

    