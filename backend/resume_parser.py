import pdfplumber
import docx
import re
import spacy
import json
from pathlib import Path
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ---------------------------
# Load Transformer SpaCy Model
# ---------------------------
try:
    nlp = spacy.load("en_core_web_trf")  # transformer-based (more accurate)
except:
    nlp = spacy.load("en_core_web_sm")  # fallback

# ---------------------------
# File reading helpers
# ---------------------------


def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def read_resume(file_path):
    file_path = Path(file_path)
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() in [".docx", ".doc"]:
        return read_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

# ---------------------------
# NLP Extraction helpers
# ---------------------------


def extract_sections(text):
    """
    Split resume text by common headers.
    """
    # print(text)
    sections = defaultdict(str)
    current = "General"
    for line in text.split("\n"):
        clean_line = line.strip()
        if not clean_line:
            continue
        # Detect common sections
        if re.search(r"education", clean_line, re.I):
            current = "Education"
        elif re.search(r"experience|work history|employment", clean_line, re.I):
            current = "Experience"
        elif re.search(r"project|Project|Projects", clean_line, re.I):
            current = "Projects"
        elif re.search(r"skill|technical|Technical|tools|Course|Course work", clean_line, re.I):
            current = "Skills"
        elif re.search(r"Achievement|achievement|award|honor", clean_line, re.I):
            current = "Achievements"
        elif re.search(r"certifification|Certifications", clean_line, re.I):
            current = "Certifications"
        elif re.search(r"Codeforces|Leetcode|Atcoder|Codechef", clean_line, re.I):
            current = "Competitive"
        sections[current] += clean_line + " "
    return sections


def extract_skills(text):
    """
    Match against predefined skills dictionary.
    """
    skill_dict = {
        "Frontend": ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue", "Svelte", "Ruby on Rails"],
        "Backend": ["Node.js", "Django", "Flask", "Spring", "Express", "Java", "C#", "PHP", "Go", "Rust", "Gin", "Chi", "Actix"],
        "Databases": ["MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Oracle", "Cassandra", "HiveDb", "InfluxDB"],
        "Version Control": ["Git", "GitHub", "GitLab", "Bitbucket"],
        "Other": ["Docker", "Kubernetes", "AWS", "GCP", "Azure", "Linux", "CI/CD", "REST API", "GraphQL"],
        "Coursework": ["Data Structures", "Algorithms", "Operating Systems", "Databases", "Computer Networks", "Machine Learning", "Artificial Intelligence", "Web Development", "Mobile App Development", "Cloud Computing"]
    }

    found_skills = defaultdict(list)
    for cat, keywords in skill_dict.items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", text, re.I):
                found_skills[cat].append(kw)
    return dict(found_skills)


def summarize_text(text, n_sentences=3):
    """
    Summarize text using TF-IDF + KMeans to pick representative sentences.
    """
    if not text.strip():
        return []

    doc = nlp(text)
    sentences = [sent.text.strip()
                 for sent in doc.sents if len(sent.text.strip()) > 20]

    if len(sentences) <= n_sentences:
        return sentences

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(sentences)

    kmeans = KMeans(n_clusters=n_sentences, random_state=42, n_init=10)
    kmeans.fit(X)

    clustered = defaultdict(list)
    for i, label in enumerate(kmeans.labels_):
        clustered[label].append(sentences[i])

    summary = [cluster[0] for cluster in clustered.values()]
    return summary

# ---------------------------
# Main Parser
# ---------------------------


def parse_resume(file_path):
    text = read_resume(file_path)
    sections = extract_sections(text)

    parsed = {
        "Education": sections.get("Education", "").strip(),
        "Experience": {
            "raw": sections.get("Experience", "").strip(),
            "summary": summarize_text(sections.get("Experience", ""))
        },
        "Projects": {
            "raw": sections.get("Projects", "").strip(),
            "summary": summarize_text(sections.get("Projects", ""))
        },
        "Skills": extract_skills(sections.get("Skills", "")),
        "Certifications": sections.get("Certifications", "").strip(),
        "Competitive Programming / Contests": sections.get("Competitive", "").strip()
    }

    return parsed


# ---------------------------
# Run as script
# ---------------------------
if __name__ == "__main__":

    file_path = r"xxx"
    result = parse_resume(file_path)
    print(json.dumps(result, indent=4))
