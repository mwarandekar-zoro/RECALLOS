from pathlib import Path
import fitz
from docx import Document


def extract_text(file_path):
    """
    Extract text from supported file types.

    Supported:
    - PDF
    - TXT
    - Markdown
    - DOCX
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    try:
        if extension == ".pdf":
            return extract_pdf(path)

        elif extension in {".txt", ".md"}:
            return extract_plain_text(path)

        elif extension == ".docx":
            return extract_docx(path)

        return ""

    except Exception as error:
        print(f"Error extracting {path.name}: {error}")
        return ""


def extract_pdf(path):
    text = ""

    with fitz.open(path) as document:
        for page in document:
            page_text = page.get_text()
            text += page_text + "\n"

    return text.strip()


def extract_plain_text(path):
    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def extract_docx(path):
    document = Document(path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)