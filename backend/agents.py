# agents.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import backend.prompts as prompts
import streamlit as st
# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = st.secrets("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found error")
# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def ats_agent(resume_text) -> str:
    prompt = prompts.ATS_PROMPT.format(resume_text=resume_text)
    response = model.generate_content(prompt)
    return response.text.strip()


def recruiter_agent(resume_text) -> str:
    prompt = prompts.RECRUITER_PROMPT.format(resume_text=resume_text)
    response = model.generate_content(prompt)
    return response.text.strip()


def career_coach_agent(resume_text) -> str:
    prompt = prompts.CAREER_COACH_PROMPT.format(resume_text=resume_text)
    response = model.generate_content(prompt)
    return response.text.strip()
