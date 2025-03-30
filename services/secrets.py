import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Supabase 설정
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get("SUPABASE_API_KEY", os.getenv("SUPABASE_API_KEY"))

# ✅ OpenAI 설정
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# ✅ 필수 키 확인
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❗ Supabase 환경변수가 설정되지 않았습니다.")
if not OPENAI_API_KEY:
    raise ValueError("❗ OpenAI API 키가 설정되지 않았습니다.")