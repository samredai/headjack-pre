"""
Headjack web server
"""
import logging

from chromadb.api.local import LocalAPI
from fastapi import Depends, FastAPI

from headjack_server.config import get_chroma_client

_logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/healthcheck/")
async def health_check(*, chroma_client: LocalAPI = Depends(get_chroma_client)):
    chroma_client.heartbeat()
    return {"status": "OK"}
