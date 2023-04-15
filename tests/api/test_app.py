"""
Tests for app.py
"""

def test_healthcheck(client):
    client.get("/healthcheck/")