"""
Headjack web server
"""
import logging

from chromadb.api.local import LocalAPI
from chromadb.api.models.Collection import Collection
from chromadb.api.types import GetResult
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from headjack_server.config import get_chroma_client, get_headjack_collection
from headjack_server.models import Document, KnowledgeDocument

_logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/healthcheck/")
async def health_check(*, chroma_client: LocalAPI = Depends(get_chroma_client)):
    chroma_client.heartbeat()
    return {"status": "OK"}


@app.post("/nodes/")
async def add_node_embeddings(
    node: Document, *, headjack_collection: Collection = Depends(get_headjack_collection)
) -> JSONResponse:
    """
    Generate and store node embeddings
    """
    batch_embeddings = node.generate_embeddings()
    headjack_collection.add(**batch_embeddings.dict())
    return {"message": f"Node document {node.name} successfully saved"}


@app.get("/nodes/{node_name}/")
async def get_node_embeddings(node_name: str, *, headjack_collection: Collection = Depends(get_headjack_collection)) -> GetResult:
    """
    Get stored embeddings for a node
    """
    results = headjack_collection.get(where={"node_document": node_name})
    return results


@app.post("/knowledge/")
async def add_knowledge_embeddings(
    knowledge: KnowledgeDocument, *, headjack_collection: Collection = Depends(get_headjack_collection)
) -> JSONResponse:
    """
    Generate and store knowledge embeddings
    """
    batch_embeddings = knowledge.generate_embeddings()
    headjack_collection.add(**batch_embeddings.dict())
    return {"message": f"Knowledge document {knowledge.name} successfully saved"}


@app.get("/knowledge/{knowledge_name}/")
async def get_knowledge_embeddings(
    knowledge_name: str, *, headjack_collection: Collection = Depends(get_headjack_collection)
) -> GetResult:
    """
    Get stored embeddings for a knowledge document
    """
    results = headjack_collection.get(where={"knowledge_document": knowledge_name})
    return results
