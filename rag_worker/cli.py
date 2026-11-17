import argparse
import json
from rag_worker.engine import CitationRAGWorker
from rag_worker.models import DocumentChunk, QueryRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Citation-Grounded RAG Worker CLI")
    parser.add_argument("--query", required=True, help="Query string")
    parser.add_argument("--role", default="finance", help="Caller role for ACL filtering")
    parser.add_argument("--version", default="v1", help="Index version")
    args = parser.parse_args()

    sample_chunks = [
        DocumentChunk(
            chunk_id="fin-q3-01",
            text="Q3 operating margin reached 24.5% driven by cloud revenue.",
            source="q3_report.pdf",
            allowed_roles=["finance", "exec"],
            index_version="v1",
        )
    ]
    worker = CitationRAGWorker(sample_chunks)
    result = worker.answer(QueryRequest(query=args.query, role=args.role, index_version=args.version))
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
