import json
import ollama
from typing import Generator
from app.services.vector_store import VectorStoreManager


class InvestigationPipeline:
    def __init__(self):
        self.default_model = "llama3:latest"
        self.vector_store = VectorStoreManager()

    def run_query_stream(
        self,
        query: str,
        history: list = [],
        use_web: bool = True,
        model_name: str = None,
        document_context: str = "",
        session_id: str = None,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        active_model = model_name or self.default_model

        if document_context and session_id:
            self.vector_store.add_documents(session_id, document_context)

        sub_queries = [query]
        if use_web:
            sub_queries = [
                query,
                f"effects of {query}",
                f"{query} mitigation strategies",
            ]

        yield json.dumps({"type": "planning", "data": sub_queries}) + "\n"

        sources = []
        if use_web:
            sources = [
                {
                    "title": f"Web Source {i+1} for {query}",
                    "url": f"https://example.com/search?q={query.replace(' ', '+')}",
                    "snippet": f"Comprehensive intelligence report and context regarding {query}.",
                }
                for i in range(2)
            ]

        yield json.dumps({"type": "sources", "data": sources}) + "\n"

        retrieved_chunks = []
        if session_id:
            retrieved_chunks = self.vector_store.query_documents(
                session_id, query, n_results=3
            )

        full_context = ""
        if retrieved_chunks:
            full_context += "\n\nRelevant Document Chunks (RAG):\n" + "\n".join(
                [f"- {chunk}" for chunk in retrieved_chunks]
            )
        elif document_context:
            full_context += f"\n\nDocument RAG Context:\n{document_context[:2000]}"

        if sources:
            full_context += "\n\nWeb Sources:\n" + "\n".join(
                [f"- {s['title']}: {s['snippet']}" for s in sources]
            )

        messages_payload = []
        for h in history:
            messages_payload.append({"role": h["role"], "content": h["content"]})

        prompt_content = f"Query: {query}\n{full_context}"
        messages_payload.append({"role": "user", "content": prompt_content})

        try:
            stream = ollama.chat(
                model=active_model,
                messages=messages_payload,
                stream=True,
                options={"temperature": temperature},
            )

            for chunk in stream:
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield json.dumps({"type": "token", "data": token}) + "\n"

        except Exception as e:
            yield json.dumps(
                {"type": "token", "data": f"\n\n[Pipeline Execution Error: {e}]"}
            ) + "\n"
            