from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import servicios

app = FastAPI(title="Registro de gastos")


class GastoEntrada(BaseModel):
    descripcion: str
    monto: float = Field(gt=0)
    categoria: Literal["comida", "transporte", "estudio", "otros"]


@app.get("/")
def inicio():
    return {"mensaje": "Registro de gastos"}


@app.get("/api/gastos")
def listar_gastos():
    return servicios.listar_gastos()


@app.post("/api/gastos", status_code=201)
def crear_gasto(gasto: GastoEntrada):
    return servicios.registrar_gasto(gasto.model_dump())


@app.delete("/api/gastos/{gasto_id}", status_code=204)
def eliminar_gasto(gasto_id: int):
    if not servicios.eliminar_gasto(gasto_id):
        raise HTTPException(status_code=404, detail="No se encontró el gasto")
