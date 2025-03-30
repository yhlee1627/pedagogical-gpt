from services.secrets import SUPABASE_URL, SUPABASE_KEY
import requests
from datetime import datetime

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
'''
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
'''
def create_class(name, password, system_prompt, rubric_prompt, student_count=30, created_by="admin"):
    class_data = {
        "name": name,
        "password": password,
        "system_prompt": system_prompt,
        "rubric_prompt": rubric_prompt,
        "created_by": created_by,
        "created_at": datetime.utcnow().isoformat()
    }

    headers = HEADERS.copy()
    headers["Prefer"] = "return=representation"

    res = requests.post(f"{SUPABASE_URL}/rest/v1/classes", json=class_data, headers=headers)
    if res.status_code != 201 or not res.json():
        return False

    class_id = res.json()[0]["class_id"]
    return create_students_for_class(class_id, count=student_count)


def fetch_all_classes():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/classes?select=*", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []

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

def create_students_for_class(class_id, count=30, default_password="1234"):
    students = []
    for i in range(1, count + 1):
        student_id = f"s{str(i).zfill(2)}"
        students.append({
            "student_id": student_id,
            "password": default_password,
            "class_id": class_id,
            "created_at": datetime.utcnow().isoformat()
        })
    res = requests.post(f"{SUPABASE_URL}/rest/v1/students", json=students, headers=HEADERS)
    return res.status_code == 201