# ProbeAI: Enterprise AI Research & Web Intelligence Hub

ProbeAI is a fully containerized, enterprise-grade AI research and web intelligence application built to automate multi-modal research, context extraction, and grounded knowledge retrieval.

By combining an asynchronous **FastAPI backend**, interactive **Streamlit frontend**, local vector search using **ChromaDB**, and local LLM inference through **Ollama**, ProbeAI provides a robust and privacy-focused solution for complex organizational and technical investigations.

---

## 🏗️ Comprehensive Architecture & System Design

ProbeAI uses a microservices-inspired, multi-container architecture orchestrated through Docker Compose.

```text
┌─────────────────────────────────────────────────────────────┐
│                       Docker Network                        │
│                                                             │
│  ┌───────────────────────┐         ┌─────────────────────┐  │
│  │  Streamlit Frontend   │◄───────►│   FastAPI Backend   │  │
│  │  Container: 8501      │         │  Container: 8000   │  │
│  └───────────────────────┘         └──────────┬──────────┘  │
│                                               │             │
│                                    ┌──────────┴──────────┐  │
│                                    │ ChromaDB & SQLite   │  │
│                                    │ Persistent Volumes  │  │
│                                    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Layer — `probeai_frontend`

Built with **Streamlit and Python**.

Responsibilities include:

* Conversational research interface
* Sidebar configuration controls
* Real-time investigation status
* Agent thought/progress traces
* Source visualization
* Markdown export utilities
* Dynamic backend URL configuration through `BACKEND_URL`
* Cross-container communication with FastAPI

### Backend Intelligence Layer — `probeai_backend`

Built with **FastAPI and Pydantic**.

Responsibilities include:

* API request lifecycle management
* Research-agent orchestration
* Multi-step query planning
* Web search integration
* Streaming responses
* Prompt orchestration
* Session management
* RAG pipeline
* Communication with Ollama
* Persistent storage operations

### Storage & Knowledge Layer

#### ChromaDB

Used for:

* Vector embeddings
* Document indexing
* Semantic search
* Retrieval-Augmented Generation (RAG)
* Context retrieval from uploaded documents

#### SQLite / Local Storage

Used to persist:

* Chat session metadata
* Investigation history
* User messages
* Research results
* Session state

Persistent Docker volumes ensure that stored information survives container restarts.

### Inference Engine — Ollama

ProbeAI connects to locally running models through **Ollama**.

Supported model examples include:

* Llama 3
* Mistral
* Other Ollama-compatible models

Local inference provides:

* Data privacy
* Reduced external API dependency
* Offline-capable LLM inference
* Full control over the selected model

---

# 🚀 Detailed Feature Set

## 1. Automated Multi-Step Sub-Query Planning

ProbeAI can transform a complex research question into multiple focused sub-queries.

Example:

```text
User Question
      ↓
Query Analysis
      ↓
Sub-Query Generation
      ↓
Parallel / Sequential Search
      ↓
Information Collection
      ↓
Context Synthesis
      ↓
Final Answer
```

This improves research coverage by breaking complicated topics into smaller, targeted searches.

---

## 2. Grounded Web Intelligence

ProbeAI can combine LLM reasoning with live web search results.

The application presents:

* Search result titles
* Source URLs
* Descriptions/snippets
* Retrieved context
* Generated research response

The goal is to reduce unsupported AI-generated claims by grounding responses in retrieved information.

---

## 3. Document Ingestion & RAG

ProbeAI supports uploading contextual documents for retrieval-augmented generation.

Supported formats include:

* PDF
* TXT
* Python (`.py`)
* JavaScript (`.js`)
* Markdown (`.md`)

### Document Pipeline

```text
Upload Document
      ↓
File Parsing
      ↓
Text Extraction
      ↓
Text Processing
      ↓
Chunking
      ↓
Embedding Generation
      ↓
ChromaDB
      ↓
Semantic Retrieval
      ↓
LLM Context
      ↓
