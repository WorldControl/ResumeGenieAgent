from typing import Dict, Any
import PyPDF2
from docx import Document


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages])

def extract_text_from_docx(file):
    doc = Document(file)
    return " ".join(paragraph.text for paragraph in doc.paragraphs)

def parse_resume(file) -> str:
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        return extract_text_from_docx(file.file)
    else:
        raise ValueError("仅支持 PDF 和 DOCX 文件")