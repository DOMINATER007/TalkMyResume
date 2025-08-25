# backend/murf_api.py
import os
import re
import requests
from murf import Murf
from murf.core.api_error import ApiError
from dotenv import load_dotenv

# ---------- Setup ----------
# Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
API_KEY = os.getenv("MURF_API_KEY")
client = Murf(api_key=API_KEY)

# Output folder fixed to ../data/output_audio
BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "data", "output_audio"))
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------- Helpers ----------
def _safe_name(name):
    """Sanitize name for filenames."""
    return re.sub(r"[^A-Za-z0-9_\-]+", "_", name.strip()) or "default"


def _save_from_url(url, path):
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    with open(path, "wb") as f:
        f.write(resp.content)


def _tts_generate(text, voice_id, fmt="MP3", channel_type=None,
                  sample_rate=None, style=None, rate=None, pitch=None):
    """Wrapper around Murf SDK generate()."""
    if not API_KEY:
        raise RuntimeError("MURF_API_KEY is not set in environment.")

    kwargs = {
        "text": text,
        "voice_id": voice_id,
        "format": fmt,
    }
    if channel_type is not None:
        kwargs["channel_type"] = channel_type
    if sample_rate is not None:
        kwargs["sample_rate"] = sample_rate
    if style is not None:
        kwargs["style"] = style
    if rate is not None:
        kwargs["rate"] = rate
    if pitch is not None:
        kwargs["pitch"] = pitch

    try:
        res = client.text_to_speech.generate(**kwargs)
        return res.audio_file
    except ApiError as e:
        # Retry without style if unsupported
        if style is not None:
            kwargs.pop("style", None)
            res = client.text_to_speech.generate(**kwargs)
            return res.audio_file
        raise RuntimeError(f"Murf API error: {e.status_code} {e.body}")


# ---------- Category Functions ----------
def recruiter_voice(text, name="default"):
    """Recruiter — clear, professional."""
    safe = _safe_name(name)
    out_path = os.path.join(OUTPUT_DIR, f"recruiter_{safe}.mp3")

    audio_url = _tts_generate(
        text=text,
        voice_id="en-US-terrell",
        fmt="MP3",
        channel_type="STEREO",
        sample_rate=44100,
        style="Newscast",
        rate=0,
        pitch=0
    )
    _save_from_url(audio_url, out_path)
    return out_path


def ats_voice(text, name="default"):
    """ATS — robotic, monotone."""
    safe = _safe_name(name)
    out_path = os.path.join(OUTPUT_DIR, f"ats_{safe}.mp3")

    audio_url = _tts_generate(
        text=text,
        voice_id="en-US-natalie",
        fmt="MP3",
        channel_type="MONO",
        sample_rate=24000,
        style="Narration",
        rate=-10,
        pitch=-5
    )
    _save_from_url(audio_url, out_path)
    return out_path


def career_coach_voice(text, name="default"):
    """Career coach — motivational, friendly."""
    safe = _safe_name(name)
    out_path = os.path.join(OUTPUT_DIR, f"coach_{safe}.mp3")

    audio_url = _tts_generate(
        text=text,
        voice_id="en-US-ariana",
        fmt="MP3",
        channel_type="STEREO",
        sample_rate=44100,
        style="Conversational",
        rate=8,
        pitch=6
    )
    _save_from_url(audio_url, out_path)
    return out_path


# ---------- Unified ----------
def generate_voice(category, text, name="default"):
    """Choose recruiter / ats / coach."""
    key = category.strip().lower()
    if key == "recruiter":
        return recruiter_voice(text, name)
    if key == "ats":
        return ats_voice(text, name)
    if key in {"coach", "career_coach"}:
        return career_coach_voice(text, name)
    raise ValueError("Unknown category: use recruiter, ats, or coach")


# # ---------- Example ----------
# if __name__ == "__main__":
#     # print(recruiter_voice("Hello, I am reviewing your application.", name="ashish"))
#     # print(ats_voice("Scanning resume for Python, SQL, and Data Analysis.", name="ashish"))
#     print(career_coach_voice(
#         "You're doing great! Keep going—each interview builds momentum.", name="ashish"))
