import os
import chromadb
from chromadb.utils import embedding_functions
import ollama

class VectorStoreManager:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use Ollama for local embeddings if available, or fall back to default
        try:
            self.embedding_function = embedding_functions.OllamaEmbeddingFunction(
                url="http://localhost:11434/api/embeddings",
                model_name="nomic-embed-text:latest"
            )
        except Exception:
            # Fallback to Chroma's default sentence transformer model if needed
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()

    def add_documents(self, session_id: str, text: str, chunk_size: int = 500, overlap: int = 50):
        if not text.strip():
            return
            
        collection_name = f"session_{session_id.replace('-', '_')}"
        
        # Delete collection if it already exists to reset for the session
        try:
            self.client.delete_collection(name=collection_name)
        except Exception:
            pass

        collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

        # Simple sliding-window chunking
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if len(chunk.strip()) > 50: # Ignore tiny fragments
                chunks.append(chunk)

        if not chunks:
            return

        ids = [f"chunk_{idx}" for idx in range(len(chunks))]
        metadata = [{"source_index": idx} for idx in range(len(chunks))]

        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadata
        )

    def query_documents(self, session_id: str, query: str, n_results: int = 3) -> list:
        collection_name = f"session_{session_id.replace('-', '_')}"
        try:
            collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            if results and results.get("documents"):
                return results["documents"][0]
        except Exception:
            pass
        return []