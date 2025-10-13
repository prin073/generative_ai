import json
import re
import time
import requests
from aws_base import AWSBase

class AWSTranscriber(AWSBase):
    def __init__(self, service_name='transcribe', aws_profile='hackathon', aws_region='us-east-1', language_code='en-US'):
        super().__init__(aws_profile, aws_region, language_code)
        self.aws_transcribe_client = self.session.client(service_name, region_name=self.aws_region)
        self.job_name = None
        self.job = None
        self.job_status = None
        

    def start_transcribe_job(self, s3_bucket_name, video_file_name, media_format, output_bucket):
        # transcribe job name will be used as output folder name if output bucket is provided
        folder_name = re.sub(r'\s+', '_', video_file_name).lower().split('.')[0]
        self.job_name = f"{folder_name}_{int(time.time())}"

        # S3 URL of your video
        media_uri = f's3://{s3_bucket_name}/{video_file_name}'
        media = {'MediaFileUri': media_uri}

        if output_bucket:
            # Start transcription job with output bucket
            self.aws_transcribe_client.start_transcription_job(
                TranscriptionJobName=self.job_name,
                Media=media,
                MediaFormat=media_format,  # change if your file is mp3, wav, etc.
                LanguageCode=self.language_code,  # change to your language
                OutputBucketName=output_bucket  # to store transcript in S3
            )
        else:
            # Start transcription job
            self.aws_transcribe_client.start_transcription_job(
                TranscriptionJobName=self.job_name,
                Media=media,
                MediaFormat=media_format,  # change if your file is mp3, wav, etc.
                LanguageCode=self.language_code,  # change to your language
            )

        print(f"Started transcription job: {self.job_name}")

    def poll_transcribe_job(self, poll_interval=30, max_attempts=60):
        # Polling for job completion
        attempts = 0
        while True and attempts < max_attempts:
            status = self.aws_transcribe_client.get_transcription_job(TranscriptionJobName=self.job_name)
            self.job = status['TranscriptionJob']
            self.job_status = self.job['TranscriptionJobStatus']
            if self.job_status in ['COMPLETED', 'FAILED']:
                print(f"Transcription job {self.job_name} finished with status: {status}")
                return self.job_status
            print(f"Transcription job {self.job_name} is still in progress. Checking again in {poll_interval} seconds...")
            attempts += 1
            time.sleep(poll_interval)
        return None

    def get_transcript_url(self):
        if self.job_status == 'COMPLETED':
            transcript_file_uri = self.job['Transcript']['TranscriptFileUri']
            print(f"Transcript URL: {transcript_file_uri}")
            return transcript_file_uri
        else:
            print("Transcription job did not complete successfully in max attempts.")
            return None

    def fetch_transcript_from_uri(self, transcript_file_uri, output_file, save_local=True):
        transcript_json, transcript_text = dict(), ''
        if self.job_status == 'COMPLETED' and transcript_file_uri:
            print(f"Transcript available at: {transcript_file_uri}")

            # Download transcript JSON
            response = requests.get(transcript_file_uri)
            transcript_json = response.json()

            # Extract transcript text
            transcript_text = transcript_json['results']['transcripts'][0]['transcript']
            print("Transcript:\n", transcript_text)

            # Save locally if needed
            if save_local:

                txt_output_file = f'{output_file}.txt'
                with open(txt_output_file, 'w', encoding='utf-8') as f:
                    f.write(transcript_text)
                print(f"Transcript saved as {txt_output_file}")

                json_output_file = f'{output_file}.json'
                with open(json_output_file, 'w') as f:
                    json.dump(transcript_json, f, indent=4)

                print(f"Transcript saved as {json_output_file}")
        else:
            print(f"Transcription failed with job_status: {self.job_status} and transcript_file_uri: {transcript_file_uri}")

        return transcript_json, transcript_text

    def delete_transcribe_job(self):
        if self.job_name:
            self.aws_transcribe_client.delete_transcription_job(TranscriptionJobName=self.job_name)
            print(f"Deleted transcription job: {self.job_name}")
        else:
            print(f"Deletion unsuccessful as transcription job is not provided")


    def get_transcript(self, s3_bucket_name, video_file_name, local_output_file, media_format='mp4', output_bucket=None, poll_interval=30, max_attempts=60,
                       save_local=True):
        # Start transcription job
        self.start_transcribe_job(s3_bucket_name, video_file_name, media_format=media_format, output_bucket=output_bucket)

        # Wait for job to complete
        self.poll_transcribe_job(poll_interval=poll_interval, max_attempts=max_attempts)

        # Get transcript URL
        transcript_url = self.get_transcript_url()

        # Fetch and save transcript
        json_transcript, text_transcript = self.fetch_transcript_from_uri(transcript_url, output_file=local_output_file, save_local=save_local)

        return json_transcript, text_transcript
