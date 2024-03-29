## My Attempt at Solving the ARC Challenge

**ARC Challenge:** [ARC Challenge on Kaggle](https://www.kaggle.com/competitions/abstraction-and-reasoning-challenge/overview)

I didn't get a chance to run the full evaluation set as the costs kept mounting pretty high, and I would like to preserve my OpenAI budget for other experiments.

Randomly picking 5 tasks repetitively in the evaluation set usually resulted in 1/5 correct answers.

**Things to Note:**
- The token limit of 4096 tokens on GPT4-Vision prevents us from creating chains that might be able to provide a "smarter" model.
- The model performed pretty well with smaller grids.

**Improving Chain Performance:**

**Indexing Previously Successful Reasonings:**
- Having the model fill in and return reasoning structures, then indexing the successful ones and reusing them, could help improve its reasoning ability.
- This would mimic how humans draw parallels to previous experiences when solving new problems.
- By having the model fill out reasoning forms, saving those that work, and retrieving those effective reasoning patterns, it can build on what worked before rather than starting from scratch each time.
- This repetition and reuse of successful reasoning frameworks represent more human-like logic and pattern recognition.
