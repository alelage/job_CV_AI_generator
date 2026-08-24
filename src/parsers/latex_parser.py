import re


def clean_latex(latex: str) -> str:
    text = latex.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = re.sub(r"\\(?:section|subsection|subsubsection|chapter|paragraph)\*?\s*\{([^{}]*)\}", r"\n\n\1\n", text, flags=re.I)
    text = re.sub(r"\\(?:begin|end)\s*\{[^{}]*\}", "\n", text)
    text = re.sub(r"\\(?:textbf|textit|emph|underline|textrm|textsf|texttt)\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\href\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:item)\s*", "\n- ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\s*\[[^]]*\])?\s*", "", text)
    text = re.sub(r"[{}]", "", text).replace("~", " ").replace("\\&", "&").replace("\\%", "%")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()
