from rag_worker.models import DocumentChunk, GroundedAnswer, QueryRequest, RetrievedChunk


class CitationRAGWorker:
    """Role-ACL filtered RAG engine with versioned indexing and strict chunk citations."""

    def __init__(self, chunks: list[DocumentChunk] | None = None) -> None:
        self._chunks: list[DocumentChunk] = list(chunks or [])

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        self._chunks.extend(chunks)

    def rewrite_query(self, query: str) -> list[str]:
        tokens = [t.strip("?.,!").lower() for t in query.split() if len(t.strip("?.,!")) > 2]
        return list(dict.fromkeys(tokens))

    def retrieve(self, request: QueryRequest) -> list[RetrievedChunk]:
        terms = self.rewrite_query(request.query)
        candidates: list[RetrievedChunk] = []
        for chunk in self._chunks:
            if chunk.index_version != request.index_version:
                continue
            if request.role not in chunk.allowed_roles:
                continue
            lower_text = chunk.text.lower()
            hits = sum(1 for term in terms if term in lower_text)
            if hits > 0:
                score = hits / max(len(terms), 1)
                candidates.append(RetrievedChunk(chunk=chunk, score=round(score, 4)))
        candidates.sort(key=lambda item: item.score, reverse=True)
        return candidates[: request.top_k]

    def answer(self, request: QueryRequest) -> GroundedAnswer:
        retrieved = self.retrieve(request)
        if not retrieved:
            return GroundedAnswer(
                answer="Insufficient authorized evidence to answer the query.",
                citations=[],
                refused=True,
            )
        citations = [item.chunk.chunk_id for item in retrieved]
        snippets = [f"{item.chunk.text} [{item.chunk.chunk_id}]" for item in retrieved]
        return GroundedAnswer(
            answer=" ".join(snippets),
            citations=citations,
            refused=False,
        )
