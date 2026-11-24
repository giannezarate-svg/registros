from typing import TypedDict

CATEGORIAS = ("comida", "transporte", "estudio", "otros")


class Gasto(TypedDict):
    id: int
    descripcion: str
    valor: float
    categoria: str


_gastos: list[Gasto] = []
_siguiente_id = 1


def listar_gastos() -> list[Gasto]:
    return [gasto.copy() for gasto in _gastos]


def registrar_gasto(descripcion: str, valor: float, categoria: str) -> Gasto:
    global _siguiente_id
    gasto: Gasto = {
        "id": _siguiente_id,
        "descripcion": descripcion,
        "valor": valor,
        "categoria": categoria,
    }
    _gastos.append(gasto)
    _siguiente_id += 1
    return gasto.copy()


def eliminar_gasto(gasto_id: int) -> bool:
    for indice, gasto in enumerate(_gastos):
        if gasto["id"] == gasto_id:
            del _gastos[indice]
            return True
    return False


def obtener_resumen() -> dict[str, int | float | dict[str, int | float]]:
    por_categoria: dict[str, int | float] = {categoria: 0 for categoria in CATEGORIAS}
    for gasto in _gastos:
        por_categoria[gasto["categoria"]] += gasto["valor"]
    return {
        "total": sum(por_categoria.values()),
        "por_categoria": por_categoria,
    }
