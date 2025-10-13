import boto3
import json

session = boto3.Session(profile_name='hackathon')
bedrock = session.client('bedrock-runtime', region_name='us-east-1')

# Models
# MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0' #working
# MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0' #working

MODEL_ID = 'arn:aws:bedrock:us-east-1:477345795103:inference-profile/us.anthropic.claude-opus-4-20250514-v1:0'



# MODEL_ID = 'anthropic.claude-3-opus-20240229-v1:0'

# Request body
body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 256,
    "temperature": 0.2,
    "messages": [
        {
            "role": "user",
            "content": "Write Python code to add two numbers."
        }
    ]
}

# Call the model
response = bedrock.invoke_model(
    modelId=MODEL_ID,
    body=json.dumps(body),            #must use json.dumps, not str()
    contentType="application/json",
    accept="application/json"
)

# Parse and print the result
result = json.loads(response['body'].read())
print("Claude's response:")
print(result["content"][0]["text"])


