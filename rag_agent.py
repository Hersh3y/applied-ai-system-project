import os
import logging
from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Simple Pet Care Knowledge Base
PET_KNOWLEDGE = [
    "Dogs need at least 30 to 120 minutes of exercise a day depending on their breed and age.",
    "Cats are generally more independent but benefit from 20-30 minutes of interactive play per day.",
    "Puppies have smaller bladders and need outdoor breaks every 1-2 hours.",
    "Older dogs may suffer from arthritis, so short, gentle walks are better than long hikes.",
    "Cats should be fed a mix of wet and dry food to ensure they get enough moisture in their diet.",
    "A regular feeding schedule helps prevent obesity in pets. Twice a day is standard for adult dogs and cats.",
    "Grooming is essential. Long-haired cats and dogs need daily brushing to prevent mats.",
    "Mental stimulation is just as important as physical exercise. Use puzzle toys or training sessions.",
    "Changes in litter box habits can indicate medical issues in cats. Clean the box daily.",
    "Morning and evening walks are ideal for dogs to avoid the midday heat, especially in summer."
]

class PetCareRAG:
    """Retrieval-Augmented Generation module for providing pet care advice."""
    
    def __init__(self, knowledge_base: List[str] = None):
        if knowledge_base is None:
            knowledge_base = PET_KNOWLEDGE
        self.knowledge_base = knowledge_base
        
        # Initialize vectorizer
        try:
            self.vectorizer = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = self.vectorizer.fit_transform(self.knowledge_base)
            logger.info(f"Initialized RAG knowledge base with {len(self.knowledge_base)} entries.")
        except Exception as e:
            logger.error(f"Failed to initialize RAG vectorizer: {e}")
            self.tfidf_matrix = None
            
        # Initialize OpenAI client if key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.has_llm = True
            logger.info("OpenAI client initialized successfully.")
        else:
            self.client = None
            self.has_llm = False
            logger.warning("No OPENAI_API_KEY found. RAG will fallback to raw retrieved text.")

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        """Retrieve top k most relevant knowledge chunks for a query."""
        if self.tfidf_matrix is None:
            return []
            
        try:
            query_vec = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            # Only return results with non-zero similarity
            results = [self.knowledge_base[i] for i in top_indices if similarities[i] > 0.0]
            logger.info(f"Retrieved {len(results)} relevant facts for query.")
            return results
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []

    def get_advice(self, pet_summary: str, task_context: str) -> str:
        """Use RAG to provide personalized pet care advice based on the schedule."""
        query = f"{pet_summary} {task_context}"
        retrieved_facts = self.retrieve(query, top_k=3)
        context_str = "\\n- ".join(retrieved_facts) if retrieved_facts else "No specific facts found."
        
        if not self.has_llm:
            logger.info("Using fallback text generation (no LLM).")
            return f"**Retrieved Advice (No LLM):**\\n- {context_str}\\n\\n*(Set OPENAI_API_KEY in .env to enable AI generation)*"
            
        prompt = f"""You are an expert pet care AI assistant.
You are given the following pet and task context:
{query}

Here is some retrieved knowledge that might be helpful:
- {context_str}

Please provide 2-3 sentences of personalized advice for the pet owner. 
Make sure you integrate the retrieved knowledge meaningfully into your response.
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful pet care assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            advice = response.choices[0].message.content.strip()
            logger.info("Successfully generated AI advice.")
            return advice
        except Exception as e:
            logger.error(f"Error generating AI advice: {e}")
            return "Could not generate advice due to an API error."
