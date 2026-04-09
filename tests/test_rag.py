import pytest
import sys
import os

# Add the parent directory to the path so we can import rag_agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag_agent import PetCareRAG

def test_rag_initialization():
    rag = PetCareRAG(["Dogs need walks.", "Cats need play."])
    assert len(rag.knowledge_base) == 2
    assert rag.tfidf_matrix is not None

def test_rag_retrieval():
    rag = PetCareRAG(["Dogs need 30 minutes of walking.", "Cats love laser pointers."])
    # TfidfVectorizer matches exact words, so 'Dogs' and 'walking' will match the text
    results = rag.retrieve("Dogs walking", top_k=1)
    assert len(results) == 1
    assert "Dogs need 30 minutes of walking." in results[0]

def test_rag_fallback_no_api_key(monkeypatch):
    # Ensure OPENAI_API_KEY is not set
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    rag = PetCareRAG(["Puppies need potty breaks."])
    assert rag.has_llm is False
    
    advice = rag.get_advice("puppy dog", "potty breaks")
    assert "Retrieved Advice (No LLM)" in advice
    assert "Puppies need potty breaks." in advice
