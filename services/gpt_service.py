import os
import json
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# ✅ 환경변수 로드
#load_dotenv()

# ✅ API 키 불러오기
api_key = st.secrets["openai"]["openai_api_key"]
#api_key = st.secrets["openai"].get("openai_api_key", os.getenv("OPENAI_API_KEY"))

# ✅ 키 확인
if not api_key:
    raise ValueError("❗ OpenAI API 키가 설정되지 않았습니다. .env 또는 secrets.toml을 확인하세요.")

# ✅ 클라이언트 생성
client = OpenAI(api_key=api_key)

# ✅ GPT 응답 함수
def get_gpt_response(prompt, history=None):
    if history is None:
        history = []

    # ✅ 세션에 저장된 system_prompt 사용
    system_prompt = st.session_state.get("system_prompt", "당신은 교육용 GPT입니다.")

    messages = [{"role": "system", "content": system_prompt}]

    for user, assistant in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 필요 시 gpt-3.5-turbo 등으로 변경 가능
        messages=messages
    )

    return response.choices[0].message.content