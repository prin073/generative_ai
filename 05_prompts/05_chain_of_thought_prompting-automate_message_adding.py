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
PLAN: {"step": "PLAN",  "content": "Seems user is interested in solving a mathematical expression."}
PLAN: {"step": "PLAN", "content": "I understand that I need to solve the expression step by step."}
PLAN: {"step": "PLAN", "content": "The question is asking to solve the mathematical expression 2+3*5/10."}
PLAN: {"step": "PLAN", "content": "I need to follow BODMAS to solve it correctly."}
PLAN: {"step": "PLAN", "content": "To solve the expression 2+3*5/10, I will first handle the multiplication and division from left to right, and then perform the addition.", 
PLAN: {"step": "PLAN", "content": "1. Calculate 3*5 = 15. 2. Calculate 15/10 = 1.5. 3. Finally, add 2 + 1.5."}
OUTPUT: {"step": "OUTPUT", "content": "The final answer is 3.5."}
"""
#initialize messages list
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_input = input("👉:")
messages.append({"role": "user", "content": user_input})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=messages
    )

    assistant_raw_message = response.choices[0].message.content

    # Add the assistant's message(raw string) to the conversation history
    messages.append({"role": "assistant", "content": assistant_raw_message})

    # Parse the assistant's message to extract the step
    assistant_parsed_message = json.loads(assistant_raw_message)
    step = assistant_parsed_message.get("step")

    if step == "START":
        # Continue the loop to get the next step from the assistant
        print("🔥:", assistant_parsed_message.get("content"))
        continue

    elif step == "PLAN":
        # Continue the loop to get the next step from the assistant
        print("🧠:", assistant_parsed_message.get("content"))
        continue

    elif step == "OUTPUT":
        print("🧰:", assistant_parsed_message.get("content"))
        break
