## Rol
Actúa como desarrollador backend con experiencia en FastAPI, Jinja2 y pruebas con pytest.

## Objetivo
Agregar la funcionalidad de eliminar gastos en la aplicación Registro de gastos:
1. Implementar el endpoint DELETE /api/gastos/{id} que elimina el gasto correspondiente, actualiza el resumen para que deje de contar el gasto eliminado y responde con el código de estado 204 sin contenido. Si el id del gasto no existe, debe responder con el código 404.
2. Actualizar la página principal (app/templates/index.html) para que cada gasto en la lista tenga un botón de eliminar que llame al endpoint y actualice tanto la lista como el resumen por categoría sin recargar la página.
3. Crear el archivo tests/test_mejora.py con pruebas automáticas que verifiquen la eliminación exitosa (204), que el gasto desaparece de GET /api/gastos, que el total y la categoría en GET /api/gastos/resumen se descuentan correctamente, y que eliminar un id inexistente devuelve 404.

## Contexto
Lee AGENTS.md, app/main.py, app/servicios.py y app/templates/index.html.

## Restricciones
No modifiques tests/test_aceptacion.py.
Mantén la lógica de negocio en app/servicios.py (sin importar FastAPI allí) y las rutas en app/main.py.
Usa solo las dependencias de requirements.txt y JavaScript nativo en el frontend.

## Formato de salida
Antes de escribir o modificar código, muestra el plan con las rutas completas de los archivos que vas a crear o modificar y espera mi aprobación.

## Ejemplo
Si existe el gasto con id 1 por valor de 15000 en comida:
DELETE /api/gastos/1 responde con código 204 (cuerpo vacío).
Luego GET /api/gastos/resumen devuelve {"total": 0, "por_categoria": {"comida": 0, "transporte": 0, "estudio": 0, "otros": 0}}.
DELETE /api/gastos/9999 responde con código 404.

## Criterio de éxito
python -m pytest -v pasa todas las pruebas (tanto tests/test_aceptacion.py como tests/test_mejora.py) y ruff check . no reporta errores. Si después de 3 intentos no pasan, detente y explica el problema.