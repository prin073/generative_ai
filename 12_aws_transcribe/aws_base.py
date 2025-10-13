import boto3


class AWSBase:
    def __init__(self, aws_profile='hackathon', aws_region='us-east-1', language_code='en-US'):
        self.aws_profile = aws_profile
        self.aws_region = aws_region
        self.language_code = language_code
        self.session = boto3.Session(profile_name=self.aws_profile)