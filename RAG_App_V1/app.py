import streamlit as st
from src.config.config import load_config
from src.models.rag_model import RAGModel
from src.processors.pdf_processor import PDFProcessor
from src.utils.logger import setup_logger
from src.utils.exceptions import RAGException
import os

logger = setup_logger(__name__)

def reset_conversation():
    st.session_state.chat_history = []
    st.session_state.rag_model = RAGModel(st.session_state.config.model_name)
    logger.info("Chat conversation reset")

def initialize_app():
    st.set_page_config(
        page_title="RAG PDF Assistant",
        page_icon="📚",
        layout="wide"
    )
    config = load_config()
    
    if "rag_model" not in st.session_state:
        st.session_state.rag_model = RAGModel(config.model_name)
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    if "config" not in st.session_state:
        st.session_state.config = config
    
    os.makedirs(config.pdfs_directory, exist_ok=True)
    return config

def main():
    try:
        config = initialize_app()
        st.title("📚 RAG PDF Assistant")
        
        # Add reset button in sidebar
        with st.sidebar:
            st.title("Chat Controls")
            if st.button("Start New Chat", type="primary"):
                reset_conversation()
                st.rerun()
        
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                processor = PDFProcessor(config.pdfs_directory)
                documents = processor.process_pdf(uploaded_file)
                st.session_state.rag_model.add_documents(documents)
                st.success("PDF processed successfully!")
        
        # Display chat interface with message count
        if st.session_state.chat_history:
            st.info(f"Current conversation has {len(st.session_state.chat_history)} messages")
            
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        if question := st.chat_input("Ask a question about your documents"):
            st.chat_message("user").write(question)
            st.session_state.chat_history.append({"role": "user", "content": question})
            
            with st.spinner("Thinking..."):
                try:
                    # Ensure question is a string
                    question_str = str(question).strip()
                    if not question_str:
                        raise RAGException("Please enter a valid question")
                        
                    response = st.session_state.rag_model.query(question_str)
                    if response:
                        st.chat_message("assistant").write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    else:
                        raise RAGException("No response generated")
                except RAGException as e:
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Error processing question: {str(e)}")
                    
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()
