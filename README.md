# Citation-Grounded RAG Worker (Project 05)

Role-ACL filtered Chroma RAG knowledge worker with versioned indexes, query rewriting, reranking, and strict chunk citations.

## System Architecture

```
[User Query + Role Context]
        |
        v
[1. Pre-Retrieval Role ACL Filter] ---> (Enforce RBAC metadata filter before vector search)
        |
        v
[2. Query Rewriter & Multi-Query] ----> (Expand domain acronyms & sub-queries)
        |
        v
[3. Versioned Chroma Index] ----------> (Immutable collection + manifest alias)
        |
        v
[4. Cross-Encoder Reranker] ----------> (Score & select top-k grounded chunks)
        |
        v
[5. Strict Citation Grounder] --------> (Require [doc_id:chunk_id] per claim or abstain)
```

## 6-Stage Execution Workflow

1. **Role-ACL Pre-Filtering**: Build Chroma `where` metadata filters from the caller's role before any similarity search runs.
2. **Index Version Resolution**: Resolve the active immutable Chroma collection from the versioned index manifest.
3. **Query Rewriting**: Normalize terminology and generate focused retrieval queries.
4. **Vector Retrieval & Reranking**: Retrieve candidate chunks and rerank by relevance and ACL compliance.
5. **Grounded Synthesis**: Generate an answer where every factual claim is tied to `[doc_id:chunk_id]`.
6. **Citation Verification & Abstention**: Reject or abstain if any claim lacks a valid retrieved chunk ID.

## Production & Failure Controls

- **Pre-Retrieval RBAC**: Unauthorized documents never enter the LLM context window.
- **Versioned Index Rollback**: Atomic manifest pointer enables zero-downtime index updates and instant rollback.
- **Strict Citation Validation**: Blocks hallucinated citations by verifying every `[doc_id:chunk_id]` against retrieved chunks.
- **Abstention on Empty Evidence**: Returns explicit insufficient-evidence response instead of guessing.

## Local Setup & Pytest Verification

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Pinned Ed Donner Commit Attribution

- Derived from and hardened beyond the [ed-donner/llm_engineering](https://github.com/ed-donner/llm_engineering) **Week 5** (RAG knowledge worker with Chroma) notebooks.

## Architecture
- **Chroma Index Versioning**: Immutable versioned collections with manifest tracking and zero-downtime alias switching.
- **Pre-Retrieval Role ACL Filter**: Enforces document-level RBAC metadata filters before vector similarity search.
- **Query Rewrite & Reranking**: Multi-query expansion followed by cross-encoder reranking for high precision.
- **Chunk Citations**: Every generated claim is grounded to exact `[doc_id:chunk_id]` citations verified against retrieved context.

## Structure
- `rag_worker/` — Core RAG pipeline, ACL filter, index version manager, and citation grounder
- `tests/` — Unit tests for ACL enforcement, index versioning, and citation verification
- `pyproject.toml` — Project configuration and dependencies
