import requests
import streamlit as st
from datetime import datetime

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["api_key"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ✅ 메시지 저장
def save_message(student_id, class_id, conversation_id, message, role):
    data = {
        "student_id": student_id,
        "class_id": class_id,
        "conversation_id": conversation_id,
        "message": message,
        "role": role,
        "timestamp": datetime.utcnow().isoformat()
    }
    res = requests.post(f"{SUPABASE_URL}/rest/v1/chats", json=data, headers=HEADERS)
    return res.status_code == 201

# ✅ 특정 학생의 대화 목록 가져오기
def fetch_conversation_list(student_id):
    url = f"{SUPABASE_URL}/rest/v1/chats?student_id=eq.{student_id}&select=conversation_id,timestamp"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        conversation_ids = sorted(list({item["conversation_id"] for item in data}))
        return conversation_ids
    return []

# ✅ 특정 대화 불러오기 (전체 메시지)
def fetch_conversation(student_id, conversation_id):
    url = f"{SUPABASE_URL}/rest/v1/chats?student_id=eq.{student_id}&conversation_id=eq.{conversation_id}&select=message,role,timestamp"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        data = sorted(res.json(), key=lambda x: x["timestamp"])
        return [(m["message"], m["role"]) for m in data]
    return []

# ✅ 대화 ID 생성 (timestamp 기반)
def generate_conversation_id(student_id):
    now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"{student_id}_{now}"