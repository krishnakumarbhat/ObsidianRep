
"""
Configuration settings for RecallMind application.
"""
import os

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY = "chroma_db"
EMBEDDING_MODEL = "nomic-embed-text:latest"
LLM_MODEL = "deepseek-r1:latest"

# Data Directory Configuration
DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")

# Application Configuration
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

# API Configuration
API_PREFIX = "/api"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Vector Search Configuration
VECTOR_SEARCH_LIMIT = 5
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
