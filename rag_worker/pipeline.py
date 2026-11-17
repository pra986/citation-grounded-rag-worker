from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    allowed_roles: List[str]
    index_version: str

def build_acl_filter(user_role: str, index_version: str) -> Dict[str, Any]:
    return {"allowed_roles": {"$in": [user_role]}, "index_version": index_version}

def format_citation(chunk: Chunk) -> str:
    return f"[{chunk.doc_id}:{chunk.chunk_id}]"
