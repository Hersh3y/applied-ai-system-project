## AI Responsibility and Ethics

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
    
