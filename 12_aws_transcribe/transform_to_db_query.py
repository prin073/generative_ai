import json
import time
from asyncore import write

with open('questions/full_match_portugal_v_spain_2018_fifa_world_cup-1760085032.json', 'r') as f:
    json_data = json.load(f)


queries = ''
for i, q in enumerate(json_data, start=1):
    display_duration = q["endTime"] - q["startTime"]
    sql = f"""
    INSERT INTO livebetting.questions
        (correct_answer, display_at_second, display_duration, question_text, match_id, is_resolved)
    VALUES
        ('{q['answer']}', {q['startTime']}, {round(display_duration, 2)}, '{q['question'].replace("'", "''")}', 6, 0);
    """
    queries += f'{sql}\n\n'
    print(sql)
    print('\n')

t = int(time.time())
with open(f'query/query-{t}.txt', 'w') as f:
    f.write(queries)