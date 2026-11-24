from fastapi import FastAPI

app = FastAPI(title="Registro de gastos")
gastos = []


@app.get("/")
def inicio():
    return {"mensaje": "Registro de gastos"}


@app.get("/api/gastos")
def listar_gastos():
    return gastos


@app.post("/api/gastos", status_code=201)
def crear_gasto(gasto: dict):
    nuevo = {"id": len(gastos) + 1, **gasto}
    gastos.append(nuevo)
    return nuevo


@app.delete("/api/gastos/{gasto_id}", status_code=204)
def eliminar_gasto(gasto_id: int):
    for g in gastos:
        if g["id"] == gasto_id:
            gastos.remove(g)
            return
