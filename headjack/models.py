from typing import Dict, List, Optional

from pydantic import BaseModel


class BatchEmbeddings(BaseModel):
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict[str, str]]


class NodeDocument(BaseModel):
    name: str
    description: str
    metadata: Optional[Dict[str, str]]

    def generate_embeddings(self) -> BatchEmbeddings:

        # Add logic here to chunk up the content
        embeddings = BatchEmbeddings(
            ids=["foo"],
            documents=["placeholder sentence"],
            metadatas=[{"node_document": "foo"}],
        )
        return embeddings


class KnowledgeDocument(BaseModel):
    name: str
    description: str
    content: str
    url: str
    metadata: Optional[Dict[str, str]]

    def generate_embeddings(self) -> BatchEmbeddings:

        # Add logic here to chunk up the content
        embeddings = BatchEmbeddings(
            ids=["foo"],
            documents=["placeholder sentence"],
            metadatas=[{"knowledge_document": "foo"}],
        )
        return embeddings
