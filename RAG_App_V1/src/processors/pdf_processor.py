from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from ..utils.exceptions import DocumentProcessingError
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class PDFProcessor:
    def __init__(self, pdfs_directory: str):
        self.pdfs_directory = pdfs_directory
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )

    def save_pdf(self, uploaded_file) -> str:
        try:
            file_path = f"{self.pdfs_directory}/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            logger.error(f"Error saving PDF: {str(e)}")
            raise DocumentProcessingError(f"Failed to save PDF: {str(e)}")

    def process_pdf(self, uploaded_file) -> List:
        try:
            file_path = self.save_pdf(uploaded_file)
            loader = PDFPlumberLoader(file_path)
            documents = loader.load()
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Successfully processed PDF: {uploaded_file.name}")
            return split_docs
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise DocumentProcessingError(f"Failed to process PDF: {str(e)}")
