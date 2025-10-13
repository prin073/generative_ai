from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage
import boto3

# boto3 Bedrock runtime client
session = boto3.Session(profile_name='hackathon')
bedrock_client = session.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"   # adjust region
)

# Models(langchain doesn't support ARN based model, use boto3 instead)
MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0' #working
# MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0' #working


# Wrap in LangChain's ChatBedrock
llm = ChatBedrock(
    client=bedrock_client,
    model_id=MODEL_ID,
)


# Send a message
response = llm([HumanMessage(content="Write a short poem about soccer.")])

print(response.content)
