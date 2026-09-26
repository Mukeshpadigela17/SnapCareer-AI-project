# SnapCareer AI

**Private-first on-device AI career assistant for Snapdragon-powered HP PCs**

SnapCareer AI is a prototype built for the **Snapdragon AI Lab Build & Present Challenge**. It helps students and job seekers analyze resumes, understand job descriptions, identify skill gaps, prepare interview questions, and draft application responses.

## Why this project?

Career documents contain personal information. SnapCareer AI is designed around a local-first approach so sensitive resume and job-description content can be processed on the user's PC instead of being sent automatically to a cloud API.

The project has two operating modes:

1. **Lightweight mode** - runs with the included rule-based NLP analyzer and needs only Streamlit.
2. **Local AI mode** - optionally uses a local Hugging Face text-to-text model. This provides a foundation for replacing the model with a Qualcomm AI Hub optimized model for Snapdragon hardware.

## Features

- Resume skill extraction
- Job description skill extraction
- Resume-to-job skill matching
- Skill-gap identification
- Interview-question generation
- Application-response generation
- Local-first processing
- No API key required for the lightweight mode
- Designed for future Qualcomm AI Hub/NPU optimization

## Architecture

```text
                 +----------------------+
Resume / Job --->|    Streamlit UI      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Resume / Job Analyzer|
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Skill Matching       |
                 | + Gap Analysis       |
                 +----------+-----------+
                            |
                 +----------+-----------+
                 |                      |
                 v                      v
          Lightweight NLP       Optional Local AI
          (offline)             (Hugging Face)
                 |                      |
                 +----------+-----------+
                            |
                            v
                 Interview / Application
                       Assistance
```

## Snapdragon / Qualcomm AI Hub optimization path

The repository intentionally separates the UI, analysis logic, and generation layer so the local model can be replaced without changing the application interface.

For the challenge demonstration, the recommended deployment path is:

1. Select a compact open-source model supported by Qualcomm AI Hub.
2. Convert/optimize the model through Qualcomm AI Hub for the target Snapdragon platform.
3. Export the optimized artifact in the supported runtime format.
4. Add a Snapdragon runtime adapter inside `snapcareer/generator.py`.
5. Benchmark CPU/GPU/NPU execution.
6. Report latency, memory usage, model size, and offline behavior in the presentation.

**Important:** The current repository is a working prototype and does not falsely claim that a Qualcomm AI Hub model has already been benchmarked. Those measurements should be added after testing on the actual Snapdragon-powered HP PC.

## Installation

### Option A - lightweight mode

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -r requirements-lite.txt
```

Run:

```bash
streamlit run app.py
```

### Option B - local AI mode

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Enable **Use optional local AI model** in the sidebar.

The first use of the selected Hugging Face model may download model files. For a fully offline competition demo, download and cache the model before the presentation.

## Demo

Sample files are included:

- `data/sample_resume.txt`
- `data/sample_job.txt`

The Streamlit interface currently accepts TXT files. Upload the sample resume and job description to demonstrate the workflow.

## Suggested Snapdragon demo metrics

Measure these on the target HP Snapdragon PC:

- First inference time
- Subsequent inference time
- CPU utilization
- NPU/GPU utilization where supported
- RAM usage
- Model size
- Offline response time
- Cloud/API calls: 0 during local inference

Do not invent benchmark values. Record actual measurements from the target device and add them to the challenge presentation.

## Project structure

```text
SnapCareer-AI/
├── app.py
├── requirements.txt
├── requirements-lite.txt
├── README.md
├── data/
│   ├── sample_resume.txt
│   └── sample_job.txt
└── snapcareer/
    ├── __init__.py
    ├── analyzer.py
    └── generator.py
```

## Future improvements

- PDF/DOCX resume parsing
- Qualcomm AI Hub model integration
- Snapdragon NPU acceleration
- Local embeddings and semantic job matching
- Resume improvement suggestions
- Skill-learning recommendations
- Voice-based interview practice
- More detailed performance benchmarking

## License

MIT License. See `LICENSE`.

## Challenge note

This project is intended as a prototype for the Snapdragon AI Lab Build & Present Challenge. Before submission, test the complete application on the required Snapdragon-powered HP PC and document the actual Qualcomm AI Hub model/runtime and benchmark results used in the final build.
