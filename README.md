# Job-CV Matcher & Tailor

Automated assistant to compare a LaTeX CV with a job description, highlight gaps, and generate tailored LaTeX CVs and cover letters.
---
**Inputs:** 

1. A CV (Plain text or Latex .tex)
2. A job description (Job URL, or paste description directly in text area)

**Outputs:**

1. A **list of skills** and requirements that Match and Do Not Match, between your CV and the Job description.
2. A version of **your CV, adapted** to this job.
3. A **Cover Letter** for the job application.

---
## Requires

Relies on AI. You will need to provide an **API key for any AI** service of your choice.

Advise: Edit `CV_guidelines.md` and `CL_guidelines.md` in the project root to guide generation. These files you can use to personalize your CV generator and the Cover Letter generator. 
They are passed to the AI as context, together with your CV and Job description.

## Quickstart

1. Copy `credentials.json.example` to `credentials.json` and fill keys, or use Streamlit Cloud secrets.
2. Install dependencies:

```bash
make setup
```

3. Run locally:

```bash
make run
```

