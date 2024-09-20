from typing import List
from documine.utils.file_utils import get_file_extension
from documine.structures import Element
from documine.parser.html import HTMLParser
from documine.parser.pdf import PdfParser
from documine.parser.docx import DocxParser


def document_parser(file_path: str) -> List[Element]:
    extension = get_file_extension(file_path)
    if extension == '.html':
        parser = HTMLParser()
    elif extension == '.pdf':
        parser = PdfParser()
    elif extension == '.docx':
        parser = DocxParser()
    else:
        raise ValueError(f"Unsupported file type: {extension}")
    return parser.parse(file_path)
