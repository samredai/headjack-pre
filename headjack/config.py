"""
Module containing all config related things
"""
import chromadb
from chromadb.config import Settings


def get_chroma_client():
    """
    Get a chromadb client
    """
    chroma_client = chromadb.Client(
        Settings(
            chroma_api_impl="rest",
            chroma_server_host="chromadb",
            chroma_server_http_port="16402",
        ),
    )
    return chroma_client
