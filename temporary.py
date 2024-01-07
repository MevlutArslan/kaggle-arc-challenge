## Instructions for returning in proper format.
''''
Return a JSON:
   - Return the response as a JSON object with the keys:
     - "output_matrix": (List of lists) The generated output matrix.
     - "reasoning": (Object) The finalized explanation of the recognized pattern.
     '''

## FOR GPT VISION QUERIES
number_color_map = ''''
The following map explains which number corresponds to which color incase you want to use the images to extract the pattern
[
    0: 'Black',
    1: 'Blue',
    2: 'Red',
    3: 'Green',
    4: 'Yellow',
    5: 'Light Grey'
    7: 'Pink',
    8: 'Orange',
    9: 'Maroon'
]
'''

## INDEXING LOGIC

# output_dimension_mismatch_template = PromptTemplate(input_variables=["output_dimension_selection_logic_history"], template=output_matrix_mismatch_msg)
#     output_dimension_mismatch_prompt_template = SystemMessagePromptTemplate(prompt=output_dimension_mismatch_template).format(output_dimension_selection_logic_history=str(output_dimension_selection_logic_history))
#     output_dimension_mismatch_prompt = str(output_dimension_mismatch_prompt_template)
    
#     is_equal = False

#     if len(test_case.output_matrix) != len(output_matrix) or len(test_case.output_matrix[0]) != len(output_matrix[0]):
#         print("Detected grid mismatch, adding SystemMessage to assist the model")
#         messages.insert(0, SystemMessage(content=output_dimension_mismatch_prompt))
#     else:
#         is_equal = (output_matrix == test_case.output_matrix).all()

#         wrong_answer_template = PromptTemplate(input_variables=["detected_pattern_history"], template=wrong_answer_msg)
#         wrong_answer_prompt_template = SystemMessagePromptTemplate(prompt=wrong_answer_template).format(detected_pattern_history=str(detected_pattern_history))
#         wrong_answer_prompt = str(wrong_answer_prompt_template)
        
#         if is_equal == False:
#             print("Detected wrong answer, adding SystemMessage to assist the model")
#             messages.insert(1, SystemMessage(content=wrong_answer_prompt))
        
#     if len(messages) > messages_len:
#         result = llm.predict_messages(messages)
#         print(parser.parse(result.content))
#         output_matrix == parser.parse(result.content).output_matrix

#     if is_equal:
#         # index output_dimension_reasoning
#         if not similar_output_dimension_selection_logic_exists(result.reasoning["output_matrix_size_reason"]):
#             output_dimension_selection_logic_history.append(reasoning_obj["output_dimension_selection_logic"])
            
#         # index operation_descriptions
#         if not similar_operation_descriptions_exists(result.reasoning["operation_descriptions"]):
#             detected_pattern_history.append(reasoning_obj["operation_descriptions"])

#     

# output_dimension_selection_logic_history = []
# detected_pattern_history = []

# check_similar_meaning_exists_system_template = '''
#     You are a model tasked with determining if the given list of strings has very similar meanings to those already stored.
#     Perform a detailed comparison, considering semantic nuances, and return a response in the following format:

    
#     is_similar: bool  # Set to True if highly similar meanings are detected, otherwise set to False
    

#     Note: Pay attention to subtle differences in meaning, context, or connotation when making your assessment.

#     {existing_elements}
# '''

# check_similar_meaning_exists_human_template = '''
#     Check if the following list of text are similar to any existing ones:

#     {list_to_check}
# '''

# class SimilarityCheckParser(BaseModel):
#     is_similar: bool = Field("True or False value depending on if highly similar meanings are detected")

# def similar_output_dimension_selection_logic_exists(new_entry: list, llm) -> bool:
#     system_prompt_template = PromptTemplate(input_variables=["existing_elements"], template=check_similar_meaning_exists_system_template)
#     system_prompt = SystemMessagePromptTemplate(prompt= system_prompt_template).format(existing_elements=str(output_dimension_selection_logic_history))

#     human_prompt_template = PromptTemplate(input_variables=["list_to_check"], template=check_similar_meaning_exists_human_template)
#     human_prompt = HumanMessagePromptTemplate(prompt=human_prompt_template).format(list_to_check=str(new_entry))
#     result = llm.predict_messages([
#         system_prompt,
#         human_prompt
#     ])
    
#     parser = PydanticOutputParser(SimilarityCheckParser)

#     return parser.parse(result.content).is_similar

# def similar_operation_descriptions_exists(new_entry: list, llm):
#     system_prompt_template = PromptTemplate(input_variables=["existing_elements"], template=check_similar_meaning_exists_system_template)
#     system_prompt = SystemMessagePromptTemplate(prompt= system_prompt_template).format(existing_elements=str(detected_pattern_history))

#     human_prompt_template = PromptTemplate(input_variables=["list_to_check"], template=check_similar_meaning_exists_human_template)
#     human_prompt = HumanMessagePromptTemplate(prompt=human_prompt_template).format(list_to_check=str(new_entry))
#     result = llm.predict_messages([
#         system_prompt,
#         human_prompt
#     ])
    
#     parser = PydanticOutputParser(SimilarityCheckParser)

#     return parser.parse(result.content).is_similar
