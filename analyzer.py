import re

SKILL_VOCAB = [
    "python", "java", "c++", "javascript", "typescript", "sql", "html", "css",
    "react", "react.js", "node.js", "spring boot", "rest api", "django",
    "flask", "streamlit", "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "machine learning", "deep learning", "artificial intelligence",
    "ai", "llm", "generative ai", "prompt engineering", "nlp", "computer vision",
    "opencv", "yolo", "ocr", "git", "github", "docker", "aws", "azure", "gcp",
    "mysql", "postgresql", "mongodb", "dbms", "data analytics", "power bi",
    "tableau", "linux", "rest", "api", "agile", "spring", "kubernetes"
]

def _normalize(text):
    return re.sub(r"\s+", " ", text.lower())

def detect_skills(text):
    t = _normalize(text)
    found = []
    for skill in SKILL_VOCAB:
        if re.search(r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)", t):
            found.append(skill)
    # Remove duplicate variants such as react/react.js when both occur.
    return sorted(set(found), key=str.lower)

def analyze_resume(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    projects = [x for x in lines if any(k in x.lower() for k in ["project", "built", "developed", "application"])]
    experience = [x for x in lines if any(k in x.lower() for k in ["intern", "experience", "worked", "developer", "engineer"])]
    return {
        "skills": detect_skills(text),
        "projects": projects[:10],
        "experience_signals": experience[:10],
    }

def analyze_job(text):
    skills = detect_skills(text)
    keywords = []
    role_terms = [
        "software engineer", "software developer", "backend developer",
        "frontend developer", "full stack developer", "data analyst",
        "data scientist", "machine learning engineer", "ai engineer",
        "ai/ml engineer", "python developer", "java developer"
    ]
    t = _normalize(text)
    for term in role_terms:
        if term in t:
            keywords.append(term.title())
    return {"skills": skills, "keywords": keywords}

def match_skills(resume, job):
    resume_skills = set(detect_skills(resume))
    job_skills = set(detect_skills(job))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0
    return {"score": score, "matched": matched, "missing": missing}
