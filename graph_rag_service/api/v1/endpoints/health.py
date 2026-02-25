"""
Health check endpoints
"""
from fastapi import APIRouter, Depends, status
from typing import Dict

from graph_rag_service.domain.schemas.response import HealthResponse
from graph_rag_service.services.graph_db.connector import GraphDBConnector
from graph_rag_service.services.ollama.ollama_loader import OllamaLoader
from graph_rag_service.services.cache.semantic_cache import SemanticCache
from graph_rag_service.api.deps import (
    get_connector,
    get_ollama_loader,
    get_semantic_cache,
    get_components
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check(
    connector: GraphDBConnector = Depends(get_connector),
    ollama_loader: OllamaLoader = Depends(get_ollama_loader),
    semantic_cache: SemanticCache = Depends(get_semantic_cache)
) -> HealthResponse:
    """
    Проверка здоровья системы
    
    Проверяет:
    - Доступность GraphDB
    - Доступность Ollama
    - Доступность Redis
    - Статус инициализации компонентов
    """
    graph_db_healthy = False
    ollama_healthy = False
    redis_healthy = False
    
    # Проверка GraphDB
    try:
        connector.execute_query("RETURN 1")
        graph_db_healthy = True
    except Exception as e:
        graph_db_healthy = False
    
    # Проверка Ollama
    try:
        test_embedding = ollama_loader.embed_text("test")
        ollama_healthy = len(test_embedding) > 0
    except Exception as e:
        ollama_healthy = False
    
    # Проверка Redis
    try:
        semantic_cache.redis_client.ping()
        redis_healthy = True
    except Exception as e:
        redis_healthy = False
    
    overall_status = "healthy" if (graph_db_healthy and ollama_healthy and redis_healthy) else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        components={
            "graph_db": "healthy" if graph_db_healthy else "unhealthy",
            "ollama": "healthy" if ollama_healthy else "unhealthy",
            "redis": "healthy" if redis_healthy else "unhealthy"
        },
        version="1.0.0"
    )


@router.get("/ready")
async def readiness_check(
    components: Dict = Depends(get_components)
) -> Dict:
    """Проверка готовности к обработке запросов"""
    all_ready = all([
        components.get("connector"),
        components.get("ollama_loader"),
        components.get("rag_pipeline"),
        components.get("semantic_cache")
    ])
    
    return {
        "ready": all_ready,
        "message": "System is ready" if all_ready else "System is initializing"
    }


@router.get("/live")
async def liveness_check() -> Dict:
    """Проверка живучести приложения (для Kubernetes)"""
    return {"status": "alive"}
