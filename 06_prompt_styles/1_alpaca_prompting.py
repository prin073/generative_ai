"""
This is a different prompting style than few shot, zero shot or chain of thought prompting.

05 styles can be converted to this. Below is one of the example of converting few shot to alpaca.
"""

#Prompt Styles

### Instructions: <SYSTEM_PROMPT>\n
### Input: <USER_QUERY>\n
### Response: \n

from openai import OpenAI
import json

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['GEMINI_API_KEY']


client = OpenAI(
    api_key=token,  # Gemini API key here
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

# Replace these with your actual values
SYSTEM_PROMPT = """You are an expert AI assistant that answers all types of question.

"""

USER_QUERY = "what is temperature=0 in LLMs?"

# Build prompt in the required Alpaca-style format
prompt = f"""
### Instructions: {SYSTEM_PROMPT}
### Input: {USER_QUERY}
### Response:\n
"""

#With `temperature=0`, the model will **always select the token with the absolute highest probability** (or highest logit score) as the next token.
# It does not consider any other options, no matter how close their probabilities might be.

# Call OpenAI API
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0
)

# Print assistant's reply
print(response.choices[0].message.content)