Grounded Response
```

PDF documents can be processed using `pypdf`.

---

## 4. Investigation Session Management

Users can manage previous research sessions.

Supported operations:

* Create sessions
* Save sessions
* Load previous sessions
* View investigation history
* Delete individual sessions
* Clear all sessions
* Restore previous conversations

This allows ProbeAI to function as a persistent research workspace rather than a single-use chatbot.

---

## 5. Dynamic Configuration Controls

The Streamlit sidebar provides runtime configuration options.

Users can:

* Enable/disable web grounding
* Select an available Ollama model
* Adjust LLM temperature
* Configure research behavior
* Control contextual document usage

Example:

```text
┌──────────────────────────────┐
│ ProbeAI Configuration        │
├──────────────────────────────┤
│ Web Grounding     [ON]       │
│                              │
│ Model             llama3     │
│                              │
│ Temperature       0.7        │
│ ████████████░░░              │
└──────────────────────────────┘
```

---

# 📁 Project Directory Structure

```text
ProbeAI/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── search.png
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

### Backend

The backend contains:

* FastAPI application
* API routes
* Agent logic
* RAG implementation
* Web research functionality
* Database operations
* Ollama integration

### Frontend

The frontend contains:

* Streamlit interface
* Chat UI
* Configuration sidebar
* Research status display
* Source display
* Session controls
* Export functionality

---

# 🐳 Docker Architecture

ProbeAI is designed to run through Docker Compose.

The primary services are:

```text
probeai_frontend
        │
        │ HTTP
        ▼
probeai_backend
        │
        ├──────────► ChromaDB
        │
        ├──────────► SQLite
        │
        └──────────► Ollama
```

Docker Compose manages:

* Container creation
* Networking
* Environment variables
* Service dependencies
* Persistent volumes
* Port mapping

---

# ⚙️ Quickstart & Installation

## Prerequisites

Make sure the following are installed:

* Docker Desktop
* Docker Compose
* Ollama

Verify Docker:

```bash
docker --version
docker compose version
```

Verify Ollama:

```bash
ollama --version
```

---

## 1. Clone or Open the Project

Open a terminal inside the project directory:

```bash
cd ProbeAI
```

---

## 2. Pull an Ollama Model

For example:

```bash
ollama pull llama3
```

Alternatively:

```bash
ollama pull mistral
```

Verify installed models:

```bash
ollama list
```

---

## 3. Start ProbeAI

From the project root:

```bash
docker compose up --build
```

To run the containers in detached mode:

```bash
docker compose up --build -d
```

---

## 4. Access the Application

### Streamlit Frontend

Open:

```text
http://localhost:8501
```

### FastAPI Backend

Open:

```text
http://localhost:8000
```

### Swagger API Documentation

Open:

```text
http://localhost:8000/docs
```

FastAPI automatically provides an interactive Swagger UI for testing the available API endpoints.

---

# 🔌 API Documentation

ProbeAI exposes RESTful APIs for research, model management, and session persistence.

| Endpoint                     | Method | Description                                                                                        |
| ---------------------------- | ------ | -------------------------------------------------------------------------------------------------- |
| `/api/investigate`           | POST   | Executes the research pipeline and streams planning steps, sources, and generated response chunks. |
| `/api/models`                | GET    | Retrieves available Ollama LLM models.                                                             |
| `/api/sessions`              | GET    | Retrieves stored investigation sessions.                                                           |
| `/api/sessions`              | POST   | Creates or updates a chat session and message payload.                                             |
| `/api/sessions/{session_id}` | GET    | Retrieves a specific investigation session and its message history.                                |
| `/api/sessions/{session_id}` | DELETE | Deletes a specific investigation session.                                                          |
| `/api/sessions`              | DELETE | Clears all stored investigation sessions.                                                          |

---

# 🔄 Investigation Request Flow

The primary `/api/investigate` endpoint follows this general workflow:

```text
User Research Question
          │
          ▼
    FastAPI Backend
          │
          ▼
   Query Understanding
          │
          ▼
  Sub-Query Generation
          │
          ▼
 ┌────────┴─────────┐
 │                  │
 ▼                  ▼
Web Search       ChromaDB
 │                  │
 └────────┬─────────┘
          ▼
   Context Aggregation
          │
          ▼
      Ollama LLM
          │
          ▼
   Response Generation
          │
          ▼
   Streaming Response
          │
          ▼
    Streamlit UI
```

