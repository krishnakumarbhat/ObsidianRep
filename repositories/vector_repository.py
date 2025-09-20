"""
Vector database repository implementation using ChromaDB.
Following the Single Responsibility Principle and Dependency Inversion Principle.
"""
import os
from typing import List, Dict, Any
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from repositories.interfaces import IVectorRepository
import config


class ChromaVectorRepository(IVectorRepository):
    """ChromaDB implementation of vector repository."""
    
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
        self.db = Chroma(
            persist_directory=config.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )
    
    async def search_similar(self, query: str, limit: int = 5) -> List[dict]:
        """Search for similar content using vector similarity."""
        try:
            retriever = self.db.as_retriever(search_kwargs={"k": limit})
            docs = retriever.get_relevant_documents(query)
            
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": getattr(doc, 'score', 0.0)
                })
            return results
        except Exception as e:
            print(f"Error searching vector database: {e}")
            return []
    
    async def add_documents(self, documents: List[dict]) -> bool:
        """Add documents to the vector database."""
        try:
            from langchain.schema import Document
            
            # Convert dict documents to LangChain Document objects
            langchain_docs = []
            for doc in documents:
                langchain_docs.append(Document(
                    page_content=doc.get("content", ""),
                    metadata=doc.get("metadata", {})
                ))
            
            # Add to ChromaDB
            self.db.add_documents(langchain_docs)
            self.db.persist()
            return True
        except Exception as e:
            print(f"Error adding documents to vector database: {e}")
            return False
    
    async def is_empty(self) -> bool:
        """Check if the vector database is empty."""
        try:
            # Try to get a small sample to check if database has content
            retriever = self.db.as_retriever(search_kwargs={"k": 1})
            docs = retriever.get_relevant_documents("test query")
            return len(docs) == 0
        except Exception:
            return True
    
    async def clear(self) -> bool:
        """Clear all data from the vector database."""
        try:
            # ChromaDB doesn't have a direct clear method, so we recreate the collection
            import shutil
            if os.path.exists(config.CHROMA_PERSIST_DIRECTORY):
                shutil.rmtree(config.CHROMA_PERSIST_DIRECTORY)
            self.db = Chroma(
                persist_directory=config.CHROMA_PERSIST_DIRECTORY,
                embedding_function=self.embeddings
            )
            return True
        except Exception as e:
            print(f"Error clearing vector database: {e}")
            return False


class DocumentIngestionService:
    """Service for ingesting documents into the vector database."""
    
    def __init__(self, vector_repo: IVectorRepository):
        self.vector_repo = vector_repo
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
    
    async def ingest_from_directory(self, data_directory: str) -> bool:
        """Ingest all markdown files from a directory."""
        try:
            if not os.path.exists(data_directory):
                print(f"Data directory does not exist: {data_directory}")
                return False
            
            print("Loading documents...")
            loader = DirectoryLoader(data_directory, glob="**/*.md")
            documents = loader.load()
            print(f"Loaded {len(documents)} documents.")
            
            if not documents:
                print("No documents found to ingest.")
                return False
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            print(f"Split into {len(texts)} text chunks.")
            
            # Convert to dict format for vector repository
            documents_dict = []
            for doc in texts:
                documents_dict.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata
                })
            
            # Add to vector database
            success = await self.vector_repo.add_documents(documents_dict)
            if success:
                print("Documents successfully ingested into vector database.")
            else:
                print("Failed to ingest documents into vector database.")
            
            return success
            
        except Exception as e:
            print(f"Error during document ingestion: {e}")
            return False