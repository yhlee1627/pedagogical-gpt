from services.secrets import SUPABASE_URL, SUPABASE_KEY
import requests

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def authenticate_student(student_id, password, class_id):
    url = (
        f"{SUPABASE_URL}/rest/v1/students"
        f"?student_id=eq.{student_id}&password=eq.{password}&class_id=eq.{class_id}&select=*"
    )
    response = requests.get(url, headers=HEADERS)
    return response.status_code == 200 and len(response.json()) == 1

def fetch_students_by_class(class_id):
    url = f"{SUPABASE_URL}/rest/v1/students?class_id=eq.{class_id}&select=student_id"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return [item["student_id"] for item in res.json()]
    return []