# AI-Based Resume Screening & Candidate Match Predictor

An ML-powered recruitment assistant that analyzes resumes, predicts candidate-job compatibility, and ranks candidates based on skill match and semantic similarity.

## Features

- **NLP Skill Extraction** — identifies 60+ technical skills from raw resume text
- **TF-IDF Similarity** — measures semantic closeness between JD and resume
- **Weighted Scoring** — combines skill overlap (60%) + semantic similarity (40%)
- **Candidate Ranking** — ranks all candidates by overall match score
- **Skill Gap Analysis** — shows matched and missing skills per candidate
- **Interactive Dashboard** — built with Streamlit + Plotly

## Tech Stack

`Python` · `Scikit-learn` · `Pandas` · `NumPy` · `NLP` · `Streamlit` · `Plotly` · `Matplotlib`

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/gorigavaishnavi29/resume-screener.git
cd resume-screener

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

## How It Works

| Step | What happens |
|------|-------------|
| 1 | JD and resumes are preprocessed (lowercased, punctuation removed) |
| 2 | Skill keywords are extracted using regex matching against a 60+ skill bank |
| 3 | TF-IDF vectors are computed for semantic similarity |
| 4 | Final score = 60% skill overlap + 40% cosine similarity |
| 5 | Candidates are ranked; skill gaps and charts are displayed |

## Project Structure

```
resume-screener/
├── app.py           # Streamlit UI
├── screener.py      # NLP extraction + ML scoring logic
├── visualizer.py    # Plotly chart functions
├── requirements.txt
└── README.md
```
