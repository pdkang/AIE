from typing import List
import PyPDF2
import io

class CharacterTextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_texts(self, documents: List[str]) -> List[str]:
        texts = []
        for doc in documents:
            if not doc.strip():
                continue
                
            # Split the text into chunks
            start = 0
            while start < len(doc):
                end = start + self.chunk_size
                chunk = doc[start:end]
                texts.append(chunk)
                start = end - self.chunk_overlap
                
        return texts

class TextFileLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_documents(self) -> List[str]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return [file.read()]

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_documents(self) -> List[str]:
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return [text] 