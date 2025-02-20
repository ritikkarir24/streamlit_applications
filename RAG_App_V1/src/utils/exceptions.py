class RAGException(Exception):
    """Base exception class for RAG application"""
    pass

class DocumentProcessingError(RAGException):
    """Raised when there's an error processing documents"""
    pass

class ModelError(RAGException):
    """Raised when there's an error with the model operations"""
    pass
