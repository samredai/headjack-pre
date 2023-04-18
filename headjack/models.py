from typing import Dict, List

from pydantic import BaseModel


class BatchEmbeddings(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict[str, str]]


class NodeDocument(BaseModel):
    name: str
    description: str

    def generate_embeddings(self) -> BatchEmbeddings:

        # Add logic here to chunk up the content
        embeddings = BatchEmbeddings(
            ids=[],
            documents=[],
            metadatas=[],
        )
        return embeddings


class KnowledgeDocument(BaseModel):
    name: str
    description: str
    content: str
    url: str
    metadata: Dict[str, str]

    def generate_embeddings(self) -> BatchEmbeddings:

        # Add logic here to chunk up the content
        embeddings = BatchEmbeddings(
            ids=[],
            documents=[],
            metadatas=[],
        )
        return embeddings
