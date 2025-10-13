"""
Zero Shot Prompting Example
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

#Zero Shot Prompting: Directly giving instruction to the model without any examples

SYSTEM_PROMPT = """
Don't answer questions other than coding. If user asks non-coding questions, respond with "I am a coding assistant. Please ask coding related questions only."

"""

response = client.chat.completions.create(

    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        # {"role": "user", "content": "Hey, translate word hello to hindi"},
        # {"role": "user", "content": "Hey,give python code for adding 2 numbers"},
        {"role": "user", "content": "Can you give me formula for a+b ^^ 2? "}
    ]
)

print(response.choices[0].message.content)