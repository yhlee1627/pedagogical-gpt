from services.secrets import SUPABASE_URL, SUPABASE_KEY
import pandas as pd
import requests
import streamlit as st

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def load_all_evaluation_results():
    url = f"{SUPABASE_URL}/rest/v1/evaluations?select=*"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        st.error("❌ Supabase에서 평가 결과를 불러오지 못했습니다.")
        return pd.DataFrame()

    data = response.json()
    records = []

    for item in data:
        row = {
            "학생 ID": item["student_id"],
            "대화 ID": item["conversation_id"],
            "학급 ID": item.get("class_id", ""),
        }

        scores = item.get("scores", {})
        for key, value in scores.items():
            row[key] = float(value) if value.isdigit() else None

        records.append(row)

    return pd.DataFrame(records)