# PyAssistant

PyAssistant is a beginner-friendly Python learning assistant that uses a Retrieval-Augmented Generation (RAG) workflow to answer Python questions with context from curated learning materials and official documentation.

It combines a Streamlit chat interface with a vector database, embeddings, and a Groq-powered language model to provide helpful explanations and Python code snippets for learners.

## Overview

This project is designed to help students and beginners:

- ask Python questions in plain English
- receive answers grounded in curated educational content
- review relevant examples from PDF and web resources
- generate Python code snippets for common programming tasks
- learn core concepts and interview-ready patterns in a guided format

## What the app does

PyAssistant loads a set of Python learning PDFs and documentation pages, splits them into chunks, stores them in a local Chroma vector database, and then retrieves the most relevant context for each user question.

The app then sends that retrieved context along with the prompt to a Groq LLM and returns an answer that is grounded in the project materials.

## Tech stack

- Python 3.13+
- Streamlit
- LangChain
- Chroma
- Hugging Face sentence-transformers embeddings
- Groq API for LLM inference
- PyPDF and web loaders for source material
- dotenv environment configuration

## Project structure

- `main.py` – Streamlit application entry point and chat UI
- `rag_model.py` – document loading, chunking, vector store setup, retrieval, and RAG chain creation
- `pdf_srcs/` – curated Python PDFs used as knowledge sources
- `db/chroma/` – persistent Chroma database created automatically on first run
- `assets/` – branding assets for the app interface
- `requirements.txt` – Python dependencies
- `pyproject.toml` – project metadata and dependency configuration

## Features

- conversational Python tutoring
- context-aware answers from curated learning resources
- code generation for common Python tasks
- persistent vector database for faster reuse of indexed documents
- beginner-focused learning flow for Python fundamentals and interview prep

## Prerequisites

Before running the project, make sure you have:

- Python 3.13 or newer
- a Groq API key
- access to the internet for loading documentation pages
- the PDF files in `pdf_srcs/`

## Setup

1. Clone the repository.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Or with uv:

   ```bash
   uv sync
   ```

4. Create a `.env` file in the project root with your Groq API key:

   ```env
   GROQ_API=your_groq_api_key_here
   ```

5. Confirm that the reference PDFs are present in `pdf_srcs/`.

## Running the app

Start the Streamlit app:

```bash
streamlit run main.py
```

Then open the local URL shown in the terminal in your browser.

## How it works

On startup, the app checks whether the Chroma database already exists.

- If the database is empty, it loads the configured PDFs and website content, splits them into chunks, and stores them in Chroma.
- If the database already contains data, it reuses the indexed content instead of rebuilding it.

When you ask a question, the app:

1. retrieves the most relevant document chunks
2. passes them to the retrieval pipeline
3. sends the context and your prompt to the Groq model
4. returns a context-aware answer along with Python code when needed

## Example questions

- "Explain list comprehensions in Python"
- "Write a Python function to check for palindromes"
- "What is the difference between a list and a tuple?"
- "Show an example of dictionary iteration in Python"

## Notes

- The project depends on the PDFs in `pdf_srcs/` and a valid `GROQ_API` value.
- The vector database is stored in `db/chroma` and is reused across runs.
- This project is intended for learning and experimentation, not for production deployment.

## License

This project is currently intended for educational use. Add a formal license if you plan to share or distribute it publicly.
