from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path):
    """
    Load text from a PDF file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def load_text_file(file_path):
    """
    Load text from a normal text file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Text file not found: {file_path}"
        )

    return file_path.read_text(
        encoding="utf-8"
    )


def load_document(file_path):
    """
    Automatically load PDF or text document.
    """

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".txt":
        return load_text_file(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )