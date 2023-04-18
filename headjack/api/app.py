"""
Headjack web server
"""
import logging

from chromadb.api.local import LocalAPI
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from headjack.config import get_chroma_client
from headjack.models import KnowledgeDocument, NodeDocument

_logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/healthcheck/")
async def health_check(*, chroma_client: LocalAPI = Depends(get_chroma_client)):
    chroma_client.heartbeat()
    return {"status": "OK"}


@app.post("/nodes/")
async def add_node_embeddings(node: NodeDocument, *, chroma_client: LocalAPI = Depends(get_chroma_client)) -> JSONResponse:
    """
    Generate and store node embeddings
    """
    collection = chroma_client.get_or_create_collection("nodes")
    batch_embeddings = node.generate_embeddings()
    collection.add(**batch_embeddings.dict())
    return {"message": f"Node document {node.name} successfully saved"}


@app.get("/nodes/{node_name}/")
async def get_node_embeddings(node_name: str, *, chroma_client: LocalAPI = Depends(get_chroma_client)) -> JSONResponse:
    """
    Get stored embeddings for a node
    """
    collection = chroma_client.get_or_create_collection("nodes")
    results = collection.get(where={"node_document": node_name})
    return results


@app.post("/knowledge/")
async def add_knowledge_embeddings(
    knowledge: KnowledgeDocument, *, chroma_client: LocalAPI = Depends(get_chroma_client)
) -> JSONResponse:
    """
    Generate and store knowledge embeddings
    """
    collection = chroma_client.get_or_create_collection("knowledge")
    batch_embeddings = knowledge.generate_embeddings()
    collection.add(**batch_embeddings.dict())
    return {"message": f"Knowledge document {knowledge.name} successfully saved"}


@app.get("/knowledge/{knowledge_name}/")
async def get_knowledge_embeddings(knowledge_name: str, *, chroma_client: LocalAPI = Depends(get_chroma_client)) -> JSONResponse:
    """
    Get stored embeddings for a knowledge document
    """
    collection = chroma_client.get_or_create_collection("knowledge")
    results = collection.get(where={"knowledge_document": knowledge_name})
    return results
