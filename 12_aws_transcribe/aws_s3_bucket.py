import json
import re

from aws_base import AWSBase

class AWSBucket(AWSBase):
    def __init__(self, service_name='s3', aws_profile='hackathon', aws_region='us-east-1', language_code='en-US'):
        super().__init__(aws_profile, aws_region, language_code)
        self.aws_s3_client = self.session.client(service_name, region_name=self.aws_region)

    def create_bucket(self, bucket_name):
        # Logic to create an S3 bucket
        print(f"Creating S3 bucket: {bucket_name}")

    def delete_bucket(self, bucket_name):
        # Logic to delete an S3 bucket
        print(f"Deleting S3 bucket: {bucket_name}")

    def list_bucket_content(self, bucket_name, match_file_name=None):
        # List objects in the bucket
        response = self.aws_s3_client.list_objects_v2(Bucket=bucket_name)
        l = []
        if 'Contents' in response:
            print("S3 URIs in bucket:")
            for obj in response['Contents']:
                print(f"{obj['Key']}")

                if obj['Key'].endswith('.temp'):
                    continue

                if match_file_name and obj['Key'].startswith(match_file_name):
                    s3_uri = f"s3://{bucket_name}/{obj['Key']}"
                    print(s3_uri)
                    l.append(s3_uri)

                if not match_file_name:
                    s3_uri = f"s3://{bucket_name}/{obj['Key']}"
                    print(s3_uri)
                    l.append(s3_uri)
        else:
            print("No files found in bucket.")

        print("Ended Listing S3 buckets Content")
        return l


    def read_s3_json(self, s3_uri):
        # Parse bucket and key from s3://bucket/key
        match = re.match(r's3://([^/]+)/(.+)', s3_uri)
        if not match:
            raise ValueError("Invalid S3 URI format. Expected s3://bucket/key")

        bucket, key = match.groups()

        response = self.aws_s3_client.get_object(Bucket=bucket, Key=key)

        # Read and parse JSON
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)

        return data