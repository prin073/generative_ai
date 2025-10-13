import json
import os
import re
import time

from flask import Flask, jsonify, request
from aws_transcriber import AWSTranscriber
from aws_s3_bucket import AWSBucket
from aws_bedrock_agent import AWSBedRockAgent

app = Flask(__name__)
input_s3_bucket_name = 'bucket-hack-agentic-avenger'
output_s3_bucket_name = 'output-bucket-hack-agentic-avenger'
# video_file_name = 'FULL MATCH Portugal v Spain  2018 FIFA World Cup.mp4'


@app.route('/')
def index():
    return "Agentic Hackathon Service is Running!"

@app.route('/transcript/start/<video_file_name>', methods=['GET'])
def start_transcript(video_file_name):
    client_transcribe = AWSTranscriber()
    json_transcript, text_transcript = client_transcribe.get_transcript(s3_bucket_name=input_s3_bucket_name, video_file_name=video_file_name,
                                                                        local_output_file=None, save_local=False, output_bucket=output_s3_bucket_name)



@app.route('/transcript/<video_file_name>', methods=['GET'])
def get_transcript_from_bucket(video_file_name):
    """returns latest transcript file matching video_file_name from output_s3_bucket_name"""
    output_file_name = re.sub(r'\s+', '_', video_file_name).lower().split('.')[0]
    print(f"output_file_name: {output_file_name}")
    client_s3 = AWSBucket()
    l = client_s3.list_bucket_content(output_s3_bucket_name, match_file_name=output_file_name)
    l.sort(reverse=True)

    """read output bucket matching latest transcript"""
    transcript_json =  client_s3.read_s3_json(l[0])

    output_dir = 'transcripts/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    return transcript_json


@app.route('/questions/<video_file_name>', methods=['GET'])
def generate_questions_for_transcript(video_file_name):
    """Generates interactive questions for a transcript"""
    output_file_name = re.sub(r'\s+', '_', video_file_name).lower().split('.')[0]
    t = int(time.time())
    # Reuse the existing route logic
    transcript_json = get_transcript_from_bucket(video_file_name)

    # Now generate questions using AWS Bedrock
    # Assuming you have a function `generate_questions_for_segments` which takes transcript_data
    # and returns a list of questions

    bedrock_agent = AWSBedRockAgent(max_tokens=1024, temperature=0.7)

    start_time = time.time()
    questions = bedrock_agent.generate_questions_for_transcript(transcript_json, batch_size=30, max_workers=3, max_questions=50)
    end_time = time.time()

    print(f"Generated {len(questions)} questions in {end_time - start_time:.2f} seconds")
    output_dir = 'questions'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with open(f"{output_dir}/{output_file_name}-{t}.json", "w") as f:
        json.dump(questions, f, indent=2)

    return jsonify({"video_file_name": video_file_name, "questions": questions})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)