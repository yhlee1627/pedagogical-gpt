import streamlit as st
import pandas as pd
import plotly.express as px

from services.db_class import (
    create_class,
    fetch_all_classes,
    fetch_class_by_id,
    update_class_prompts
)
from services.db_user import fetch_students_by_class
from services.db_chat import fetch_conversation, fetch_conversation_list
from services.gpt_rubric import grade_conversation, save_evaluation_result, load_evaluation_result
from services.evaluation_stats import load_all_evaluation_results


def show_admin_page():
    st.title("🛠️ 관리자 페이지")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏫 학급 생성",
        "🛠️ 학급 관리",
        "📄 학생 개별 평가 보기",
        "📊 전체 평가 통계"
    ])

    # -------------------------------
    # 🏫 탭 1: 학급 생성
    # -------------------------------
    with tab1:
        st.subheader("🆕 새로운 학급 생성")

        name = st.text_input("학급명", placeholder="예: 6학년 1반")
        password = st.text_input("학급 비밀번호", type="password")
        system_prompt = st.text_area("📜 GPT system prompt", height=200)
        rubric_prompt = st.text_area("📋 GPT 평가 루브릭 프롬프트", height=250)

        if st.button("✅ 학급 생성"):
            if not name or not password or not system_prompt or not rubric_prompt:
                st.warning("모든 항목을 입력해 주세요.")
            else:
                success = create_class(name, password, system_prompt, rubric_prompt)
                if success:
                    st.success("✅ 학급이 성공적으로 생성되었습니다.")
                else:
                    st.error("❌ 학급 생성에 실패했습니다.")

    # -------------------------------
    # 🛠️ 탭 2: 학급 관리
    # -------------------------------
    with tab2:
        st.subheader("📋 학급 목록 및 프롬프트 관리")

        classes = fetch_all_classes()
        if not classes:
            st.info("아직 생성된 학급이 없습니다.")
            return

        df = pd.DataFrame(classes)
        st.dataframe(df[["class_id", "name", "created_by", "created_at"]], use_container_width=True)

        selected_class_name = st.selectbox("🔍 프롬프트 확인/수정할 학급 선택", df["name"].tolist())
        selected_data = df[df["name"] == selected_class_name].iloc[0]
        selected_class_id = selected_data["class_id"]

        st.markdown("#### 📜 현재 system prompt")
        st.code(selected_data["system_prompt"])

        st.markdown("#### 📋 현재 rubric prompt")
        st.code(selected_data["rubric_prompt"])

        edited_system_prompt = st.text_area("✏️ 수정할 system prompt", selected_data["system_prompt"], height=200)
        edited_rubric_prompt = st.text_area("✏️ 수정할 rubric prompt", selected_data["rubric_prompt"], height=250)

        if st.button("✅ 프롬프트 수정 저장"):
            success = update_class_prompts(selected_class_id, edited_system_prompt, edited_rubric_prompt)
            if success:
                st.success("✅ 프롬프트가 성공적으로 수정되었습니다.")
            else:
                st.error("❌ 수정에 실패했습니다.")

    # -------------------------------
    # 📄 탭 3: 학생 개별 평가 보기
    # -------------------------------
    with tab3:
        st.subheader("📂 학생 대화 기록 및 평가")

        classes = fetch_all_classes()
        class_dict = {cls["name"]: cls["class_id"] for cls in classes}

        selected_class_name = st.selectbox("학급 선택", list(class_dict.keys()), key="eval_class")
        selected_class_id = class_dict[selected_class_name]

        students = fetch_students_by_class(selected_class_id)
        if not students:
            st.info("해당 학급에 등록된 학생이 없습니다.")
            return

        student_id = st.selectbox("👤 학생 선택", students)

        chat_list = fetch_conversation_list(student_id)
        selected_chat = st.selectbox("💬 대화 선택", chat_list if chat_list else ["(대화 없음)"])

        if selected_chat and selected_chat != "(대화 없음)":
            chat_data = fetch_conversation(student_id, selected_chat)
            st.markdown(f"### 📁 대화 ID: `{selected_chat}`")

            for msg, role in chat_data:
                if role == "user":
                    st.markdown(f"**🧑‍🎓 {student_id}:** {msg}")
                elif role == "assistant":
                    st.markdown(f"**🤖 GPT:** {msg}")
                st.markdown("---")

            # GPT 자동 평가
            class_info = fetch_class_by_id(selected_class_id)
            rubric_prompt = class_info.get("rubric_prompt", "")

            if chat_data:
                if st.button("🧠 GPT 자동 평가"):
                    with st.spinner("GPT가 평가 중입니다..."):
                        user_only = [(m, r) for m, r in chat_data if r == "user"]
                        result = grade_conversation(user_only, rubric_prompt)
                        save_evaluation_result(
                            student_id=student_id,
                            class_id=selected_class_id,
                            conversation_id=selected_chat,
                            result=result
                        )
                    st.success("✅ 평가 결과 저장 완료")

            eval_result = load_evaluation_result(selected_chat)
            if eval_result:
                st.markdown("### 📊 GPT 평가 결과")
                for criterion, score in eval_result["scores"].items():
                    explanation = eval_result["explanations"].get(criterion, "")
                    st.markdown(f"- **{criterion}**: `{score}`점")
                    if explanation:
                        st.caption(f"📝 {explanation}")
                st.markdown("**총평:**")
                st.success(eval_result["summary"])

            else:
                st.info("이 대화는 아직 평가되지 않았습니다.")

    # -------------------------------
    # 📊 탭 4: 전체 평가 통계
    # -------------------------------
    with tab4:
        df = load_all_evaluation_results()

        if df.empty:
            st.info("아직 저장된 평가 결과가 없습니다.")
        else:
            score_columns = ["질문의 다양성", "질문의 깊이", "질문의 진전성", "자기주도성"]
            df[score_columns] = df[score_columns].astype(float)

            st.markdown("### ✅ 항목별 평균 점수")
            avg_scores = df[score_columns].mean().reset_index()
            avg_scores.columns = ["항목", "평균 점수"]

            fig = px.bar(avg_scores, x="항목", y="평균 점수", text="평균 점수",
                         color="항목", color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(textposition="outside")
            fig.update_layout(yaxis_range=[0, 5], height=400)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 👥 학생별 평가 테이블")
            st.dataframe(df, use_container_width=True)

            selected_person = st.selectbox("🔍 학생별 점수 보기", df["학생 ID"].unique())
            if selected_person:
                per_student_df = df[df["학생 ID"] == selected_person]
                for idx, row in per_student_df.iterrows():
                    st.markdown(f"#### 🎯 대화: {row['대화 ID']}")
                    scores = row[score_columns]
                    fig2 = px.bar(scores, x=scores.index, y=scores.values,
                                  text=scores.values, color=scores.index,
                                  color_discrete_sequence=px.colors.qualitative.Set3)
                    fig2.update_traces(textposition="outside")
                    fig2.update_layout(yaxis_range=[0, 5], height=300)
                    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # 🔓 로그아웃
    # -------------------------------
    st.markdown("---")
    if st.button("🔓 로그아웃"):
        for key in ["student_id", "class_id", "conversation_id", "system_prompt"]:
            st.session_state.pop(key, None)
        st.rerun()