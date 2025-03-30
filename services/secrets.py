import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ 안전하게 환경변수 불러오기 (Railway + 로컬 모두 대응)
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get("SUPABASE_API_KEY", os.getenv("SUPABASE_API_KEY"))
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# ✅ 필수 키 체크
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❗ Supabase 키가 설정되지 않았습니다.")
if not OPENAI_API_KEY:
    raise ValueError("❗ OpenAI 키가 설정되지 않았습니다.")