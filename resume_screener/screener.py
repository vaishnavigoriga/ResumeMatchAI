import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ── Skill keyword bank ────────────────────────────────────────────────────────
SKILL_KEYWORDS = {
    # Languages
    "python", "java", "javascript", "c++", "c#", "typescript", "r", "scala", "go", "rust",
    # Web
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "spring",
    # Data / ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "matplotlib",
    "seaborn", "nlp", "machine learning", "deep learning", "data science", "transformers",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
    # DevOps / Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github", "linux", "ci/cd",
    # Other
    "rest api", "graphql", "agile", "scrum", "streamlit", "spark", "hadoop",
    "excel", "power bi", "tableau", "opencv",
}


def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, normalise whitespace."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation.replace(".", "").replace("+", "")))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(text: str) -> set[str]:
    """Return skills found in text that exist in the keyword bank."""
    processed = preprocess(text)
    found = set()
    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, processed):
            found.add(skill)
    return found


def tfidf_similarity(jd_text: str, resume_text: str) -> float:
    """Cosine similarity between JD and resume using TF-IDF vectors."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(score)


class ResumeScreener:
    """
    Scores each resume against a job description using:
      - Skill keyword overlap  (60% weight)
      - TF-IDF cosine similarity (40% weight)
    """

    SKILL_WEIGHT = 0.60
    TFIDF_WEIGHT = 0.40

    def screen(self, job_desc: str, candidate_name: str, resume_text: str) -> dict:
        jd_skills     = extract_skills(job_desc)
        resume_skills = extract_skills(resume_text)

        matched = jd_skills & resume_skills
        missing = jd_skills - resume_skills

        # Skill overlap ratio (0–1)
        skill_score = len(matched) / len(jd_skills) if jd_skills else 0.0

        # TF-IDF semantic similarity (0–1)
        tfidf_score = tfidf_similarity(job_desc, resume_text)

        # Weighted final score (0–100)
        final = (self.SKILL_WEIGHT * skill_score + self.TFIDF_WEIGHT * tfidf_score) * 100
        final = round(np.clip(final, 0, 100), 1)

        label = (
            "Strong match — highly recommended for interview."
            if final >= 70 else
            "Moderate match — consider with reservations."
            if final >= 45 else
            "Weak match — significant skill gaps detected."
        )

        return {
            "score":   final,
            "matched": sorted(matched),
            "missing": sorted(missing),
            "skill_score": round(skill_score * 100, 1),
            "tfidf_score": round(tfidf_score * 100, 1),
            "summary": (
                f"{candidate_name} matched {len(matched)} of {len(jd_skills)} required skills "
                f"({final}% overall score). {label}"
            ),
        }

    def screen_all(self, job_desc: str, resumes: dict[str, str]) -> dict[str, dict]:
        return {name: self.screen(job_desc, name, text) for name, text in resumes.items()}
