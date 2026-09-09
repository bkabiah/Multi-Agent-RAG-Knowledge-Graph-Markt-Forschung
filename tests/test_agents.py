import pytest
from unittest.mock import patch, MagicMock
from src.models.state import ResearchState, MarketQuery, WebSearchResult, GraphEntity
from src.agents.research import execute_research
from src.agents.graph import execute_graph_analysis
import json

@pytest.fixture
def sample_state():
    return ResearchState(
        query=MarketQuery(
            target_market="Nachhaltige Mode",
            focus_companies=["Adidas"]
        )
    )

@patch('src.agents.research.search_market_trends')
@patch('src.agents.research.get_embedding')
def test_execute_research(mock_get_embedding, mock_search, sample_state):
    # Arrange
    mock_get_embedding.return_value = [0.1] * 384
    mock_search.return_value = json.dumps({
        "status": "success",
        "data": [{"score": 0.95, "payload": {"text": "Nachhaltigkeit ist im Trend"}}]
    })
    
    # Act
    result_state = execute_research(sample_state)
    
    # Assert
    assert len(result_state.web_findings) == 1
    assert result_state.web_findings[0].snippet == "Nachhaltigkeit ist im Trend"
    assert result_state.web_findings[0].relevance_score == 0.95

@patch('src.agents.graph.get_company_relationships')
def test_execute_graph_analysis(mock_get_relationships, sample_state):
    # Arrange
    mock_get_relationships.return_value = json.dumps({
        "status": "success",
        "data": [{"source": "Adidas", "relationship": "PARTNER_OF", "target": "Allbirds", "target_type": ["Company"]}]
    })
    
    # Act
    result_state = execute_graph_analysis(sample_state)
    
    # Assert
    assert len(result_state.graph_findings) == 1
    assert result_state.graph_findings[0].name == "Allbirds"
    assert result_state.graph_findings[0].relationship == "PARTNER_OF"
