# PyAssistant

PyAssistant is a beginner-friendly Python learning assistant built with Streamlit and Retrieval-Augmented Generation (RAG). It answers Python questions by searching through curated learning resources, official Python documentation, and programming examples, then responds with context-aware answers and code snippets.

## Overview

This project helps users:

- learn Python concepts from trusted sources
- ask questions in plain English
- get answers grounded in provided documents
- generate Python code examples for common tasks
- explore beginner and interview-focused Python topics

The app combines:

- a Streamlit chat interface
- Chroma vector database for semantic retrieval
- Hugging Face sentence embeddings
- Llama/Ollama-based language model for answer generation
- curated PDF and website content for Python learning

## Tech Stack

- Python 3.13+
- Streamlit
- LangChain
- Chroma
- Hugging Face Embeddings
- Ollama / local LLM
- PyPDFLoader and WebBaseLoader

## Project Structure

- `main.py` – Streamlit app UI and chat flow
- `rag_model.py` – document loading, chunking, embedding, vector retrieval, and LLM/RAG chain setup
- `pdf_srcs/` – PDF learning resources used as context
- `db/chroma/` – persisted Chroma vector database
- `assets/` – app branding assets

## Features

- conversational Python tutoring
- AI-generated code snippets
- retrieval from curated documents and official Python docs
- persistent vector store so the app can reuse indexed content
- beginner-focused Q&A for Python programming and interview prep

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   or, if using uv:

   ```bash
   uv sync
   ```

4. Make sure Ollama is installed and running.
5. Pull the model used by the app:

   ```bash
   ollama pull gemma4:31b-cloud
   ```

6. Start the app:

   ```bash
   streamlit run main.py
   ```

## Notes

- The project expects the Python learning PDFs located in the `pdf_srcs/` folder.
- The app indexes these documents the first time it runs and stores them in `db/chroma`.
- If the database is empty, it automatically creates the vector store based on the configured documents.
- The project is designed as a local educational AI assistant and may require a machine with enough RAM and a working local model runtime.

## Usage

Open the Streamlit UI in your browser and ask questions such as:

- "Explain Python list comprehensions"
- "Write a Fibonacci function in Python"
- "What is a dictionary in Python?"
- "Show example code for string slicing"

The assistant will retrieve relevant document chunks and generate a response grounded in those resources.

## License

This project is currently for educational and personal use. Update this section if you plan to distribute it under a specific license.
