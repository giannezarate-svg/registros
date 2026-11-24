from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Registro de gastos")
gastos = []


class GastoEntrada(BaseModel):
    descripcion: str
    monto: float = Field(gt=0)
    categoria: Literal["comida", "transporte", "estudio", "otros"]


@app.get("/")
def inicio():
    return {"mensaje": "Registro de gastos"}


@app.get("/api/gastos")
def listar_gastos():
    return gastos


@app.post("/api/gastos", status_code=201)
def crear_gasto(gasto: GastoEntrada):
    nuevo = {"id": len(gastos) + 1, **gasto.model_dump()}
    gastos.append(nuevo)
    return nuevo


@app.delete("/api/gastos/{gasto_id}", status_code=204)
def eliminar_gasto(gasto_id: int):
    for g in gastos:
        if g["id"] == gasto_id:
            gastos.remove(g)
            return
    raise HTTPException(status_code=404, detail="No se encontró el gasto")
