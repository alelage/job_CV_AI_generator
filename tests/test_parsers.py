from src.parsers.latex_parser import clean_latex
from src.parsers.html_parser import extract_job_sections


def test_clean_latex_basic():
    tex = r"""
    % Comment line
    \section{Experience}
    Some \textbf{bold} text and an \item itemize
    \begin{itemize}
    \item First
    \end{itemize}
    """
    cleaned = clean_latex(tex)
    assert "Experience" in cleaned
    assert "bold" in cleaned
    assert "- First" in cleaned


def test_extract_job_sections_selects():
    md = "\n".join([
        "# Title",
        "Some intro",
        "## Responsibilities",
        "- Do things",
        "- More things",
        "## Other",
        "Irrelevant",
    ])
    selected = extract_job_sections(md)
    assert "Responsibilities" in selected
    assert "Do things" in selected
