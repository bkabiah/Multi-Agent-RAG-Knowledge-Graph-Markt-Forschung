from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
from src.config import settings
import json

# Lokales Embedding-Modell laden (wird beim ersten Mal heruntergeladen, ca. 90MB)
print("Lade Embedding-Modell...")
embedding_model = SentenceTransformer(settings.hf_model_name)

# LLM Client für Zusammenfassungen
llm_client = InferenceClient(
    model=settings.llm_model_id,
    token=settings.hf_api_token if settings.hf_api_token else None
)

def get_embedding(text: str) -> list[float]:
    """Erstellt einen Vektor für einen gegebenen Text."""
    return embedding_model.encode(text).tolist()

def generate_summary(context: str, query: str) -> str:
    """Nutzt das LLM, um eine professionelle Berater-Zusammenfassung zu erstellen."""
    prompt = f"""Du bist ein erfahrener Marktberater im E-Commerce. 
    Fasse die folgenden recherchierten Daten prägnant, professionell und handlungsorientiert zusammen.
    Gehe speziell auf die Anfrage ein: "{query}"
    
    RECHERCHE-DATEN:
    {context}
    
    FORMATIERE DIE ANTWORT MIT KLAREN ABSÄTZEN UND BULLET POINTS.
    """
    
    try:
        response = llm_client.text_generation(
            prompt,
            max_new_tokens=500,
            temperature=0.3,
            do_sample=True
        )
        return response
    except Exception as e:
        # Fallback, falls kein HF Token vorhanden ist oder das Modell überlastet ist
        return f"[FALLBACK: Kein LLM-Zugriff] Zusammenfassung der Daten für '{query}':\n\n{context}\n\n(Hinweis: Für eine KI-Zusammenfassung bitte einen HF_API_TOKEN in der .env hinterlegen.)"
