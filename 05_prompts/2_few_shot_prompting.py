"""
Few Shot Prompting Example
"""
from openai import OpenAI
import json

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['GEMINI_API_KEY']

client = OpenAI(
    api_key=token, #Gemini API key here
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

#Few Shot Prompting: We give a few examples to the model in the prompt to guide its response along with the instruction.

#The model is provided with a few examples before asking it to generate a response.
# This helps the model understand the desired format and content of the response.
# In reality, few shot prompt is used alot in real world applications to guide the model's behavior.

SYSTEM_PROMPT = """
Don't answer questions other than coding. If user asks non-coding questions, respond with "I am a coding assistant. Please ask coding related questions only."

Examples:

Q. Can you you translate word hello to hindi?
A. Sorry, I am a coding assistant. Please ask coding related questions only.

Q. Can you give formula for a+b ^^ 2?
A. Sorry, I am a coding assistant. Please ask coding related questions only.

Q. Can you give python code for adding 2 numbers?
A. Sure! Here is a simple Python code to add two numbers:
```python
def add_numbers(a, b):
    return a + b        
# Example usage
num1 = 5
num2 = 10
result = add_numbers(num1, num2)
print("The sum is:", result)    

"""

response = client.chat.completions.create(

    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        # {"role": "user", "content": "Hey, translate word hello to hindi"},
        {"role": "user", "content": "Hey,give python code for adding 2 numbers"},
        # {"role": "user", "content": "Can you give me formula for a+b ^^ 2? "}
    ]
)

print(response.choices[0].message.content)