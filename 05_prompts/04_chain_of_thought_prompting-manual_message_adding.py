"""
Chain of Thought Prompting Example
"""

from openai import OpenAI

import json

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['GEMINI_API_KEY']

client = OpenAI(
    api_key=token,  # Gemini API key here
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

SYSTEM_PROMPT = """
You are an expert AI assistant that always thinks step by step before answering using chain of thought prompting.
You work on START, PLAN and OUTPUT framework.
You need to follow these steps:
1. START: Understand the question and identify what is being asked.
2. PLAN: Outline a step-by-step plan to solve the problem or answer the question. There can be multiple steps.
3. OUTPUT: Execute the plan and provide the final answer or solution. This will be displayed to the user.

Rules:
- Strictly follow the JSON output format.
- Only run one step at a time.

Output Format:
{
"step": "START" | "PLAN" | "OUTPUT",
"thought": "<your_thought_process>",
"content": "<your_content_based_on_step>"
}

Example:
START: Hey, Can you solve 2+3*5/10
PLAN: {"step": "PLAN", "thought": "Seems user is interested in solving a mathematical expression. I need to follow the order of operations (PEMDAS/BODMAS) to solve it correctly.", "content": "I need to first handle the multiplication and division from left to right, and then perform the addition."}
PLAN: {"step": "PLAN", "thought": "The question is asking to solve the mathematical expression 2+3*5/10. I need to follow the order of operations (PEMDAS/BODMAS) to solve it correctly.", "content": "I understand that I need to solve the expression step by step."}
PLAN: {"step": "PLAN", "thought": "To solve the expression 2+3*5/10, I will first handle the multiplication and division from left to right, and then perform the addition.", "content": "1. Calculate 3*5 = 15. 2. Calculate 15/10 = 1.5. 3. Finally, add 2 + 1.5."}
OUTPUT: {"step": "OUTPUT", "thought": "Now I will execute the plan step by step to get the final answer.", "content": "The final answer is 3.5."}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        # {"role": "user", "content": "Hey, translate word hello to hindi"},
        # {"role": "user", "content": "Hey,give python code for adding 2 numbers"},
        # {"role": "user", "content": "Can you give me formula for a+b ^^ 2? "}
        {"role": "user", "content": "Hey,give js code for adding n numbers"},
        #Manually keep adding responses to the history to simulate chain of thought prompting
        {"role": "assistant", "content": json.dumps(
            {
                "step": "START",
                "thought": "The user wants JavaScript code to add two numbers. I need to provide a clear and simple example.",
                "content": "I need to provide a JavaScript code snippet that adds two numbers."
            })
         },
        {"role": "assistant", "content": json.dumps(
            {
            "step": "PLAN",
            "thought": "The user wants JavaScript code for adding 'n' numbers. This implies a function that can take multiple arguments or an array of numbers. I will provide a function that takes an array of numbers as input and returns their sum.",
            "content": "1. Define a JavaScript function that accepts an array of numbers. 2. Initialize a variable to store the sum to 0. 3. Iterate through the array, adding each number to the sum. 4. Return the final sum. 5. Provide an example usage of the function."
            }
        )},

    ]
)

print(response.choices[0].message.content)