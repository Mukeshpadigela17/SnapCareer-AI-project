import streamlit as st
from snapcareer.analyzer import analyze_resume, analyze_job, match_skills
from snapcareer.generator import generate_interview_questions, generate_application_response

st.set_page_config(page_title="SnapCareer AI", page_icon="💼", layout="wide")

st.title("💼 SnapCareer AI")
st.caption("Private-first AI career assistant for Snapdragon-powered HP PCs")

st.info(
    "SnapCareer AI is designed for local/on-device processing. "
    "You can run it with an optional local Hugging Face model or use the lightweight "
    "privacy-first analyzer included in this repository."
)

with st.sidebar:
    st.header("Settings")
    use_local_model = st.checkbox("Use optional local AI model", value=False)
    model_name = st.text_input(
        "Local model",
        value="google/flan-t5-small",
        help="Download is required the first time. For Snapdragon optimization, replace this with a Qualcomm AI Hub converted/optimized model."
    )

resume_file = st.file_uploader("Upload your resume (TXT)", type=["txt"])
job_file = st.file_uploader("Upload a job description (TXT)", type=["txt"])

resume_text = resume_file.read().decode("utf-8", errors="ignore") if resume_file else ""
job_text = job_file.read().decode("utf-8", errors="ignore") if job_file else ""

if resume_text:
    st.subheader("Resume Analysis")
    analysis = analyze_resume(resume_text)
    c1, c2, c3 = st.columns(3)
    c1.metric("Skills Found", len(analysis["skills"]))
    c2.metric("Projects", len(analysis["projects"]))
    c3.metric("Experience Signals", len(analysis["experience_signals"]))
    st.write("**Detected skills:**", ", ".join(analysis["skills"]) or "None detected")

if job_text:
    st.subheader("Job Analysis")
    job_analysis = analyze_job(job_text)
    st.write("**Required skills:**", ", ".join(job_analysis["skills"]) or "None detected")
    st.write("**Role keywords:**", ", ".join(job_analysis["keywords"]) or "None detected")

if resume_text and job_text:
    st.subheader("🎯 Resume–Job Match")
    result = match_skills(resume_text, job_text)
    c1, c2, c3 = st.columns(3)
    c1.metric("Match Score", f'{result["score"]}%')
    c2.metric("Matched", len(result["matched"]))
    c3.metric("Missing", len(result["missing"]))

    st.write("**Matched skills:**", ", ".join(result["matched"]) or "None")
    st.write("**Skill gaps:**", ", ".join(result["missing"]) or "None")

    st.subheader("🎤 Interview Preparation")
    count = st.slider("Number of questions", 3, 10, 5)
    if st.button("Generate Interview Questions"):
        questions = generate_interview_questions(
            role=job_analysis["keywords"][0] if job_analysis["keywords"] else "Software Engineer",
            skills=job_analysis["skills"],
            count=count,
            use_local_model=use_local_model,
            model_name=model_name,
        )
        for i, q in enumerate(questions, 1):
            st.write(f"**{i}.** {q}")

    st.subheader("📝 Application Response")
    prompt = st.text_input(
        "Question",
        value="Why are you interested in this role?"
    )
    if st.button("Generate Response"):
        response = generate_application_response(
            prompt,
            resume_text,
            job_text,
            use_local_model=use_local_model,
            model_name=model_name,
        )
        st.write(response)

st.divider()
st.caption("Prototype for the Snapdragon AI Lab Build & Present Challenge.")
