from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app import servicios

app = FastAPI(title="Registro de gastos")
templates = Jinja2Templates(directory="app/templates")


class GastoEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    descripcion: str = Field(min_length=1, max_length=80)
    valor: float = Field(gt=0, allow_inf_nan=False)
    categoria: Literal["comida", "transporte", "estudio", "otros"]

    @field_validator("descripcion")
    @classmethod
    def descripcion_no_vacia(cls, descripcion: str) -> str:
        if not descripcion:
            raise ValueError("La descripción no puede estar vacía")
        return descripcion


class GastoRespuesta(GastoEntrada):
    id: int


@app.get("/", include_in_schema=False)
def pagina_principal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "gastos": servicios.listar_gastos(),
            "resumen": servicios.obtener_resumen(),
            "categorias": servicios.CATEGORIAS,
        },
    )


@app.post("/api/gastos", response_model=GastoRespuesta, status_code=201)
def crear_gasto(entrada: GastoEntrada) -> dict:
    return servicios.registrar_gasto(
        descripcion=entrada.descripcion,
        valor=entrada.valor,
        categoria=entrada.categoria,
    )


@app.get("/api/gastos", response_model=list[GastoRespuesta])
def listar_gastos() -> list[dict]:
    return servicios.listar_gastos()


@app.get("/api/gastos/resumen")
def resumen_gastos() -> dict:
    return servicios.obtener_resumen()


@app.delete("/api/gastos/{gasto_id}", status_code=204)
def eliminar_gasto(gasto_id: int) -> Response:
    if not servicios.eliminar_gasto(gasto_id):
        raise HTTPException(status_code=404, detail="No se encontró el gasto")
    return Response(status_code=204)
