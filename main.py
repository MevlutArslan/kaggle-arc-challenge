from helpers import load_tasks

tasks = load_tasks("evaluation", number_of_tasks=5, pick_randomly=True)

num_of_tasks = len(tasks)
success_counter = 0

for task in tasks:
    solved_successfully: bool = task.solve()
    
    if solved_successfully:
        success_counter += 1

print(f"Percentage of succesful predictions for {num_of_tasks} tasks is {success_counter/num_of_tasks}")