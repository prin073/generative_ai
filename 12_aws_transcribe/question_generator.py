import json
import openai  # For Bedrock, you can use boto3 client as well
import random

# ----------------------------
# CONFIG: Set your API or Bedrock client
# ----------------------------
# Example for OpenAI-style usage (replace with Bedrock client if needed)
openai.api_key = "YOUR_API_KEY"

# ----------------------------
# Load your transcript JSON
# ----------------------------
with open("transcript.json", "r") as f:
    transcript_data = json.load(f)

# ----------------------------
# Function to generate questions for a single transcript segment
# ----------------------------
def generate_questions(segment):
    start = segment.get("start_time")
    end = segment.get("end_time")
    text = segment.get("transcript")

    prompt = f"""
You are a sports commentator AI. 
Given the soccer match commentary below, generate 1-2 **predictive and interactive questions** for viewers.
Focus on engagement: e.g., "Will the match go to penalty?", "How many goals will be scored?", "If a player scores now, will they score again?"
Keep the questions short and relevant to the commentary segment.
Output in JSON with "start_time", "end_time", and "question".

Commentary: "{text}"
Start_time: {start}, End_time: {end}
"""

    # ----------------------------
    # Call LLM
    # ----------------------------
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with Bedrock model if using AWS
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.8
    )

    # Extract text
    answer_text = response['choices'][0]['message']['content']

    # Attempt to parse as JSON
    try:
        questions = json.loads(answer_text)
    except:
        # If LLM returns plain text, wrap manually
        questions = [{"start_time": start, "end_time": end, "question": answer_text.strip()}]

    return questions

# ----------------------------
# Generate questions for all segments
# ----------------------------
all_questions = []
for segment in transcript_data:
    qs = generate_questions(segment)
    all_questions.extend(qs)

# ----------------------------
# Save output
# ----------------------------
with open("interactive_questions.json", "w") as f:
    json.dump(all_questions, f, indent=2)

print("Interactive questions saved to interactive_questions.json")
