# Job-CV Matcher & Tailor

Automated assistant to compare a LaTeX CV with a job description, highlight gaps, and generate tailored LaTeX CVs and cover letters.

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

Provide `CV_guidelines.md` and `CL_guidelines.md` in the project root to guide generation.
