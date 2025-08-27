import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from constant import QUESTIONS
from response import Response
from prompt import Prompt
from utils import is_valid_email, is_valid_phone

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
    st.session_state.messages = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "finished_questions" not in st.session_state:
    st.session_state.finished_questions = False

for msg in st.session_state.messages:
    if msg["role"] in ["assistant", "user"]:
        st.chat_message(msg["role"]).write(msg["content"])

idx = st.session_state.current_question
if idx < len(QUESTIONS):
    if not st.session_state.messages or st.session_state.messages[-1]["role"] == "user":
        current_question_text = QUESTIONS[idx]["question"]
        st.session_state.messages.append({"role": "assistant", "content": current_question_text})
        st.chat_message("assistant").write(current_question_text)

if prompt := st.chat_input("Type your response here..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    exit_keywords = ["exit", "quit", "bye", "thank you", "goodbye", "close chat"]
    if any(k in prompt.lower() for k in exit_keywords):
        reply = "Thanks for chatting! We’ll review your details and contact you soon. 👋"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
        st.stop()

    if not st.session_state.finished_questions:
        idx = st.session_state.current_question
        current_key = QUESTIONS[idx]["key"]

        if not prompt.strip():
            reply = "I didn’t receive any input. Please type your response again."
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
        elif current_key == "email" and not is_valid_email(prompt):
            reply = "That doesn’t seem like a valid email. Please enter in format: name@example.com"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
        elif current_key == "phone" and not is_valid_phone(prompt):
            reply = "That doesn’t look like a valid phone number. Please include country code if possible."
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
        else:
            st.session_state.answers[current_key] = prompt
            st.session_state.current_question += 1

            if st.session_state.current_question < len(QUESTIONS):
                next_question = QUESTIONS[st.session_state.current_question]["question"]
                st.session_state.messages.append({"role": "assistant", "content": next_question})
                st.chat_message("assistant").write(next_question)
            else:
                answers = st.session_state.answers
                summary = Response.summary_response(answers)
                st.session_state.messages.append({"role": "assistant", "content": summary})
                st.chat_message("assistant").write(summary)

                follow_up = (
                    "Would you like me to generate **technical interview questions** "
                    "based on the above information? (yes/no)"
                )
                st.session_state.messages.append({"role": "assistant", "content": follow_up})
                st.chat_message("assistant").write(follow_up)

                st.session_state.finished_questions = True

    else:
        if prompt.lower() in ["yes", "y"]:
            reply = "Great! Generating some tailored technical interview questions for you... 🔎"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)

            try:
                if model:
                    tech_prompt = Prompt.generate_tech_questions(st.session_state.answers)
                    response = model.generate_content(tech_prompt)
                    tech_questions = response.text if response else "⚠️ Could not generate questions."
                else:
                    tech_questions = "⚠️ Model not configured. Cannot generate questions."
            except Exception as e:
                tech_questions = f"⚠️ Error generating questions: {str(e)}"

            guide_msg = Prompt.tech_question_guide()
            st.session_state.messages.append({"role": "assistant", "content": guide_msg})
            st.chat_message("assistant").write(guide_msg)
            
            st.session_state.messages.append({"role": "assistant", "content": tech_questions})
            st.chat_message("assistant").write(tech_questions)
            
            eng_msg = Prompt.tech_end_message()
            st.session_state.messages.append({"role": "assistant", "content": eng_msg})
            st.chat_message("assistant").write(eng_msg)
            
        elif prompt.lower() in ["no", "n"]:
            reply = "Alright 👍 Thanks for sharing your details. Wishing you the best in your career journey! 🚀"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
            st.stop()
        else:
            reply = "Please reply with 'yes' or 'no'."
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
