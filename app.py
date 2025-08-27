import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in environment. Please set it in your .env file.")
else:
    genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    model = None

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")
st.title("🤖 TalentScout Hiring Assistant")
st.write("Hello! I'm your AI Hiring Assistant. I’ll collect your details and ask tailored tech questions.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are TalentScout, a hiring assistant for a tech recruitment agency. "
            "Your job: (1) Greet the candidate. "
            "Collect candidate details (Name, Email, Phone, Experience, Desired Position, Location, Tech Stack). "
            "Politely validate inputs (e.g., valid email/phone). "
            "Then ask 3-5 technical questions based on the candidate’s declared tech stack. "
            "Keep tone professional but friendly. "
            "If the user sends nonsense or irrelevant input, ask them to clarify. "
            "If they want to end (say bye/exit/quit/thanks), gracefully conclude. "
        )},
        {"role": "assistant", "content": "Hi there! I’m TalentScout, your hiring assistant. Can we start with your full name?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] in ["assistant", "user"]:
        st.chat_message(msg["role"]).write(msg["content"])

def is_valid_email(text: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", text))

def is_valid_phone(text: str) -> bool:
    return bool(re.match(r"^\+?[0-9\s\-]{7,15}$", text))

if prompt := st.chat_input("Type your message..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    exit_keywords = ["exit", "quit", "bye", "thank you", "goodbye", "close chat"]
    if any(k in prompt.lower() for k in exit_keywords):
        reply = "Thanks for chatting! We’ll review your details and contact you soon. 👋"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
        st.stop()

    if not prompt.strip():
        reply = "I didn’t receive any input. Could you please type your response again?"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
        st.stop()

    if len(prompt.split()) == 1 and not prompt.isalpha():
        reply = "Hmm, that doesn’t look like valid information. Could you please rephrase?"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
        st.stop()

    last_question = st.session_state.messages[-2]["content"].lower()
    if "email" in last_question and not is_valid_email(prompt):
        reply = "That doesn’t seem like a valid email. Can you re-enter it in the format `name@example.com`?"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
        st.stop()

    if "phone" in last_question and not is_valid_phone(prompt):
        reply = "That doesn’t look like a valid phone number. Please include country code if possible."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
        st.stop()

    history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])

    try:
        if model:
            response = model.generate_content(history_text)
            reply = response.text if response else "Sorry, I didn’t catch that."
        else:
            reply = "⚠️ AI model not available. Please check API key or try again later."
    except Exception as e:
        reply = f"⚠️ Oops, something went wrong: {str(e)}. Please try again."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
