from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from typing import List
from ..utils.exceptions import ModelError, RAGException
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class RAGModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.vector_store = InMemoryVectorStore(self.embeddings)
        self.llm = OllamaLLM(model=model_name)
        
        # Create RAG prompt template
        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, just say "I don't have enough information to answer this question."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:"""
        
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Initialize retrieval chain
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        
        logger.info(f"Initialized RAG model with {model_name}")

    def add_documents(self, documents: List[Document]) -> None:
        try:
            self.vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise ModelError(f"Failed to add documents: {str(e)}")

    def reset(self):
        """Reset the model's vector store and clear any stored state"""
        try:
            self.vector_store = InMemoryVectorStore(self.embeddings)
            logger.info("RAG model reset successfully")
        except Exception as e:
            logger.error(f"Error resetting RAG model: {str(e)}")
            raise ModelError(f"Failed to reset model: {str(e)}")

    def query(self, question: str) -> str:
        try:
            if not isinstance(question, str) or not question.strip():
                raise RAGException("Question must be a non-empty string")
            
            logger.info(f"Processing query: {question}")
            result = self.chain.invoke({"query": question})
            
            # Log retrieved documents for debugging
            if hasattr(result, 'source_documents'):
                logger.info(f"Retrieved {len(result.source_documents)} relevant documents")
            
            answer = result.get('result', '')
            if not answer:
                raise RAGException("No answer generated")
                
            logger.info("Successfully generated response")
            return answer
            
        except Exception as e:
            logger.error(f"Error in query processing: {str(e)}")
            raise RAGException(f"Failed to generate response: {str(e)}")
