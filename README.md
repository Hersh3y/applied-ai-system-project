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
