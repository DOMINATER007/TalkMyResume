import streamlit as st
import requests
import os
import glob
import backend.resume_parser as parser
import backend.prompts as prompts
import json
# assuming parser.py has parse_resume(path)

# Page config
st.set_page_config(page_title="Talk My Resume", layout="centered")

# CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #7c3aed; /* Purple */
        text-align: center;
        margin-bottom: -10px;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #374151;
        margin-bottom: 30px;
    }
    .stTextInput > div > div > input {
        text-align: left;
    }
    .stButton > button {
        background-color: #7c3aed;
        color: white;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Title

st.markdown('<div class="title">Talk My Resume...</div>',
            unsafe_allow_html=True)

# Subtitle
st.markdown(
    '<div class="subtitle">An AI-powered vocal assistant that reviews resumes in distinct tones — such as a recruiter’s perspective or a career coach’s guidance.</div>',
    unsafe_allow_html=True
)
sample_dir = "data/sample_resumes"
output_audio_dir = "data/output_audio"


def clear_directory(directory):
    """Delete all files in the given directory"""
    files = glob.glob(os.path.join(directory, "*"))
    for f in files:
        try:
            os.remove(f)
            print(f"Deleted: {f}")
        except IsADirectoryError:
            print(f"Skipping directory: {f}")


# Clear both
clear_directory(sample_dir)
clear_directory(output_audio_dir)
# Create folder for resumes
SAMPLE_DIR = "data/sample_resumes"
os.makedirs(SAMPLE_DIR, exist_ok=True)

# Helper functions


def save_uploaded_file(uploaded_file):
    file_path = os.path.join(SAMPLE_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def download_file_from_url(url):
    file_name = url.split("/")[-1] or "resume.pdf"
    file_path = os.path.join(SAMPLE_DIR, file_name)
    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)
    return file_path


# Input Section
st.write("### Enter PDF URL or upload a file:")


pdf_url = st.text_input(" ", placeholder="https://example.com/resume.pdf")

st.write("##### OR ")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

name = st.text_input("What's your name?")

options = ["ATS", "Recruiter", "Career Coach"]
tone = st.selectbox("Select Review Tone", options, index=1)

# Button
if st.button("Generate Review", use_container_width=True):
    file_path = None

    # Case 1: Uploaded file
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"✅ PDF GOT UPLOADED.. Generating AI voice review...")

    # Case 2: URL
    elif pdf_url.strip():
        try:
            file_path = download_file_from_url(pdf_url)
            st.success(
                f"✅ Downloaded PDF from URL into sample_resumes/: {file_path}")
        except Exception as e:
            st.error(f"⚠️ Error downloading file: {e}")

    # If we have a file path, run parser
    if file_path:
        file_path = os.path.abspath(file_path)
        with st.spinner("⏳ Parsing resume..."):
            parsed_data = parser.parse_resume(file_path)
            # print(json.dumps(parsed_data, indent=4))
        if options:
            with st.spinner("⏳ Generating AI review..."):
                if tone == "ATS":
                    from backend.agents import ats_agent
                    from backend.murf_api import ats_voice
                    review = ats_agent(parsed_data)
                    audio_path = ats_voice(review, name)
                elif tone == "Recruiter":
                    from backend.agents import recruiter_agent
                    from backend.murf_api import recruiter_voice
                    review = recruiter_agent(parsed_data)
                    audio_path = recruiter_voice(review, name)
                else:
                    from backend.agents import career_coach_agent
                    from backend.murf_api import career_coach_voice
                    review = career_coach_agent(parsed_data)
                    audio_path = career_coach_voice(review, name)
            st.success("✅ AI review generated!")
            with st.expander("▶️ Play Audio Review"):
                audio_file = open(audio_path, "rb")
                audio_bytes = audio_file.read()

                # Play audio
                st.audio(audio_bytes, format="audio/mp3")

                # Download option
                st.download_button(
                    label="⬇️ Download Audio",
                    data=audio_bytes,
                    file_name="review_audio.mp3",
                    mime="audio/mp3"
                )

            with st.expander("🗒️ Text Review"):
                st.info(review)

# st.markdown("### 🗒️ AI Review:")
# st.info(review)

else:
    st.error("⚠️ Please provide a PDF URL or upload a file.")
