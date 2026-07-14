from pathlib import Path
import fitz
from docx import Document


def extract_text(file_path):
    """
    Extract text from a supported file.

    Supported file types:
    - PDF (.pdf)
    - Text (.txt)
    - Markdown (.md)
    - Microsoft Word (.docx)

    Returns:
        str: Extracted text, or an empty string if extraction fails.
    """

    path = Path(file_path)

    # Make sure the file actually exists
    if not path.exists():
        print(f"File not found: {path}")
        return ""

    # Make sure the given path is a file
    if not path.is_file():
        print(f"Not a file: {path}")
        return ""

    extension = path.suffix.lower()

    try:
        if extension == ".pdf":
            return extract_pdf(path)

        elif extension in {".txt", ".md"}:
            return extract_plain_text(path)

        elif extension == ".docx":
            return extract_docx(path)

        else:
            print(f"Unsupported file type: {extension}")
            return ""

    except Exception as error:
        print(f"Error extracting text from '{path.name}': {error}")
        return ""


def extract_pdf(path):
    """
    Extract text from every page of a PDF file.
    """

    text_parts = []

    with fitz.open(path) as document:

        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text()

            if page_text.strip():
                text_parts.append(page_text)

    return "\n".join(text_parts).strip()


def extract_plain_text(path):
    """
    Extract text from TXT and Markdown files.
    """

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def extract_docx(path):
    """
    Extract text from a Microsoft Word DOCX file.
    """

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs).strip()


# ---------------------------------------------------------
# TEST SECTION
# This runs only when extractor.py is executed directly.
# It does NOT run when extractor.py is imported by app.py.
# ---------------------------------------------------------

if __name__ == "__main__":

    base_dir = Path(__file__).resolve().parent.parent

    test_file = (
        base_dir
        / "test_files"
        / "DSAA ESEP PRACTICE Q. (1).pdf"
    )

    print("=" * 60)
    print("RecallOS Text Extractor Test")
    print("=" * 60)

    print(f"\nTesting file:\n{test_file}\n")

    extracted_text = extract_text(test_file)

    if extracted_text:

        print(f"Success!")
        print(f"Characters extracted: {len(extracted_text)}")

        print("\nFirst 1000 characters:")
        print("-" * 60)

        print(extracted_text[:1000])

        print("\n" + "-" * 60)

    else:
        print("No text could be extracted from the file.")