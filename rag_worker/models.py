from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    source: str
    allowed_roles: list[str] = Field(default_factory=list)
    index_version: str = "v1"


class QueryRequest(BaseModel):
    query: str
    role: str
    index_version: str = "v1"
    top_k: int = 5


class RetrievedChunk(BaseModel):
    chunk: DocumentChunk
    score: float


class GroundedAnswer(BaseModel):
    answer: str
    citations: list[str] = Field(default_factory=list)
    refused: bool = False
