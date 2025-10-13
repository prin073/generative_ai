from openai import OpenAI

# need to add $5 to https://platform.openai.com/settings/organization/billing/overview to make it work
#create API token at https://platform.openai.com/settings/organization/api-keys
#https://ai.google.dev/gemini-api/docs/openai ==> gemini is compatible with openai api
import json

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['GEMINI_API_KEY']


client = OpenAI(
    api_key=token, #Gemini API key here
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

response = client.chat.completions.create(

    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            # "content": "Explain to me how AI works"
            "content": "Tell me about yourself"
        }
    ]
)

print(response.choices[0].message.content)