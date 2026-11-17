# Citation-Grounded RAG Worker (K5)

Company knowledge worker with Retrieval-Augmented Generation featuring Chroma index versioning, pre-retrieval role ACL filtering, query rewriting & cross-encoder reranking, and inline chunk citations.

## Architecture
- **Chroma Index Versioning**: Immutable versioned collections with manifest tracking and zero-downtime alias switching.
- **Pre-Retrieval Role ACL Filter**: Enforces document-level RBAC metadata filters before vector similarity search.
- **Query Rewrite & Reranking**: Multi-query expansion followed by cross-encoder reranking for high precision.
- **Chunk Citations**: Every generated claim is grounded to exact `[doc_id:chunk_id]` citations verified against retrieved context.

## Structure
- `rag_worker/` — Core RAG pipeline, ACL filter, index version manager, and citation grounder
- `tests/` — Unit tests for ACL enforcement, index versioning, and citation verification
- `pyproject.toml` — Project configuration and dependencies
