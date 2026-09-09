
# 🛒 E-Commerce Market Researcher (Multi-Agent RAG + Knowledge Graph)
In der schnelllebigen E-Commerce-Branche benötigen Marktberater fundierte, datengetriebene Analysen, um Wettbewerbsvorteile zu identifizieren und strategische Entscheidungen zu treffen. Dieses Projekt implementiert einen KI-gestützten Assistenten, der komplexe Marktrecherchen vollständig automatisiert durchführt, indem er spezialisierte AI-Agenten orchestriert. Das System kombiniert semantische Vektorsuche (RAG) für unstrukturierte Markttrends mit expliziten Unternehmensverknüpfungen aus einem Neo4j Knowledge Graph, um ein umfassendes Marktverständnis zu generieren. Ein Manager-Agent synthetisiert diese multimodalen Erkenntnisse zu prägnanten, handlungsorientierten Berater-Briefings.

Das Projekt demonstriert moderne AI-Engineering-Praktiken für Enterprise-Umgebungen und zeigt nicht nur Prompting-Kenntnisse, sondern tiefes Verständnis für skalierbare Systemarchitekturen. Neben dem aufstrebenden Model Context Protocol (MCP) für standardisierte Tool-Integration setzt es auf strikte Typisierung via Pydantic für Data Validation, vollständige Containerisierung mit Docker und eine robuste Testabdeckung mit Pytest. Ziel ist es, wartbare, produktionsreife AI-Systeme zu bauen, die den Anforderungen Tech-Unternehmen gerecht werden.

 



## 🏗️ Architektur

```mermaid
graph TD
    User[Berater / User] -->|Markt-Anfrage| Manager[Manager-Agent]
    Manager -->|1. Orchestrierung| Research[Research-Agent]
    Manager -->|2. Orchestrierung| Graph[Graph-Agent]
    
    Research -->|Embedding & Query| MCP_RAG[MCP Tool: RAG Search]
    MCP_RAG -->|Vector Search| Qdrant[(Qdrant Vector DB)]
    
    Graph -->|Cypher Query| MCP_KG[MCP Tool: KG Search]
    MCP_KG -->|Graph Traversal| Neo4j[(Neo4j Knowledge Graph)]
    
    Research -->|Web Findings| Manager
    Graph -->|Graph Findings| Manager
    Manager -->|Prompt| LLM[Hugging Face LLM]
    LLM -->|Zusammenfassung| User
🚀 Tech Stack
Orchestrierung & State: Python, Pydantic (Strikte Typisierung & State-Management)
Multi-Agenten: Custom Agent-Pipeline (Manager, Research, Graph)
Datenbanken (Docker): Neo4j (Knowledge Graph), Qdrant (Vektor-Datenbank)
Integration: Model Context Protocol (MCP) für standardisierte Tool-Aufrufe
KI-Modelle: Hugging Face sentence-transformers (lokale Embeddings), Mistral-7B (LLM via Inference API)
Testing & DevOps: Pytest, Docker Compose, Git
⚙️ Installation & Setup
1. Voraussetzungen
Python 3.10+
Docker & Docker Compose
(Optional) Hugging Face API Token für LLM-Zusammenfassungen
2. Umgebung aufsetzen
# Repository klonen und betreten
git clone <dein-repo-link>
cd ecommerce-market-researcher

# Virtuelle Umgebung erstellen und aktivieren
python3 -m venv .venv
source .venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
