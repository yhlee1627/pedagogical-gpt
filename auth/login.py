import streamlit as st
from services.db_user import authenticate_student
from services.db_class import fetch_all_classes, fetch_class_by_id

def show_login_page():
    st.title("🔐 GPT 챗봇 로그인")

    # ✅ 관리자 로그인
    with st.expander("🔑 관리자 로그인"):
        with st.form("admin_login"):
            admin_id = st.text_input("👤 관리자 ID", key="admin_id")
            admin_pw = st.text_input("🔐 비밀번호", type="password", key="admin_pw")
            admin_submit = st.form_submit_button("로그인")

            if admin_submit and admin_id == "admin":
                st.session_state["student_id"] = "admin"
                #st.experimental_rerun()
                st.rerun()

    # ✅ 학급 정보 불러오기
    classes = fetch_all_classes()
    if not classes:
        st.warning("⚠️ 아직 생성된 학급이 없습니다.")
        return

    class_options = {cls["name"]: cls["class_id"] for cls in classes}

    # ✅ 학생 로그인
    with st.form("student_login"):
        st.subheader("👩‍🎓 학생 로그인")

        class_name = st.selectbox("🏫 학급 선택", list(class_options.keys()))
        class_id = class_options[class_name]
        student_id = st.text_input("👤 학번")
        password = st.text_input("🔑 비밀번호", type="password")

        submitted = st.form_submit_button("로그인")

        if submitted:
            if authenticate_student(student_id, password, class_id):
                st.session_state["student_id"] = student_id
                st.session_state["class_id"] = class_id

                class_info = fetch_class_by_id(class_id)
                st.session_state["system_prompt"] = class_info.get("system_prompt", "")
                #st.experimental_rerun()
                st.rerun()
            else:
                st.error("❌ 학번 또는 비밀번호가 올바르지 않습니다.")