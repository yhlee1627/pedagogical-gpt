import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Railway 환경 또는 .env 파일에서 직접 가져오기
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ 필수 키 체크
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❗ Supabase 키가 설정되지 않았습니다.")
if not OPENAI_API_KEY:
    raise ValueError("❗ OpenAI API 키가 설정되지 않았습니다.")