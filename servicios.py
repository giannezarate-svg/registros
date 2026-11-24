gastos = []


def listar_gastos():
    return gastos


def registrar_gasto(gasto):
    nuevo = {"id": len(gastos) + 1, **gasto}
    gastos.append(nuevo)
    return nuevo


def eliminar_gasto(gasto_id):
    for gasto in gastos:
        if gasto["id"] == gasto_id:
            gastos.remove(gasto)
            return True
    return False
