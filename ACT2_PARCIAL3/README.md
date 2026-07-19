# Práctica 2 — Postman y Autenticación con REST APIs

## Descripción
Consumo de una API REST (ReqRes) con autenticación por API Key, realizando las 4 operaciones CRUD.
Primero exploradas visualmente en Postman (evidencia en `capturas/`) y luego automatizadas en Python.

## Requisitos
- Python 3
- Instalar dependencias: `pip install requests python-dotenv`

## Configuración
1. Crear un archivo `.env` (basado en `.env.example`) con tu propia API key:

API_KEY=tu_api_key_aqui
BASE_URL=https://reqres.in/api

2. El archivo `.env` NO se sube a Git (está en `.gitignore`).

## Ejecución

python usuarios_api.py

## Operaciones implementadas
| Operación | Método | Endpoint | Status esperado |
|-----------|--------|----------|-----------------|
| Listar    | GET    | /users   | 200 |
| Crear     | POST   | /users   | 201 |
| Actualizar| PUT    | /users/{id} | 200 |
| Eliminar  | DELETE | /users/{id} | 204 |

## Evidencia Postman
Las capturas de las 4 operaciones ejecutadas en Postman están en la carpeta `capturas/`.