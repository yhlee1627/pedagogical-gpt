import os
import json
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import requests

# ✅ 환경 변수 로드 및 키 설정
load_dotenv()
api_key = st.secrets["openai"]["openai_api_key"]  # secrets.toml 사용

if not api_key:
    raise ValueError("❗ OpenAI API 키가 설정되지 않았습니다.")

client = OpenAI(api_key=api_key)

# ✅ Supabase API 설정
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["api_key"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ✅ GPT 평가 요청
def grade_conversation(chat_data, rubric_prompt):
    # 🔹 학생 질문만 추출
    dialogue_text = ""
    for user_msg, _ in chat_data:
        dialogue_text += f"학생 질문: {user_msg}\n"

    # 🔹 GPT 메시지 구성
    messages = [
        {"role": "system", "content": rubric_prompt},
        {"role": "user", "content": dialogue_text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 필요 시 모델 변경
        messages=messages
    )

    content = response.choices[0].message.content

    # ✅ 응답 파싱
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

# ✅ 평가 결과 저장 → Supabase
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

# ✅ 평가 결과 불러오기 → Supabase
def load_evaluation_result(conversation_id):
    url = f"{SUPABASE_URL}/rest/v1/evaluations?conversation_id=eq.{conversation_id}&select=*"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return None