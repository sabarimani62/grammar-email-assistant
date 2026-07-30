"""
Grammar & Email Assistant — Streamlit + Hugging Face
------------------------------------------------------
A narrow-purpose support chatbot that ONLY does two things:
  1. Corrects grammar / sentences
  2. Helps draft emails

Built with:
- Streamlit (free UI + free hosting on Streamlit Community Cloud)
- Hugging Face Inference API (free tier, model runs on Hugging Face's servers)
"""

import os
import streamlit as st
from huggingface_hub import InferenceClient

# ---------------- Page setup ----------------
st.set_page_config(page_title="Grammar & Email Assistant", page_icon="📝")
st.title("📝 Grammar & Email Assistant")
st.caption("I only help with two things: fixing sentences and drafting emails.")

# ---------------- Hugging Face setup ----------------
# On Streamlit Cloud, set this in: App settings > Secrets
#   HF_TOKEN = "your_token_here"
HF_TOKEN = os.environ.get("HF_TOKEN") or st.secrets.get("HF_TOKEN", None)

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN, provider="auto")

SYSTEM_PROMPT = """You are a narrow-purpose support assistant.
You are ONLY allowed to do two things:
1. Correct grammar, spelling, and sentence structure when the user gives you a sentence or paragraph.
2. Help the user draft or improve professional emails.

Rules you must always follow:
- If the user asks for anything else (coding, general knowledge, jokes, advice, math, etc.),
  politely reply: "I'm only able to help with grammar correction and email drafting.
  Could you share a sentence to fix, or tell me what email you'd like help writing?"
- Do not answer unrelated questions even if the user insists.
- Keep replies clear, short, and easy to understand.
- When correcting text, show the corrected version, then briefly explain what you changed.
- When drafting an email, ask for missing details (recipient, purpose, tone) only if truly needed,
  otherwise just write a clean draft.
"""

# ---------------- Chat memory ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- Chat input ----------------
user_input = st.chat_input("Paste a sentence to fix, or describe the email you need...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build messages for the model
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages)

    with st.chat_message("assistant"):
        if not HF_TOKEN:
            reply = "⚠️ No Hugging Face token found. Please set HF_TOKEN in Secrets."
            st.markdown(reply)
        else:
            with st.spinner("Thinking..."):
                try:
                    response = client.chat_completion(
                        messages=api_messages,
                        max_tokens=500,
                        temperature=0.4,
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Sorry, something went wrong reaching the model: {e}"
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
