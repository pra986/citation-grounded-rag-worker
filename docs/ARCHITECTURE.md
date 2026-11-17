# Architecture: Citation-Grounded RAG Worker

## Overview
The Citation-Grounded RAG Worker implements a role-ACL filtered retrieval and generation pipeline over versioned Chroma collections.

## Core Components
1. **Models (`rag_worker/models.py`)**: Pydantic data contracts for `DocumentChunk`, `QueryRequest`, `RetrievedChunk`, and `GroundedAnswer`.
2. **Engine (`rag_worker/engine.py`)**:
   - **Versioned Index**: Isolates embeddings by `index_version` tag.
   - **Role-ACL Pre-Filtering**: Enforces `allowed_roles` metadata filtering before scoring.
   - **Query Rewriting & Reranking**: Expands queries and reranks candidate chunks by lexical + semantic relevance.
   - **Strict Citation Grounding**: Every answer claim must reference `[chunk_id]` from retrieved context; returns an explicit refusal if no authorized chunks match.
3. **CLI (`rag_worker/cli.py`)**: Command-line interface for indexing and querying with role context.