---

# 📡 Streaming Response

The investigation endpoint supports streaming responses.

Instead of waiting for the entire research process to finish, the frontend can receive incremental updates such as:

```text
Planning research...
↓
Generating sub-queries...
↓
Searching web sources...
↓
Retrieving document context...
↓
Analyzing retrieved information...
↓
Generating final response...
```

Generated text can then be streamed progressively into the Streamlit interface.

---

# 🧠 Retrieval-Augmented Generation Architecture

When documents are uploaded, ProbeAI uses a RAG pipeline.

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
   ↓
Similarity Search
   ↓
Relevant Context
   ↓
Prompt Construction
   ↓
Ollama
   ↓
Grounded Answer
```

This allows the LLM to answer questions using information from the user's uploaded documents.

---

# 💾 Persistence

ProbeAI uses local persistent storage.

### SQLite

Stores application-level information such as:

```text
Sessions
Messages
Investigation History
Metadata
```

### ChromaDB

Stores:

```text
Document Chunks
Embeddings
Vector Metadata
```

Docker volumes should be configured to ensure these databases persist when containers are restarted.

---

# 🔐 Privacy & Security

ProbeAI is designed around local-first AI processing.

Instead of sending organizational documents directly to an external LLM API, the application can use locally hosted models through Ollama.

Key benefits include:

* Local LLM inference
* Reduced external API dependency
* Local document storage
* Local vector database
* Container isolation
* Persistent application state

> Note: Network searches and any external services enabled by the application may still transmit the relevant search query to those services.

---

# 🛠️ Technology Stack

| Layer                | Technology        |
| -------------------- | ----------------- |
| Frontend             | Streamlit         |
| Backend              | FastAPI           |
| API Validation       | Pydantic          |
| Programming Language | Python            |
| LLM Runtime          | Ollama            |
| LLM Examples         | Llama 3, Mistral  |
| Vector Database      | ChromaDB          |
| Database             | SQLite            |
| PDF Processing       | pypdf             |
| Containerization     | Docker            |
| Orchestration        | Docker Compose    |
| API Documentation    | Swagger / OpenAPI |
| Communication        | HTTP / Streaming  |

---

# 📈 Future Enhancements

Potential future improvements include:

* Authentication and role-based access control
* Multi-user workspaces
* Enterprise SSO
* Advanced document chunking
* Hybrid keyword + vector retrieval
* Reranking models
* Citation verification
* Research result caching
* Background task queues
* Observability and logging
* Prometheus/Grafana monitoring
* Redis-based task management
* Kubernetes deployment
* Automated evaluation of RAG responses
* Multi-agent research workflows

---

# 🧪 Development

To inspect running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

View backend logs:

```bash
docker compose logs backend
```

View frontend logs:

```bash
docker compose logs frontend
```

Stop the application:

```bash
docker compose down
```

Rebuild the containers:

```bash
docker compose up --build
```

Stop containers and remove associated volumes:

```bash
docker compose down -v
```

> Use `docker compose down -v` carefully because persistent database/vector-storage volumes may be deleted.

---

# 📋 Example Research Workflow

A typical user interaction looks like:

```text
1. User opens ProbeAI
        ↓
2. Enters a complex research question
        ↓
3. ProbeAI analyzes the question
        ↓
4. Generates multiple sub-queries
        ↓
5. Searches available web sources
        ↓
6. Retrieves relevant uploaded documents
        ↓
7. Performs semantic retrieval through ChromaDB
        ↓
8. Combines retrieved context
        ↓
9. Sends grounded prompt to Ollama
        ↓
10. Streams the generated response
        ↓
11. Displays sources and research findings
        ↓
12. Saves the investigation session
```

---

# 🎯 Project Objective

The primary objective of ProbeAI is to create a **private, extensible, and containerized enterprise research assistant** capable of combining:

* LLM reasoning
* Web intelligence
* Document understanding
* RAG
* Vector search
* Persistent sessions
* Streaming responses
* Local AI inference

The architecture is designed to provide a foundation that can be extended from a personal research assistant into a production-oriented enterprise intelligence platform.


