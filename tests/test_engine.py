from rag_worker.engine import CitationRAGWorker
from rag_worker.models import DocumentChunk, QueryRequest


def _sample_worker() -> CitationRAGWorker:
    return CitationRAGWorker([
        DocumentChunk(
            chunk_id="fin-q3-01",
            text="Q3 operating margin reached 24.5%.",
            source="q3.pdf",
            allowed_roles=["finance", "exec"],
            index_version="v1",
        ),
        DocumentChunk(
            chunk_id="fin-q3-02",
            text="Q3 operating margin draft for v2.",
            source="q3_v2.pdf",
            allowed_roles=["finance"],
            index_version="v2",
        ),
    ])


def test_acl_allows_authorized_role() -> None:
    worker = _sample_worker()
    res = worker.answer(QueryRequest(query="operating margin", role="finance", index_version="v1"))
    assert not res.refused
    assert res.citations == ["fin-q3-01"]
    assert "[fin-q3-01]" in res.answer


def test_acl_refuses_unauthorized_role() -> None:
    worker = _sample_worker()
    res = worker.answer(QueryRequest(query="operating margin", role="intern", index_version="v1"))
    assert res.refused
    assert res.citations == []
