from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate, HumanMessagePromptTemplate
from task import Task, TaskCaseType

## Vision models token limit of 4096 is too low to allow the model to make sense of what it is seeing, so I omit them from the prompt
def generate_objects(task: Task):
    objects = []

    for case in task.cases:
        if case.type == TaskCaseType.TRAIN:
            input_text_object = {"type": "text", "text": "input_matrix:" + str(case.input_matrix.tolist()).strip() + "\n input_image:"}
            input_image_object = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{case.input_image}"}}
            
            output_text_object = {"type": "text", "text": "output_matrix:" + str(case.output_matrix.tolist()).strip() + "\n output_image:"}
            output_image_object = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{case.output_image}"}}

            objects.append(input_text_object)
            # objects.append(input_image_object)
            objects.append(output_text_object)
            # objects.append(output_image_object)
                

    return objects

system_message = '''  - As a specialized pattern recognition model, your task is to analyze example input and output matrices, identifying the single transformation rule and applying that transformation rule to the given input matrix.

The grids contain numbers from 0-9 inclusively and are intentionally arranged to display some rule/pattern.

Two important patterns to extract:
1. The transformation rule that decides the output_matrix's shape.
2. Layout of different Shapes and the difference between shapes in the input and output matrices.

Shapes:
Shapes in the matrices represent distinct patterns formed by collections of numbers.
 - Consider shapes as entities, like "Islands," surrounded by other shapes or the most frequent number in the matrix.
 - Pay attention to the spatial arrangement and relationships between numbers forming these shapes.
 - Note that collections of grids constitute shapes. Focus on areas with numerous numbers—they might represent a significant 'Shape.'
 - Explicitly look for lines, rectangular shapes, and symmetrical patterns.

Look for consistent patterns or conditions across multiple examples.
These patterns can be of nature:
[symmetry, set operations, rotations, scaled up and scaled down, repetition, containment, trimming, completing each other like puzzle pieces, and similar operations]

Identifying the most frequent number in the input and output matrices can be useful. Compare the most frequent numbers in input and output matrices and explore reasons for their similarity or difference.
Rather than fixating on individual numbers, concentrate on recognizing and understanding "Shapes" as defined.

Once you have a pattern:

Generate a Reasoning Object:
   - Provide a structured explanation of the recognized pattern, including notable patterns, symmetries, or relationships observed.
   - Format the reasoning object with the keys:
     - "output_matrix_size_reason": (List of strings) Explain the criteria or rule used to decide the size of the output matrix.
     - "operation_descriptions": (List of strings) Discuss any mathematical operations, transformations, or relationships involved.

Verify the Reasoning Object:
   - Cross-check your reasoning against the provided examples to ensure accuracy.
   - Make recursive modifications until you can verify the reasoning against the example cases.

Examples:
   - {example_cases}

Generate an Output Matrix:
   - Once the reasoning is verified, use the same pattern to generate an output matrix for the given input matrix.
'''




human_message = '''Find the output for the given input_matrix:

Input Matrix:
{input_matrix}

Provide the output in the following structure as JSON and only the json and nothing else:

    "output_matrix": [[][]] # output matrix as a standard python list format,
    "reasoning": 
        "output_dimension_selection_logic": [],  # List of strings describing notable patterns, symmetries, or features influencing the output size
        "operation_descriptions": []  # List of strings describing mathematical operations, transformations, or relationships involved
    

'''

output_matrix_mismatch_msg = '''
    The shape of the provided output matrix does not match the expected shape. Please review it again. To assist you, here are some of the patterns encountered while solving other examples:
    
    {output_dimension_selection_logic_history}
'''

wrong_answer_msg = '''
    It seems that the provided output matrix does not match the expected answer. Please review your solution. To assist you, consider analyzing the previously detected patterns:

    {detected_pattern_history}
'''

from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class OutputParser(BaseModel):
    output_matrix: list = Field(description="The generated output matrix in the classic Python array format i.e. [[][][]]")
    reasoning: dict = Field(
        description="A JSON object containing the recognized pattern and steps that led up to it.",
        output_dimension_selection_logic=list,
        operation_descriptions=list
    )

parser = PydanticOutputParser(pydantic_object=OutputParser)


## indexing and referencing previously succesful reasonings can help with more complex tasks, need to read more about LangChain's API and implement a RAG system
def run_model(task: Task) -> list():
    print(f"called run_model for task: {task.id}")
    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0, max_tokens=4000)

    generated_objects = generate_objects(task)

    #due to the ordering of loading the task json we can always be sure of the test case being the last loaded case
    test_case = task.cases[len(task.cases) - 1] 

    example_cases_string = str(generated_objects)

    prompt_template = PromptTemplate(input_variables=["example_cases"], template=system_message)
    system_prompt_template = SystemMessagePromptTemplate(prompt=prompt_template).format(example_cases=example_cases_string)

    system_prompt = str(system_prompt_template)

    input_matrix_str = str(test_case.input_matrix)

    human_template = PromptTemplate(input_variables=["input_matrix"], template=human_message)
    human_prompt_template = HumanMessagePromptTemplate(prompt=human_template).format(input_matrix=input_matrix_str)

    human_prompt = str(human_prompt_template)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    messages_len = len(messages)
    # print(system_prompt)
    # print(system_prompt)
    result = llm.predict_messages(
        messages
    )

    output_matrix = parser.parse(result.content).output_matrix
    reasoning_obj = parser.parse(result.content).reasoning

    # show as image for debugging purposes
    # output_as_image = Image.open(BytesIO(base64.b64decode( generate_base64_images(predicted_output_matrix, "Output"))))
    
    print(result.content)
    return output_matrix

