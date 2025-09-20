
# Recall

Recall is a Q&A application that uses a local large language model to answer questions about your markdown files. It uses LangChain, Ollama, and ChromaDB to create a retrieval-augmented generation (RAG) pipeline.

## Project Structure

```
.env
/recall
|-- app/
|   |-- __init__.py
|   |-- routes.py
|   |-- services.py
|   `-- templates/
|       `-- index.html
|-- scripts/
|   |-- ingest.py
|   `-- watcher.py
|-- chroma_db/
|-- data/
|-- config.py
|-- requirements.txt
`-- run.py
```

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Ollama:**

   - Install and run Ollama.
   - Pull the models you want to use, for example:

     ```bash
     ollama pull llama2:7b
     ollama pull nomic-embed-text:latest
     ```

3. **Add your documents:**

   - Place your markdown files in the `data` directory.

4. **Ingest your documents:**

   - Run the ingest script to process your documents and create a vector store:

     ```bash
     python scripts/ingest.py
     ```

5. **Run the application:**

   ```bash
   python run.py
   ```

   The application will be available at `http://127.0.0.1:5000`.

6. **(Optional) Watch for changes:**

   - To automatically re-ingest your documents when they change, run the watcher script:

     ```bash
     python scripts/watcher.py
     ```

## How It Works

1.  **Ingestion:** The `ingest.py` script reads your markdown files, splits them into chunks, generates embeddings using Ollama, and stores them in a ChromaDB vector store.
2.  **Watching:** The `watcher.py` script monitors the `data` directory for changes and automatically runs the `ingest.py` script when a file is added, modified, or deleted.
3.  **Application:** The `run.py` script starts a Flask web server that provides a Q&A interface. When you ask a question, the application uses the RAG pipeline to retrieve relevant documents from the vector store, combines them with your question, and uses Ollama to generate an answer.
