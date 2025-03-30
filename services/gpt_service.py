from services.secrets import OPENAI_API_KEY
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=OPENAI_API_KEY)

def get_gpt_response(prompt, history=None):
    if history is None:
        history = []

    system_prompt = st.session_state.get("system_prompt", "당신은 교육용 GPT입니다.")
    messages = [{"role": "system", "content": system_prompt}]

    for user, assistant in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content