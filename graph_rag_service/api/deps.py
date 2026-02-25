"""
FastAPI Dependencies
"""
from fastapi import Request, HTTPException
from typing import Dict

from ..services.graph_db.connector import GraphDBConnector
from ..services.ollama.ollama_loader import OllamaLoader
from ..services.graph_db.graph_builder import GraphBuilder
from ..services.graph_db.vector_store import VectorStore
from ..services.ollama.rag_pipeline import RAGPipeline
from ..services.cache.semantic_cache import SemanticCache


async def get_components(request: Request) -> Dict:
    """Dependency для получения всех компонентов"""
    if not hasattr(request.app.state, "components"):
        raise HTTPException(status_code=503, detail="System not initialized")
    
    return request.app.state.components


async def get_connector(request: Request) -> GraphDBConnector:
    """Dependency для получения GraphDB коннектора"""
    if not hasattr(request.app.state, "connector"):
        raise HTTPException(status_code=503, detail="GraphDB not initialized")
    
    return request.app.state.connector


async def get_ollama_loader(request: Request) -> OllamaLoader:
    """Dependency для получения Ollama загрузчика"""
    if not hasattr(request.app.state, "ollama_loader"):
        raise HTTPException(status_code=503, detail="Ollama not initialized")
    
    return request.app.state.ollama_loader


async def get_graph_builder(request: Request) -> GraphBuilder:
    """Dependency для получения Graph Builder"""
    if not hasattr(request.app.state, "graph_builder"):
        raise HTTPException(status_code=503, detail="Graph Builder not initialized")
    
    return request.app.state.graph_builder


async def get_vector_store(request: Request) -> VectorStore:
    """Dependency для получения Vector Store"""
    if not hasattr(request.app.state, "vector_store"):
        raise HTTPException(status_code=503, detail="Vector Store not initialized")
    
    return request.app.state.vector_store


async def get_rag_pipeline(request: Request) -> RAGPipeline:
    """Dependency для получения RAG Pipeline"""
    if not hasattr(request.app.state, "rag_pipeline"):
        raise HTTPException(status_code=503, detail="RAG Pipeline not initialized")
    
    return request.app.state.rag_pipeline


async def get_semantic_cache(request: Request) -> SemanticCache:
    """Dependency для получения Semantic Cache"""
    if not hasattr(request.app.state, "semantic_cache"):
        raise HTTPException(status_code=503, detail="Semantic Cache not initialized")
    
    return request.app.state.semantic_cache
