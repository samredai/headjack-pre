"""
Module containing all config related things
"""
import chromadb
from chromadb.config import Settings


def get_chroma_client():  # pragma: no cover
    """
    Get a chromadb client
    """
    with chromadb.Client(
        Settings(
            chroma_api_impl="rest",
            chroma_server_host="chromadb",
            chroma_server_http_port="16402",
        ),
    ) as chroma_client:
        yield chroma_client
