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

def update_name(student_id, name):
    url = f"{SUPABASE_URL}/rest/v1/students?student_id=eq.{student_id}"
    data = { "name": name }
    res = requests.patch(url, json=data, headers=HEADERS)
    return res.status_code == 204

def update_password(student_id, old_password, new_password):
    # 먼저 기존 비밀번호 확인
    check_url = (
        f"{SUPABASE_URL}/rest/v1/students"
        f"?student_id=eq.{student_id}&password=eq.{old_password}&select=*"
    )
    check_res = requests.get(check_url, headers=HEADERS)
    if check_res.status_code != 200 or not check_res.json():
        return False  # 현재 비밀번호 불일치

    # 비밀번호 변경
    patch_url = f"{SUPABASE_URL}/rest/v1/students?student_id=eq.{student_id}"
    data = { "password": new_password }
    patch_res = requests.patch(patch_url, json=data, headers=HEADERS)
    return patch_res.status_code == 204