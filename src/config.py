from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """Zentrale Konfiguration für das E-Commerce Research System."""
    
    # Hugging Face
    hf_api_token: str = ""
    hf_model_name: str = "sentence-transformers/all-MiniLM-L6-v2" # Leichtgewichtig für Embeddings
    
    # Neo4j (Knowledge Graph)
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password123"
    
    # Qdrant (Vector DB)
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "ecommerce_market_data"

    # LLM Konfiguration (Wir nutzen später HF Inference API)
    llm_model_id: str = "mistralai/Mistral-7B-Instruct-v0.2"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Singleton-Instanz für den globalen Zugriff
settings = Settings()
