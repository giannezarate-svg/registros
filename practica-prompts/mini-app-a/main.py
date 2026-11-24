import sqlite3
from collections.abc import Iterator
from contextlib import asynccontextmanager, contextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "expenses.db"
CATEGORIES = (
    "Alimentación",
    "Transporte",
    "Hogar",
    "Ocio",
    "Salud",
    "Compras",
    "Otros",
)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
                category TEXT NOT NULL,
                spent_on TEXT NOT NULL
            )
            """
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="Gastos claros", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1, max_length=100)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category: Literal[
        "Alimentación", "Transporte", "Hogar", "Ocio", "Salud", "Compras", "Otros"
    ]
    spent_on: date


class Expense(ExpenseCreate):
    id: int


def expense_from_row(row: sqlite3.Row) -> Expense:
    return Expense(
        id=row["id"],
        description=row["description"],
        amount=Decimal(row["amount_cents"]) / 100,
        category=row["category"],
        spent_on=date.fromisoformat(row["spent_on"]),
    )


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/categories", response_model=list[str])
def list_categories() -> list[str]:
    return list(CATEGORIES)


@app.get("/api/expenses", response_model=list[Expense])
def list_expenses(
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    category: str | None = None,
) -> list[Expense]:
    query = "SELECT * FROM expenses"
    conditions: list[str] = []
    parameters: list[str] = []

    if month:
        conditions.append("substr(spent_on, 1, 7) = ?")
        parameters.append(month)
    if category:
        if category not in CATEGORIES:
            raise HTTPException(status_code=400, detail="Categoría no válida")
        conditions.append("category = ?")
        parameters.append(category)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY spent_on DESC, id DESC"

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [expense_from_row(row) for row in rows]


@app.post("/api/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate) -> Expense:
    description = expense.description.strip()
    if not description:
        raise HTTPException(status_code=422, detail="La descripción no puede estar vacía")
    amount_cents = int(expense.amount * 100)
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO expenses (description, amount_cents, category, spent_on)
            VALUES (?, ?, ?, ?)
            """,
            (
                description,
                amount_cents,
                expense.category,
                expense.spent_on.isoformat(),
            ),
        )
        row = connection.execute(
            "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return expense_from_row(row)


@app.delete("/api/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int) -> Response:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="No se encontró el gasto")
    return Response(status_code=204)
