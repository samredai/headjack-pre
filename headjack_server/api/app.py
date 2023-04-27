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
