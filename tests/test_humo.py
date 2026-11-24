from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)


def test_pagina_principal_responde():
    assert cliente.get("/").status_code == 200
