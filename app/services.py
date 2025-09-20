from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from flask import current_app

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def init_qa_chain():
    embeddings = OllamaEmbeddings(model=current_app.config['EMBEDDING_MODEL'])
    db = Chroma(
        persist_directory=current_app.config['CHROMA_PERSIST_DIRECTORY'],
        embedding_function=embeddings
    )
    retriever = db.as_retriever()
    llm = Ollama(model=current_app.config['LLM_MODEL'])
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

qa_chain = init_qa_chain()
