"""
Custom exceptions
"""

class GraphDBException(Exception):
    """Base GraphDB exception"""
    pass

class ServiceUnavailable(GraphDBException):
    """GraphDB service is unavailable"""
    pass


class AuthError(GraphDBException):
    """Authentication failed"""
    pass

class RAGException(Exception):
    """Base RAG exception"""
    pass

class RAGInitializationError(RAGException):
    """Initialization failed"""
    pass


class GraphDBConnectionError(RAGException):
    """GraphDB connection failed"""
    pass


class OllamaConnectionError(RAGException):
    """Ollama connection failed"""
    pass


class DocumentNotFoundError(RAGException):
    """Document not found"""
    pass


class QueryProcessingError(RAGException):
    """Query processing failed"""
    pass
