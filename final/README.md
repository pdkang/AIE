title: FDA Regulatory Submission Accelerator

Description:
This AI application automates IND(Investigational New Drug) submission processes by providing a chat-based regulatory question assistant and a real-time submission package assessment tool, significantly reducing errors and accelerating FDA compliance.


Solution:

IND Assistant Module:

- Chat-based interface powered by RAG (Retrieval-Augmented Generation)
- Uses BGE embeddings and Qdrant vector database to retrieve relevant regulatory information
- Maintains conversation context through Streamlit session state
- Provides markdown-formatted responses with regulatory guidance

Submission Assessment Module:

- Accepts submission packages via ZIP upload or S3 URL
- Uses LangGraph with two specialized agents:
  - Cross-Reference Agent: Verifies documents against IND checklist requirements
  - Assessment Report Agent: Generates detailed analysis and recommendations
  - Supervised by a coordinator agent that calculates completeness scores
  - Provides visual progress indicators and downloadable assessment reports

The solution leverages LlamaParse for document extraction, OpenAI's GPT-4 for intelligent responses, and implements caching for performance optimization. The architecture follows a modular design with shared utilities and a unified Streamlit interface.



