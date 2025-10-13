from openai import OpenAI
from dotenv import load_dotenv

# need to add $5 to https://platform.openai.com/settings/organization/billing/overview to make it work
#create API token at https://platform.openai.com/settings/organization/api-keys

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(

    model="gpt-4o-mini",
    messages=[
        # {"role": "system", "content": "You are a helpful assistant that helps with coding tasks."},
        {"role": "user", "content": "Hey There"}
    ]
)

print(response.choices[0].message.content)