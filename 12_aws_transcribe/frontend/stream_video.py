# app.py
from flask import Flask, jsonify, request, render_template
import boto3
import os

app = Flask(__name__)

# Configure AWS credentials (can also use environment variables or IAM role)
AWS_REGION = "us-east-1"
S3_BUCKET = "internal-media-bucket"
session = boto3.Session(profile_name='hackathon')
s3_client = session.client(
    's3',
    region_name=AWS_REGION,
)

AUTHORIZED_USERS = ["prince.kumar@xperi.com"]

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.json
    user_email = data.get("email")
    video_key = data.get("video_key")

    if user_email not in AUTHORIZED_USERS:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': S3_BUCKET, 'Key': video_key},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        return jsonify({"url": presigned_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
