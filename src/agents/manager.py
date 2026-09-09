from src.models.state import ResearchState, AgentRole
from src.agents.research import execute_research
from src.agents.graph import execute_graph_analysis
from src.utils.llm import generate_summary
import json

def orchestrate_workflow(state: ResearchState) -> ResearchState:
    """Orchestriert den gesamten Multi-Agenten-Workflow."""
    print("\n🚀 Manager-Agent: Starte Workflow...")
    
    # 1. Research Phase
    state.current_agent = AgentRole.RESEARCH
    state = execute_research(state)
    
    # 2. Graph Phase
    state.current_agent = AgentRole.GRAPH
    state = execute_graph_analysis(state)
    
    # 3. Synthese Phase
    print("  📝 Manager-Agent: Erstelle finale Zusammenfassung...")
    state.current_agent = AgentRole.MANAGER
    
    # Kontext für das LLM aufbereiten
    context = "WEB FINDINGS:\n"
    for f in state.web_findings:
        context += f"- {f.snippet} (Score: {f.relevance_score:.2f})\n"
        
    context += "\nGRAPH FINDINGS:\n"
    for g in state.graph_findings:
        context += f"- {g.name} ist {g.relationship} von {g.entity_type}\n"
        
    state.final_summary = generate_summary(context, state.query.target_market)
    
    print("✅ Manager-Agent: Workflow abgeschlossen.\n")
    return state
