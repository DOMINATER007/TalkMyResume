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
2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)
3. Install dependencies
   ```bash
   pip install -r requirements.txt
4. Add API keys in .env file
   ```bash
   GEMINI_API_KEY=your_gemini_key
   MURF_API_KEY=your_murf_key
5. Run the Streamlit app
   ```bash
   streamlit run app.py

---
## Working

- Upload your resume (PDF/DOCX).
- Select the review persona (Career Coach / ATS / Recruiter).
- The system parses resume content and analyzes it using Gemini Flash 1.5.
- Feedback is generated as both text report and voice review (via Murf AI).
- Download your feedback in audio (MP3) or PDF format.

---
## 🔮 Future Roadmap & Scalability

- **Job Description Upload** → Compare resumes with job descriptions for ATS-tailored feedback.
- **Interview Prep Mode** → Generate mock interview questions based on resume content.
- **Multilingual Support** → Reviews in multiple languages for global candidates.
- **Smart Resume Editor** → Inline editing with AI-suggested improvements.
- **Gamified Progress Tracking** → Resume improvement badges (e.g., “ATS Friendly”, “Impact Driven”).
- **Integration APIs** → Provide APIs for career platforms, job portals, and universities.
- **Privacy Mode** → Local-only execution so no resume data leaves the device.
- **Custom Personas** → Add new review modes (e.g., Hiring Manager, Industry Expert).  

