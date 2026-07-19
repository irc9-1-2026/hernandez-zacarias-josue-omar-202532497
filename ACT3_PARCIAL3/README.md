# Práctica 3 — Diagnóstico de Errores con Códigos de Estado HTTP

## Descripción
Script que realiza llamadas a una API, interpreta y clasifica los códigos de estado HTTP,
maneja excepciones (Timeout y ConnectionError) y genera una tabla de diagnóstico en JSON.

## Requisitos
- Python 3
- Dependencias: `pip install requests python-dotenv`

## Configuración
Crear un archivo `.env` (basado en `.env.example`) con tu API key de ReqRes:

API_KEY=tu_api_key_aqui

El archivo `.env` NO se sube a Git (está en `.gitignore`).

## Ejecución

python diagnostico_api.py

Esto imprime el diagnóstico en consola y genera el archivo `diagnostico.json`.

## Estructura del JSON de salida
El archivo `diagnostico.json` contiene:

| Campo | Significado |
|-------|-------------|
| `total_pruebas` | Número total de URLs probadas |
| `exitosas` | Cuántas devolvieron un código 2xx (éxito) |
| `fallidas` | Cuántas fallaron (error o excepción) |
| `resultados` | Lista con el detalle de cada prueba |

Cada objeto dentro de `resultados` tiene:

| Campo | Significado |
|-------|-------------|
| `url` | La dirección que se probó |
| `metodo` | El método HTTP usado (GET, POST, PUT, DELETE) |
| `status` | El código de estado HTTP recibido (200, 404, etc.) |
| `categoria` | La familia del código: 2xx, 3xx, 4xx, 5xx |
| `tipo` | Nombre del código (Éxito, Not Found, Unauthorized, etc.) |
| `accion` | Recomendación de qué hacer ante ese código |
| `exitoso` | `true` si fue 2xx, `false` en cualquier otro caso |
| `error` | (solo si hubo excepción) Tipo de fallo: Timeout o Sin conexión |

## Cómo agregar más URLs de prueba
En la sección `if __name__ == "__main__"` del script, agrega un diccionario a la lista `pruebas`:
```python
{"metodo": "GET", "url": "https://tu-url-aqui.com"}
```
Si necesitas enviar datos (POST/PUT), agrega la clave `body`:
```python
{"metodo": "POST", "url": "https://...", "body": {"name": "X", "job": "Y"}}
```

## Manejo de errores
El script captura dos excepciones por separado:
- **Timeout**: el servidor tardó más de 8 segundos en responder.
- **ConnectionError**: no se pudo conectar (URL inexistente o sin red).

En estos casos el registro incluye un campo `error` y `exitoso: false`, sin que el script se detenga.
