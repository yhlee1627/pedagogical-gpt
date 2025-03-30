import streamlit as st
st.set_page_config(page_title="PedagogicalGPT", layout="wide")

# ✅ 필요한 함수 import 추가
from auth.login import show_login_page
from auth.chat import show_chat_page, show_sidebar
from auth.admin import show_admin_page

# ✅ 세션 상태 초기화
default_session_values = {
    "student_id": None,
    "class_id": None,
    "conversation_id": None,
    "system_prompt": "",
    "chat_history": []
}
for key, default in default_session_values.items():
    st.session_state.setdefault(key, default)

# ✅ 라우팅
if st.session_state["student_id"] == "admin":
    show_admin_page()
elif st.session_state["student_id"]:
    with st.sidebar:
        show_sidebar()
    show_chat_page()
else:
    show_login_page()