from pathlib import Path
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader,WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter


# CONFIGURATION

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "pdf_srcs"
PERSIST_DIR = PROJECT_DIR / "db" / "chroma"
COLLECTION_NAME = "pyassistant"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gemma4:31b-cloud"


# PDF FILES

PDF_FILES = (
    "Python Cheatsheet.pdf",
    "Python Interview Codes Cheatsheet.pdf",
    "PYTHON SHORTHANDS.pdf",
    "python-to-mysql.pdf",
    "Tutorial_EDIT.pdf",
)


# WEBSITE URLS

WEBSITE_URLS = (
    "https://docs.python.org/3/tutorial/",
    "https://pynative.com/python/",
    "https://www.w3schools.com/python/python_intro.asp",
    "https://www.programiz.com/python-programming/examples",
    "https://www.geeksforgeeks.org/python/python-programming-examples/"
)

# LOAD PDF DOCUMENTS

def _load_pdf_documents():
    documents = []
    for filename in PDF_FILES:
        pdf_path = DATA_DIR / filename
        if not pdf_path.is_file():
            raise FileNotFoundError(f"PDF document not found: {pdf_path}")
        print(f"Loading PDF: {filename}")
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())
    return documents

# LOAD WEBSITE DOCUMENTS

def _load_website_documents():
    if not WEBSITE_URLS:
        return []
    print("Loading website pages...")
    loader = WebBaseLoader(list(WEBSITE_URLS))
    documents = loader.load()
    print(f"Loaded {len(documents)} website pages.")
    return documents

# LOAD ALL DOCUMENTS

def _load_documents():
    documents = []
    # Load PDFs
    documents.extend(_load_pdf_documents())
    # Load websites
    documents.extend(_load_website_documents())
    if not documents:
        raise ValueError( "No documents could be loaded.")
    print(f"Total documents loaded: {len(documents)}")
    return documents

# SPLIT DOCUMENTS INTO CHUNKS

def _load_chunks():
    documents = _load_documents()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No text could be extracted from the documents.")
    print(f"Created {len(chunks)} chunks.")
    return chunks

# CREATE RAG CHAIN

def create_rag_chain():
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    
    # Create / load Chroma database
    
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings,
    )

    # Add documents if database is empty
    
    existing_documents = vectorstore.get(limit=1)

    if not existing_documents["ids"]:
        print("Vector database is empty.")
        print("Creating document chunks...")
        chunks = _load_chunks()
        print("Adding documents to Chroma...")
        vectorstore.add_documents(chunks)
        print(f"Added {len(chunks)} chunks to Chroma.")
    else:
        print("Existing Chroma database found.")

    
    # Retriever

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4
        },
    )
    
    # Ollama LLM
    
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=0,
    )

    # RAG Prompt

    prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are a helpful Python assistant.

        For requests to write or modify code:
        - Generate a correct Python solution using your programming knowledge, even if the
        exact solution is not in the provided context.
        - Return the code in a Python code block, without an explanation.

        For questions about the contents of the provided documents:
        - Answer using only the context.
        - If the answer is not in the context, say:
        "I don't have enough information in the provided documents."

        Context:
        {context}
        """),
            ("human", "{input}")
        ])

    # Document chain

    document_chain = create_stuff_documents_chain(llm,prompt)

    # Retrieval chain

    rag_chain = create_retrieval_chain(retriever,document_chain)
    return rag_chain