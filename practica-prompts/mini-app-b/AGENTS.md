# AGENTS.md

## Proyecto
Aplicación web para registrar gastos ficticios y consultar su distribución.
Permite crear y eliminar gastos, consultar el listado y ver totales por categoría.

## Stack
Python 3.14, FastAPI, Pydantic, Jinja2, HTML/CSS/JavaScript nativo, pytest, httpx y Ruff. Los datos se guardan en memoria; no hay base de datos.

## Comandos
- Instalar: `pip install -r requirements.txt`
- Ejecutar: `uvicorn app.main:app --reload`
- Pruebas: `python -m pytest -v`
- Estilo: `ruff check .`

## Estructura
- `app/`: paquete de la aplicación.
- `app/__init__.py`: inicialización del paquete.
- `app/main.py`: modelos de entrada y salida, aplicación FastAPI y rutas.
- `app/servicios.py`: categorías, almacenamiento en memoria y lógica de gastos/resumen.
- `app/templates/`: plantillas HTML.
- `app/templates/index.html`: interfaz, estilos y JavaScript del registro de gastos.
- `tests/`: pruebas automatizadas de API y funcionalidades.
- `tests/test_aceptacion.py`: pruebas de aceptación del contrato principal.
- `tests/test_mejora.py`: pruebas de eliminación y actualización del resumen.
- `requirements.txt`: dependencias de la aplicación y herramientas.
- `pyproject.toml`: configuración de Ruff.
- `.gitignore`: archivos y directorios ignorados por Git.
- `prompt-b.md`: especificación inicial de la aplicación.
- `prompt-mejora.md`: especificación de la mejora de eliminación.
- `AGENTS.md`: contexto, comandos y reglas para contribuir al proyecto.

## Qué no hacer
- No modificar las pruebas para que pasen.
- No escribir claves en el código.
- No instalar dependencias sin explicar para qué.
- No usar base de datos ni archivos para persistir gastos.
- No hacer commit ni push.

## Lecciones aprendidas
