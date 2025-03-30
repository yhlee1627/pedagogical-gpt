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

# ✅ 학급 생성 (rubric_prompt 포함)
def create_class(name, password, system_prompt, rubric_prompt, created_by="admin"):
    data = {
        "name": name,
        "password": password,
        "system_prompt": system_prompt,
        "rubric_prompt": rubric_prompt,
        "created_by": created_by,
        "created_at": datetime.utcnow().isoformat()
    }
    response = requests.post(f"{SUPABASE_URL}/rest/v1/classes", json=data, headers=HEADERS)
    return response.status_code == 201

# ✅ 전체 학급 불러오기
def fetch_all_classes():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/classes?select=*", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []

# ✅ 특정 class_id로 학급 정보 불러오기
def fetch_class_by_id(class_id):
    url = f"{SUPABASE_URL}/rest/v1/classes?class_id=eq.{class_id}&select=*"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return None

def update_class_prompts(class_id, new_system_prompt, new_rubric_prompt):
    url = f"{SUPABASE_URL}/rest/v1/classes?class_id=eq.{class_id}"
    data = {
        "system_prompt": new_system_prompt,
        "rubric_prompt": new_rubric_prompt
    }
    response = requests.patch(url, json=data, headers=HEADERS)
    return response.status_code == 204