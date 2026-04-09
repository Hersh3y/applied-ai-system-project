### Sample Interactions

**Interaction 1: Dog needing morning exercise**
*   **Input**: Pet: "Mochi" (Dog). Tasks: "Morning Walk" (30 min), "Evening Feeding" (15 min).
*   **AI Output**: *"Since Mochi has a morning walk scheduled, this is perfect for avoiding the midday heat, especially in summer. Following up with a regular evening feeding schedule will help prevent obesity and ensure Mochi stays healthy and active."*

**Interaction 2: Cat care routine**
*   **Input**: Pet: "Whiskers" (Cat, picky eater). Tasks: "Litter Box Change" (10 min), "Playtime" (15 min).
*   **AI Output**: *"It's great that you are cleaning Whiskers' litter box daily, as changes in habits can indicate medical issues. Since cats benefit from 20-30 minutes of interactive play, your scheduled playtime will provide excellent mental stimulation to keep her engaged."*

---

### Design Decisions
*   **TF-IDF for Retrieval**: I chose `scikit-learn`'s TF-IDF over a complex Vector Database (like Pinecone or Chroma) because our knowledge base is currently small and highly domain-specific. This keeps the application lightweight, reduces external dependencies, and runs entirely locally without costly infrastructure overhead.
*   **LLM Guardrails**: I implemented a strict fallback in the RAG agent. If an API key is missing or the external OpenAI API call fails, the system degrades gracefully and surfaces the raw retrieved text directly to the user. This ensures the app never outright crashes and remains partially functional offline.
*   **Decoupled Logic**: Hard constraints (time conflicts) and AI features are cleanly separated into different modules (`pawpal_system.py` vs `rag_agent.py`) so the AI can act as an observer without mutating the underlying safe schedule parameters.

---

### Testing Summary & AI Reliability
To prove the AI works reliably, the system incorporates **Automated Tests** and **Logging & Error Handling**:
*   **Automated Tests**: A `pytest` suite automatically verifies that the TF-IDF retriever logic properly matches query context with the exact expected facts.
*   **Logging & Guardrails**: The RAG module utilizes Python's `logging` to trace the similarity matching process and safely catch failed API queries, enforcing a fallback to raw text if the LLM is unreachable.

*   **Testing Results**: 31 out of 31 tests passed (28 core tests + 3 RAG tests). The AI retrieval accuracy was 100% on mapped facts. However, initial manual testing showed the generative AI struggled to formulate cohesive advice if the knowledge base completely lacked relevant context for an obscure animal. Implementing strict prompt constraints and a graceful fallback drastically improved the system's reliability.
*   **What I learned**: Automated testing is essential when integrating stochastic elements like AI. By testing the *retriever* deterministically using exact string matches, I ensured the contextual foundation provided to the LLM was always accurate.

---

### Reflection
This project taught me that "throwing AI at a problem" isn't enough—the AI needs properly structured context to be genuinely useful. Implementing RAG completely changed how the application felt. Instead of a generic, robotic response, giving the LLM specific, retrieved facts anchored its output in reality and virtually eliminated hallucinations. I also learned the true value of modular architecture; building the core programmatic logic first (Modules 1-3) made slotting the natural language AI module on top seamless and highly scalable.

### AI Responsibility and Ethics

**a. Limitations and biases**

- What are the limitations or biases in your system?
    **The RAG system's knowledge base is currently limited to dogs and cats, introducing a species bias. If an owner inputs an exotic pet (like a lizard or bird), the system may provide irrelevant advice or rely on the LLM's general algorithms. The scheduler also assumes all tasks are handled by a single owner, which shows bias against multi-caregiver households.**

**b. Misuse and prevention**

- Could your AI be misused, and how would you prevent that?
    **The AI could be misused if an owner relies entirely on it for critical medical advice instead of consulting a real veterinarian. To prevent this, the UI should include a strict disclaimer emphasizing that the AI provides general guidance only. Additionally, the prompt could be updated to automatically advise consulting a vet if the user inputs health-related task keywords.**

**c. Testing surprises**

- What surprised you while testing your AI's reliability?
    **I was surprised by how much the LLM struggled to generate useful advice when the retrieved context was sparse. Before adding strict prompting and fallback mechanisms, the AI would sometimes hallucinate confident but irrelevant facts. This proved that the generative AI is only as reliable as the specific data the retriever feeds it.**

**d. Collaboration and flawed suggestions**

- Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.
    **My collaboration involved using AI for conceptual brainstorming, troubleshooting `scikit-learn` integration, and setting up testing edge cases. 
    *Helpful suggestion*: The AI excellently generated the TF-IDF cosine similarity array logic for the RAG retriever, saving me significant time.
    *Flawed suggestion*: When writing the RAG fallback mechanism, the AI suggested passing a dummy API key to OpenAI and just catching the authentication error every run. This was inefficient and bad practice; I rejected it and instead implemented a proper environment variable check before initializing the client.**
    
