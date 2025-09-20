import os
import sys
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def ingest_documents():
    """
    Ingests markdown files into a ChromaDB vector store.
    """
    print("Loading documents...")
    loader = DirectoryLoader(config.DATA_DIRECTORY, glob="**/*.md")
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    if not documents:
        print("No documents found to ingest.")
        return

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} text chunks.")

    # Create embeddings and store in ChromaDB
    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
    print("Creating vector store...")
    db = Chroma.from_documents(
        texts,
        embeddings,
        persist_directory=config.CHROMA_PERSIST_DIRECTORY
    )
    db.persist()
    print("Vector store created and persisted.")

if __name__ == "__main__":
    if not os.path.exists(config.DATA_DIRECTORY):
        print(f"Creating data directory: {config.DATA_DIRECTORY}")
        os.makedirs(config.DATA_DIRECTORY)
        with open(os.path.join(config.DATA_DIRECTORY, "example.md"), "w") as f:
            f.write("# Welcome to your knowledge base\n\nThis is a sample markdown file. Add more files and subdirectories here to build your vector database.")
    
    ingest_documents()
