import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from aws_base import AWSBase

# Known teams
KNOWN_TEAMS = [
    "Portugal", "Spain", "Argentina", "Brazil", "France", "Germany", "Italy",
    "England", "Netherlands", "Belgium", "Uruguay", "Croatia", "Mexico"
]

class AWSBedRockAgent(AWSBase):
    def __init__(self, model_id=None, max_tokens=512, temperature=0.7,
                 service_name='bedrock-runtime', aws_profile='hackathon',
                 aws_region='us-east-1', language_code='en-US'):
        super().__init__(aws_profile, aws_region, language_code)
        self.model_id = model_id or 'arn:aws:bedrock:us-east-1:477345795103:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0'
        self.anthropic_version = 'bedrock-2023-05-31'
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = self.session.client(service_name, region_name=self.aws_region)

    @staticmethod
    def _predict_teams_from_commentary(segment_batch):
        teams_found = []
        for seg in segment_batch:
            text = seg['transcript']
            for team in KNOWN_TEAMS:
                if team in text and team not in teams_found:
                    teams_found.append(team)
            if len(teams_found) >= 2:
                break
        teamA = teams_found[0] if len(teams_found) > 0 else "Team A"
        teamB = teams_found[1] if len(teams_found) > 1 else "Team B"
        return teamA, teamB

    def _build_prompt(self, segment_batch):
        teamA, teamB = self._predict_teams_from_commentary(segment_batch)
        prompt_text = ""
        for seg in segment_batch:
            prompt_text += f"\nCommentary: \"{seg['transcript']}\" (Start: {seg['start_time']}, End: {seg['end_time']})"

        return f"""
                You are an advanced sports commentator AI generating **live interactive betting-style questions** based on football commentary segments.

                Instructions:
                1. For each commentary segment, generate **1-3 unique predictive questions**.
                2. Include a mix of:
                    - Match outcome predictions (Who will win? {teamA} or {teamB})
                    - Total goals in the match
                    - Team-specific goal predictions ({teamA} and {teamB})
                    - Famous player performance (e.g., Messi if Argentina is playing, Ronaldo if Portugal is playing)
                    - Scoreline predictions
                    - Player actions (goals, assists, cards)
                    - Event predictions (penalties, red/yellow cards)
                    - Timing-based predictions (e.g., next 5 minutes, first half, second half)
                3. For each question, provide:
                    - start_time, end_time (from the commentary segment)
                    - question text
                    - answer_type: "yes/no", "multiple_choice", or "count"
                    - answer: Yes/No, exact number, or choice
                    - explanation: reasoning **based strictly on the commentary segment**
                4. Ensure:
                    - No repeated questions or reworded variants
                    - Questions are realistic and contextually relevant
                    - JSON output is a **flat array of objects** (no nesting)

                Example output:
                [
                  {{
                    "startTime": 0.0,
                    "endTime": 10.0,
                    "question": "Who will win the match?",
                    "answerType": "multiple_choice",
                    "answer": "{teamA}",
                    "explanation": "{teamA} is dominating possession in this segment."
                  }},
                  {{
                    "startTime": 10.0,
                    "endTime": 20.0,
                    "question": "Will there be a penalty in the next 5 minutes?",
                    "answerType": "yes/no",
                    "answer": "No",
                    "explanation": "No significant fouls or defensive errors observed."
                  }}
                ]

                Here are the commentary segments to analyze:
                {prompt_text}
            """

    def _call_bedrock(self, segment_batch):
        prompt = self._build_prompt(segment_batch)
        body = {
            "anthropic_version": self.anthropic_version,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            contentType='application/json',
            accept='application/json'
        )
        response_body = response["body"].read().decode("utf-8")

        parsed_questions = self.parse_bedrock_json_response(json.loads(response_body))
        final_questions = []

        for q in parsed_questions:
            # print('Question raw:', q)
            # If "question" itself is a JSON array string → parse it
            if isinstance(q.get("question"), str):
                try:
                    inner = json.loads(q["question"])
                    if isinstance(inner, list):
                        final_questions.extend(inner)
                        continue
                    elif isinstance(inner, dict):
                        final_questions.append(inner)
                        continue
                except json.JSONDecodeError:
                    pass  # leave as-is if not parseable

            # If already a proper dict → keep it
            final_questions.append(q)

        return final_questions

    @staticmethod
    def parse_bedrock_json_response(bedrock_response):
        """
        Extract JSON array of questions from Bedrock Claude response.
        If parsing fails, attempt to sanitize before parsing.
        """
        text = bedrock_response['content'][0]['text']
        # print("Raw text:", text)

        # Remove code fences
        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)

        # Try to find the first JSON-looking block
        # match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)

        # non-greedy
        match = re.search(r'(\[.*?\]|\{.*?\})', text, re.DOTALL)

        if match:
            text = match.group(1)

        try:
            questions = json.loads(text)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            # Try some common fixes
            fixed = text.replace("'", '"')  # single → double quotes
            fixed = re.sub(r",\s*}", "}", fixed)  # remove trailing commas in objects
            fixed = re.sub(r",\s*]", "]", fixed)  # remove trailing commas in arrays
            questions = json.loads(fixed)

        if isinstance(questions, dict):
            questions = [questions]
        return questions

    def generate_questions_for_transcript(self, transcript_json, batch_size=5, max_workers=10, max_questions=100):
        audio_segments = transcript_json.get("results", {}).get("audio_segments", [])

        #1.sort by ascending order of start_time
        audio_segments = sorted(audio_segments, key=lambda x: x['start_time'])

        all_batches = [audio_segments[i:i + batch_size] for i in range(0, len(audio_segments), batch_size)]
        all_questions = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._call_bedrock, batch): batch for batch in all_batches}

            for future in as_completed(futures):
                batch_questions = future.result()
                print('Batch questions:', batch_questions)
                all_questions.extend(batch_questions)
                if len(all_questions) >= max_questions:
                    all_questions = all_questions[:max_questions]
                    break

        # 2. Ensure final questions are sorted by start_time
        all_questions.sort(key=lambda q: q['startTime'])

        """remove 30s gaping in questions from prompt and add the logic in final question"""
        final_questions = []
        last_time = -30
        for q in all_questions:
            if q['startTime'] - last_time >= 30:
                final_questions.append(q)
                last_time = q['startTime']

        return final_questions
