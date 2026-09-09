from src.models.state import ResearchState, GraphEntity
from src.mcp.tools import get_company_relationships
import json

def execute_graph_analysis(state: ResearchState) -> ResearchState:
    """Analysiert Unternehmensverknüpfungen im Knowledge Graph."""
    print(f"  🕸️ Graph-Agent: Analysiere Verknüpfungen für {state.query.focus_companies}...")
    
    for company in state.query.focus_companies:
        raw_result = get_company_relationships(company)
        parsed_result = json.loads(raw_result)
        
        if parsed_result["status"] == "success":
            for rel in parsed_result["data"]:
                state.graph_findings.append(GraphEntity(
                    name=rel["target"],
                    entity_type=", ".join(rel["target_type"]),
                    relationship=rel["relationship"]
                ))
            print(f"  ✅ Graph-Agent: Verknüpfungen für '{company}' gefunden.")
        else:
            print(f"  ℹ️ Graph-Agent: {parsed_result.get('message')}")
            
    return state
