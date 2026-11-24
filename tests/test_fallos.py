import random

import pytest
from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


@pytest.mark.parametrize(
    ("monto", "categoria"),
    [
        (-500, "comida"),
        (0, "comida"),
        (15000, "categoria-invalida"),
    ],
)
def test_post_rechaza_montos_y_categorias_invalidos(monto, categoria):
    datos = {
        "descripcion": f"Prueba ficticia {random.randint(100000, 999999)}",
        "monto": monto,
        "categoria": categoria,
    }

    respuesta = cliente.post("/api/gastos", json=datos)

    assert respuesta.status_code == 422


@pytest.mark.parametrize(
    "gasto_id",
    [99999],
    ids=[f"gasto-inexistente-{random.randint(100000, 999999)}"],
)
def test_delete_gasto_inexistente_devuelve_404(gasto_id):
    respuesta = cliente.delete(f"/api/gastos/{gasto_id}")

    assert respuesta.status_code == 404
