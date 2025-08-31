# 🎙️ TalkMyResume

**TalkMyResume** is an AI-powered resume reviewer that goes beyond generic text analysis by delivering **voice-based, persona-driven feedback**.  
It helps candidates improve their resumes by allowing them to **hear reviews** in the voices of a **Career Coach, ATS system, or Recruiter**, making the feedback more **interactive, engaging, and actionable**.  

---

## 🚀 Features

- **Resume Parsing**: Extracts structured information (skills, education, work experience) from resumes using `pdfplumber` and Python parsing libraries.  
- **Persona-Based Reviews**:  
  - 🎤 **Career Coach** – Motivational and supportive feedback  
  - 🤖 **ATS System** – Keyword- and technical-focused insights  
  - 👔 **Recruiter** – Practical, shortlisting-oriented review  
- **AI Analysis**: Uses **Gemini Flash 1.5** for context-aware analysis of resumes.  
- **Voice Feedback**: Integrates with **Murf AI TTS** to generate natural-sounding, persona-modulated voices.  
- **Text + Audio Reports**: Provides detailed written feedback and downloadable **audio reviews (MP3)** or **PDF reports**.  
- **Scoring System**:  
  - ATS Compatibility Score  
  - Recruiter Attention Score  
  - Career Coach Improvement Score  
- **Interactive Experience**: Allows candidates to track improvements and visualize progress with before/after comparisons.  

---

## 🛠️ Tech Stack

- **Backend**: Python (`pdfplumber`, `PyMuPDF`, `transformers`, `scapy`)  
- **AI Engine**: Gemini Flash 1.5 (resume review & insights)  
- **Voice Synthesis**: [Murf AI](https://murf.ai) (text-to-speech with persona modulation)  
- **Frontend**: Streamlit (UI for uploading resumes and listening to reviews)  
- **Storage**: SQLite / MongoDB (optional for saving reviews and user progress)  

---

## ▶️ Demo

🔗 **Live App**: [TalkMyResume on Streamlit](https://talkmyresume-ashishlimitless.streamlit.app/)  
💻 **Source Code**: [GitHub Repo](https://github.com/DOMINATER007/TalkMyResume)  

---

## ⚙️ Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/DOMINATER007/TalkMyResume.git
   cd TalkMyResume

