# Gastos claros

Aplicación web sencilla para registrar y consultar gastos. Usa FastAPI para la
API y SQLite para guardar los datos localmente en `expenses.db`.

## Ejecutar

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Abre <http://127.0.0.1:8000>. La documentación interactiva de la API está en
<http://127.0.0.1:8000/docs>.

## API

- `GET /api/categories`: lista las categorías.
- `GET /api/expenses?month=AAAA-MM&category=...`: lista y filtra gastos.
- `POST /api/expenses`: registra un gasto con descripción, importe, categoría y fecha.
- `DELETE /api/expenses/{id}`: elimina un gasto.
