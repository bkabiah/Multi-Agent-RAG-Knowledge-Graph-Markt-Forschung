from src.mcp.tools import get_company_relationships, search_market_trends, qdrant_client, neo4j_driver
import json

print("--- Teste Neo4j Verbindung ---")
try:
    # Wir fügen testweise einen Node ein, damit wir etwas finden
    with neo4j_driver.session() as session:
        session.run("MERGE (c:Company {name: 'Zalando'}) MERGE (s:Company {name: 'Adidas'}) MERGE (s)-[:SUPPLIES_TO]->(c)")
    
    # Wir fragen Adidas ab, da wir wissen, dass es die ausgehende Beziehung hat
    result = get_company_relationships("Adidas")
    print("Neo4j Ergebnis:", json.loads(result))
except Exception as e:
    print("Neo4j Fehler:", e)

print("\n--- Teste Qdrant Verbindung ---")
try:
    # Füge einen Dummy-Vektor ein (384 Dimensionen, passend zu all-MiniLM-L6-v2)
    dummy_vector = [0.1] * 384
    
    # Moderne Upsert-Methode mit PointStruct
    from qdrant_client.models import PointStruct
    qdrant_client.upsert(
        collection_name="ecommerce_market_data",
        points=[PointStruct(id=1, vector=dummy_vector, payload={"text": "E-Commerce Wachstumstrend: Nachhaltige Sportbekleidung steigt um 15%"})]
    )
    
    result = search_market_trends(dummy_vector)
    print("Qdrant Ergebnis:", json.loads(result))
except Exception as e:
    print("Qdrant Fehler:", e)
