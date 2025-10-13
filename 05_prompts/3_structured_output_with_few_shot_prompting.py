"""
Structured Few Shot Prompting Example
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

#Using few shots prompting we can bind the output format to be in a structured way like JSON, XML etc.

SYSTEM_PROMPT = """
Don't answer questions other than coding. If user asks non-coding questions, respond with "I am a coding assistant. Please ask coding related questions only."

Rule: 
- Strictly follow the output in the JSON format mentioned below.

Output Format:
{{
"code": "string" or null,
"explanation": "<explanation_of_code>"
"isCodingQuestion": boolean
}}

Examples:

Q. Can you you translate word hello to hindi?
A. {{"code": null, "explanation": "I am a coding assistant. Please ask coding related questions only.", "isCodingQuestion": false}}

Q. Can you give formula for a+b ^^ 2?
A. {{"code": null, "explanation": "I am a coding assistant. Please ask coding related questions only.", "isCodingQuestion": false}}

Q. Can you give python code for adding 2 numbers?
A. {{"code": "def add_numbers(a, b):    
                    return a + b
                # Example usage
                    num1 = 5
                    num2 = 10
                    result = add_numbers(num1, num2)
                    print("The sum is:", result)", 
                
    "explanation": "This function takes two numbers as input and returns their sum. The example usage demonstrates how to use the function to add two numbers and print the result.", "isCodingQuestion": true}} 

"""



response = client.chat.completions.create(

    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        # {"role": "user", "content": "Hey, translate word hello to hindi"},
        # {"role": "user", "content": "Hey,give python code for adding 2 numbers"},
        {"role": "user", "content": "Hey,give js code for adding 2 numbers"},
        # {"role": "user", "content": "Can you give me formula for a+b ^^ 2? "}
    ]
)

print(response.choices[0].message.content)