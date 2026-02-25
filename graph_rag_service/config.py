from dataclasses import dataclass, field
from typing import Optional
import os


@dataclass
class GraphDBSettings:
    uri: str = "bolt://localhost:7474"
    username: str = "graph_db"
    password: str = "password123"
    database: str = "graph_db"


@dataclass
class OllamaSettings:
    base_url: str = "http://localhost:11434"
    model: str = "llama3.1"
    embedding_model: str = "nomic-embed-text"
    temperature: float = 0.0


@dataclass
class RAGSettings:
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3
    vector_index_name: str = "chunk_embeddings"
    embedding_dimension: int = 768
    similarity_function: str = "cosine"


@dataclass
class RedisSettings:
    """Настройки Redis для семантического кэширования"""
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    decode_responses: bool = False  # False для работы с binary данными (embeddings)
    
    # Кэширование
    cache_ttl: int = 3600  # TTL для кэша (в секундах, 1 час)
    cache_enabled: bool = True
    
    # Семантическое кэширование
    semantic_cache_threshold: float = 0.95  # Порог схожести для cache hit (0-1)
    max_cache_size: int = 10000  # Максимальное количество записей в кэше



@dataclass
class Config:
    """Main configuration class for GraphDB RAG System."""
    graph_db: GraphDBSettings = field(default_factory=GraphDBSettings)
    ollama: OllamaSettings = field(default_factory=OllamaSettings)
    rag: RAGSettings = field(default_factory=RAGSettings)

    redis: RedisSettings = field(default_factory=RedisSettings)

    
    @classmethod
    def from_env(cls) -> "Config":
        """Загрузка конфигурации из переменных окружения"""
        return cls(
            graph_db=GraphDBSettings(
                uri=os.getenv("GRAPH_DB_URI", "bolt://localhost:7687"),
                username=os.getenv("GRAPH_DB_USERNAME", "graph_db"),
                password=os.getenv("GRAPH_DB_PASSWORD", "password123"),
                database=os.getenv("GRAPH_DB_DATABASE", "graph_db")
            ),
            ollama=OllamaSettings(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                model=os.getenv("OLLAMA_MODEL", "llama3.1"),
                embedding_model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
            ),
            redis=RedisSettings(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", "6379")),
                password=os.getenv("REDIS_PASSWORD"),
                db=int(os.getenv("REDIS_DB", "0")),
                cache_ttl=int(os.getenv("REDIS_CACHE_TTL", "3600")),
                cache_enabled=os.getenv("REDIS_CACHE_ENABLED", "true").lower() == "true",
                semantic_cache_threshold=float(os.getenv("REDIS_SEMANTIC_THRESHOLD", "0.95")),
                max_cache_size=int(os.getenv("REDIS_MAX_CACHE_SIZE", "10000"))
            )
        )
