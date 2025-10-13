#lib
pip install boto3


# Set up AWS credentials (ensure these are set in your environment or ~/.aws/credentials)
# os.environ['AWS_ACCESS_KEY_ID'] = 'your-access-key-id'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-secret-access-key'
#os.environ['aws_session_token'] = 'your-session-token'  # if using temporary credentials
# os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # or your region


If you set environment variables, the boto3 library automatically reads them when creating the client. 
In your script, we do not need to manually fetch or 
pass the credentials—boto3 handles it internally.

or Use your AWS profile (already set up in ~/.aws/credentials)


Amazon Bedrock is the managed service where AWS hosts foundation models (Claude, Llama, Mistral, Titan, etc.) so you don’t have to deploy them yourself.

To interact with a model, you call the Bedrock Runtime API.

This API lets you invoke a model with your prompt/input and get back the model’s output (text, embeddings, or streaming tokens).

It is separate from the Bedrock Control Plane API, which is used for tasks like listing models, checking access, and managing model settings.

Bedrock Runtime = the inference layer.
It’s the actual part that sends your request to the model and streams back the response.


# Initialize the Bedrock client (replace 'bedrock-runtime' with the correct service name if needed)
# bedrock = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'))
# Invocation of model ID anthropic.claude-3-opus-20240229-v1:0 with on-demand throughput isn’t supported.
# Retry your request with the ID or ARN of an inference profile that contains this model.


# To see the model id with ARN, go to AWS Bedrock -> Chat/Text Playground -> Compare Mode -> View API Request
# It will give the AWS command to run it. Pick the model id from there.

#
"""