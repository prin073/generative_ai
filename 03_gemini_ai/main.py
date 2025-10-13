from google import genai
import json

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['GEMINI_API_KEY']

client = genai.Client(
    api_key=token
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)