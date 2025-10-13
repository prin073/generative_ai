from aws_transcriber import AWSTranscriber


if __name__ == "__main__":
    s3_bucket_name = 'bucket-hack-agentic-avenger'
    video_file_name = 'FULL MATCH Portugal v Spain  2018 FIFA World Cup.mp4'
    local_output_file = 'transcript/portugal_vs_spain_2018_wc'

    # Unique job name
    client_transcribe = AWSTranscriber()
    client_transcribe.get_transcript(s3_bucket_name=s3_bucket_name, video_file_name=video_file_name, local_output_file=local_output_file)




