import streamlit as st

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

pdfs_directory = './pdfs/'

#embeddings will create the vectors out of the text
embeddings = OllamaEmbeddings(model="deepseek-r1:14b")
vectore_sstore = InMemoryVectorStore(embeddings)


def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())


def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    #we'll receive a list of documents containing seperate pages from the pdf file
    #and each page which is a document is a basically a 
    documents = loader.load()