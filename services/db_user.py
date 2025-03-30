import requests
import streamlit as st

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["api_key"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ✅ 학생 로그인 인증
def authenticate_student(student_id, password, class_id):
    url = (
        f"{SUPABASE_URL}/rest/v1/students"
        f"?student_id=eq.{student_id}&password=eq.{password}&class_id=eq.{class_id}&select=*"
    )
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200 and len(response.json()) == 1

def fetch_students_by_class(class_id):
    url = f"{st.secrets['supabase']['url']}/rest/v1/students?class_id=eq.{class_id}&select=student_id"
    headers = {
        "apikey": st.secrets['supabase']['api_key'],
        "Authorization": f"Bearer {st.secrets['supabase']['api_key']}"
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return [item["student_id"] for item in res.json()]
    return []