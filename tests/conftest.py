"""
Global test fixtures
"""
from typing import Iterator

import chromadb
import pytest
from chromadb.api.local import LocalAPI
from fastapi.testclient import TestClient

from headjack.api.app import app
from headjack.config import get_chroma_client


@pytest.fixture
def chroma_client() -> LocalAPI:
    """
    Create an in-memory SQLite session to test models.
    """
    client = chromadb.Client()
    yield client


@pytest.fixture
def client(chroma_client: LocalAPI) -> Iterator[TestClient]:
    """
    Test rest client
    """

    def get_chroma_client_override() -> LocalAPI:
        return chroma_client

    app.dependency_overrides[get_chroma_client] = get_chroma_client_override

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
