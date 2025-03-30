from services.secrets import SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY
import re
import requests
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key=OPENAI_API_KEY)

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def grade_conversation(chat_data, rubric_prompt):
    dialogue_text = ""
    for user_msg, _ in chat_data:
        dialogue_text += f"학생 질문: {user_msg}\n"

    messages = [
        {"role": "system", "content": rubric_prompt},
        {"role": "user", "content": dialogue_text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    content = response.choices[0].message.content

    scores = {}
    explanations = {}
    summary = ""
    current_criterion = ""

    for line in content.strip().splitlines():
        line = line.strip()
        if re.match(r"^\d+\.", line):
            match = re.match(r"\d+\.\s*(.+?):\s*(\d+)", line)
            if match:
                criterion = match.group(1).strip()
                score = match.group(2).strip()
                scores[criterion] = score
                current_criterion = criterion
        elif line.startswith("설명:") and current_criterion:
            explanations[current_criterion] = line.replace("설명:", "").strip()
        elif line.startswith("총평:"):
            summary = line.replace("총평:", "").strip()

    return {
        "scores": scores,
        "explanations": explanations,
        "summary": summary
    }

def save_evaluation_result(student_id, class_id, conversation_id, result):
    data = {
        "student_id": student_id,
        "class_id": class_id,
        "conversation_id": conversation_id,
        "scores": result["scores"],
        "explanations": result["explanations"],
        "summary": result["summary"],
        "created_at": datetime.utcnow().isoformat()
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/evaluations",
        json=data,
        headers=HEADERS
    )
    return response.status_code == 201

def load_evaluation_result(conversation_id):
    url = f"{SUPABASE_URL}/rest/v1/evaluations?conversation_id=eq.{conversation_id}&select=*"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return None