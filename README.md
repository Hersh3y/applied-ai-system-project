# PawPal+ AI: Intelligent Pet Care Assistant with RAG

### Original Project Context
This project builds upon my earlier work, **PawPal+**. Originally, PawPal+ was an algorithmic pet care task scheduler designed to manage multi-pet households, detect schedule conflicts, and auto-generate daily care itineraries based on owner time constraints and task priorities.

---

### Title and Summary
**PawPal+ AI** is a smart pet care planning application that takes the guesswork out of raising animals. By combining constraint-based scheduling with an advanced **Retrieval-Augmented Generation (RAG)** AI engine, it generates optimized daily care plans and pairs them with highly personalized, context-aware veterinary and behavioral advice. It matters because it helps busy owners provide consistent, high-quality care without needing to manually research pet care best practices.

---

### Architecture Overview
Our system is structured into four main components that flow sequentially (as visualized in our system flowchart):
1. **UI / Input (Streamlit)**: Collects pet profiles (species, age, special needs) and tasks (e.g., walks, feeding).
2. **Core Logic (Scheduler)**: Processes tasks to generate an itinerary, applying priority sorting, operating hours logic, and identifying overlapping timeline conflicts.
3. **AI RAG System**: 
   - *Retriever*: Uses TF-IDF cosine similarity to pull the Top-K most relevant facts from a local pet care knowledge base, reacting dynamically to the pet's profile and scheduled tasks.
   - *Generator*: Feeds the schedule and retrieved facts to an OpenAI LLM to formulate a tailored, holistic advice paragraph.
4. **QA & Guardrails**: A fallback mechanism ensures that if the LLM is unreachable, raw retrieved facts are still safely displayed. Pytest automates logic verification throughout the pipeline.

---

### Setup Instructions
1. **Clone the repository**: `git clone <repo-url>` and navigate into the `applied-ai-system-project` directory.
2. **Set up virtual environment**: 
   ```bash
   python -m venv venv
   # Windows:
   .\\venv\\Scripts\\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**: Copy `.env.example` to `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
5. **Run the App**: 
   ```bash
   streamlit run app.py
   ```

---

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