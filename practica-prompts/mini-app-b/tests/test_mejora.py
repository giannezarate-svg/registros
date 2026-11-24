import pytest
from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def crear_gasto(descripcion: str, valor: int, categoria: str) -> dict:
    respuesta = cliente.post(
        "/api/gastos",
        json={
            "descripcion": descripcion,
            "valor": valor,
            "categoria": categoria,
        },
    )
    assert respuesta.status_code == 201
    return respuesta.json()


def test_eliminar_gasto_responde_204_sin_contenido() -> None:
    gasto = crear_gasto("Gasto para eliminar", 15000, "comida")

    respuesta = cliente.delete(f"/api/gastos/{gasto['id']}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""


def test_gasto_eliminado_desaparece_de_la_lista() -> None:
    gasto = crear_gasto("Pasaje para eliminar", 3000, "transporte")

    cliente.delete(f"/api/gastos/{gasto['id']}")

    ids = [elemento["id"] for elemento in cliente.get("/api/gastos").json()]
    assert gasto["id"] not in ids


def test_eliminar_gasto_actualiza_el_resumen() -> None:
    gasto = crear_gasto("Libro para eliminar", 12500, "estudio")
    resumen_antes = cliente.get("/api/gastos/resumen").json()

    respuesta = cliente.delete(f"/api/gastos/{gasto['id']}")

    assert respuesta.status_code == 204
    resumen_despues = cliente.get("/api/gastos/resumen").json()
    assert resumen_despues["total"] == pytest.approx(
        resumen_antes["total"] - gasto["valor"]
    )
    assert resumen_despues["por_categoria"]["estudio"] == pytest.approx(
        resumen_antes["por_categoria"]["estudio"] - gasto["valor"]
    )


def test_eliminar_gasto_inexistente_devuelve_404() -> None:
    respuesta = cliente.delete("/api/gastos/999999999")

    assert respuesta.status_code == 404
