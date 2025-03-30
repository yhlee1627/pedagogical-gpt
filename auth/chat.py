import streamlit as st
from services.gpt_service import get_gpt_response
from services.db_chat import (
    generate_conversation_id,
    save_message,
    fetch_conversation_list,
    fetch_conversation
)

def show_sidebar():
    student_id = st.session_state.get("student_id")
    class_id = st.session_state.get("class_id")

    if not student_id or not class_id:
        st.warning("세션 정보가 손실되었습니다. 다시 로그인 해 주세요.")
        return

    st.markdown("## 👤 사용자 정보")
    st.markdown(f"**학번:** `{student_id}`")
    st.markdown("---")

    st.markdown("## 💬 대화 목록")

    chat_list = fetch_conversation_list(student_id)

    if st.button("🆕 새 대화 시작"):
        if student_id and class_id:
            st.session_state["conversation_id"] = generate_conversation_id(student_id)
            st.session_state["chat_history"] = []
            st.rerun()
        else:
            st.error("세션이 없습니다. 다시 로그인해주세요.")

    for chat_id in chat_list:
        if st.button(f"📁 {chat_id}"):
            st.session_state["conversation_id"] = chat_id
            messages = fetch_conversation(student_id, chat_id)
            st.session_state["chat_history"] = messages  # [(message, role)] 구조
            st.rerun()

    st.markdown("---")
    if st.button("🔓 로그아웃"):
        for key in ["student_id", "class_id", "conversation_id", "system_prompt", "chat_history"]:
            st.session_state.pop(key, None)
        st.rerun()

def show_chat_page():
    st.title("🤖 GPT 챗봇과 대화하기")

    student_id = st.session_state.get("student_id")
    class_id = st.session_state.get("class_id")
    conversation_id = st.session_state.get("conversation_id")

    if not student_id or not class_id:
        st.error("세션 정보가 유실되어 로그인 페이지로 돌아갑니다.")
        st.session_state["student_id"] = None
        st.rerun()

    if not conversation_id:
        st.info("왼쪽 사이드바에서 새 대화를 시작하거나 기존 대화를 선택해 주세요.")
        return

    history = st.session_state.get("chat_history", [])

    # ✅ 대화 출력
    for msg, role in history:
        if role == "user":
            st.markdown(f"🧑‍🎓 **나:** {msg}")
        elif role == "assistant":
            st.markdown(f"🤖 **GPT:** {msg}")
        st.markdown("---")

    # ✅ 입력 폼
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("GPT에게 질문하기:")
        submitted = st.form_submit_button("보내기")

        if submitted and user_input:
            with st.spinner("GPT가 답변 중입니다..."):
                response = get_gpt_response(user_input, history)

            # ✅ 기록에 추가
            history.append((user_input, "user"))
            history.append((response, "assistant"))
            st.session_state["chat_history"] = history

            # ✅ DB에도 저장
            save_message(student_id, class_id, conversation_id, user_input, "user")
            save_message(student_id, class_id, conversation_id, response, "assistant")

            st.rerun()