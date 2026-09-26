def _local_pipeline(model_name):
    try:
        from transformers import pipeline
        return pipeline("text2text-generation", model=model_name)
    except Exception as exc:
        return None

def generate_interview_questions(role, skills, count=5, use_local_model=False, model_name="google/flan-t5-small"):
    skills_text = ", ".join(skills[:8]) or "software development"
    fallback = [
        f"Explain a project where you used {skills_text.split(',')[0]}. What was your contribution?",
        "Describe a difficult technical problem you solved and how you approached it.",
        "How do you test and debug your code before deployment?",
        "How would you design a scalable service for this role?",
        "Tell me about a time you received feedback and improved your work.",
        "How do you use AI tools responsibly during software development?",
        "How would you improve the performance of an AI application running locally?",
        "What trade-offs would you consider between cloud and on-device AI?"
    ]
    if not use_local_model:
        return fallback[:count]

    pipe = _local_pipeline(model_name)
    if pipe is None:
        return fallback[:count]

    prompt = (
        f"Create {count} concise technical interview questions for a {role} role. "
        f"Relevant skills: {skills_text}. Return only the questions."
    )
    try:
        output = pipe(prompt, max_new_tokens=256, do_sample=False)[0]["generated_text"]
        questions = [x.strip("- •0123456789. ") for x in output.split("\n") if x.strip()]
        return (questions or fallback)[:count]
    except Exception:
        return fallback[:count]

def generate_application_response(prompt, resume, job, use_local_model=False, model_name="google/flan-t5-small"):
    if use_local_model:
        pipe = _local_pipeline(model_name)
        if pipe:
            context = (
                f"Write a concise professional job application answer.\n"
                f"Question: {prompt}\n"
                f"Candidate resume: {resume[:2500]}\n"
                f"Job description: {job[:2500]}"
            )
            try:
                return pipe(context, max_new_tokens=180, do_sample=False)[0]["generated_text"].strip()
            except Exception:
                pass

    return (
        "I am interested in this role because it matches my software development and AI/ML "
        "skills and gives me an opportunity to solve practical problems, learn from experienced "
        "engineers, and build useful products. I am especially interested in applying my Python, "
        "Java, SQL, and AI skills while continuing to grow through challenging projects."
    )
