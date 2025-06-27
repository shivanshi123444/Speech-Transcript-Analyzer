from docx import Document
import PyPDF2
import io

def parse_text(file_content: bytes) -> str:
    """Parses a plain text file."""
    return file_content.decode('utf-8')

def parse_docx(file_content: bytes) -> str:
    """Parses a DOCX file."""
    doc = Document(io.BytesIO(file_content))
    return "\n".join([para.text for para in doc.paragraphs])

def parse_pdf(file_content: bytes) -> str:
    """Parses a PDF file."""
    reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def parse_transcript(file_path: str, file_content: bytes) -> str:
    """Dispatches parsing based on file extension."""
    if file_path.endswith('.txt'):
        return parse_text(file_content)
    elif file_path.endswith('.docx'):
        return parse_docx(file_content)
    elif file_path.endswith('.pdf'):
        return parse_pdf(file_content)
    else:
        raise ValueError("Unsupported file format.")