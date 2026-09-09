from src.models.state import ResearchState, WebSearchResult
from src.mcp.tools import search_market_trends
from src.utils.llm import get_embedding
import json

def execute_research(state: ResearchState) -> ResearchState:
    """Führt die vektorbasierte Marktrecherche durch."""
    print(f"  🔍 Research-Agent: Suche nach Trends für '{state.query.target_market}'...")
    
    # 1. Anfrage in Vektor umwandeln
    query_embedding = get_embedding(state.query.target_market)
    
    # 2. MCP Tool aufrufen
    raw_result = search_market_trends(query_embedding, limit=3)
    parsed_result = json.loads(raw_result)
    
    # 3. Ergebnisse in den State schreiben
    if parsed_result["status"] == "success":
        for item in parsed_result["data"]:
            state.web_findings.append(WebSearchResult(
                title="Markt-Snippet",
                snippet=item["payload"].get("text", "Kein Text gefunden"),
                source_url="internal_qdrant_db",
                relevance_score=item["score"]
            ))
        print(f"  ✅ Research-Agent: {len(state.web_findings)} Treffer gefunden.")
    else:
        state.errors.append(f"Research-Fehler: {parsed_result.get('message')}")
        print(f"  ❌ Research-Agent: {parsed_result.get('message')}")
        
    return state
