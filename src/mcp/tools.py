from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from src.config import settings
import json

# Initialisierung der MCP Server Instanz
mcp = FastMCP("EcommerceResearchTools")

# --- Datenbank-Clients initialisieren ---
neo4j_driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
qdrant_client = QdrantClient(url=settings.qdrant_url)

def init_qdrant_collection():
    """Erstellt die Qdrant Collection, falls sie nicht existiert."""
    collections = [c.name for c in qdrant_client.get_collections().collections]
    if settings.qdrant_collection not in collections:
        qdrant_client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

# --- MCP TOOL 1: Knowledge Graph (Neo4j) ---
@mcp.tool()
def get_company_relationships(company_name: str) -> str:
    """
    Sucht im Knowledge Graph nach Unternehmensverknüpfungen (bidirektional: Zulieferer, Konkurrenten, Kunden).
    """
    query = """
    MATCH (c:Company {name: $name})-[r]-(connected)
    RETURN c.name AS source, type(r) AS relationship, connected.name AS target, labels(connected) AS target_type
    LIMIT 10
    """
    try:
        with neo4j_driver.session() as session:
            result = session.run(query, name=company_name)
            records = [record.data() for record in result]
            
            if not records:
                return json.dumps({"status": "info", "message": f"Keine Verknüpfungen für '{company_name}' gefunden."})
            return json.dumps({"status": "success", "data": records})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# --- MCP TOOL 2: RAG / Vektor Suche (Qdrant) ---
@mcp.tool()
def search_market_trends(query_embedding: list[float], limit: int = 5) -> str:
    """
    Sucht in der Vektordatenbank nach ähnlichen Marktreport-Snippets basierend auf dem Embedding.
    Nutzt die moderne query_points API.
    """
    try:
        search_result = qdrant_client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_embedding,
            limit=limit,
            with_payload=True
        )
        
        # query_points gibt ein Objekt zurück, die Punkte sind in .points
        findings = [{"score": hit.score, "payload": hit.payload} for hit in search_result.points]
        return json.dumps({"status": "success", "data": findings})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Initialisierung beim Import
init_qdrant_collection()
