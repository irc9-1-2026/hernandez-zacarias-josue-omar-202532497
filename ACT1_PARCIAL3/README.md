# Práctica 1 — API REST de Dispositivos de Red

## Cómo levantar el servidor (V1)
1. Instalar dependencias: `pip install flask requests`
2. Ejecutar: `python api_dispositivos.py`
3. El servidor queda escuchando en http://localhost:5000

## Cómo ejecutar el cliente (V2)
1. Con el servidor corriendo (paso anterior), abrir una segunda terminal
2. Ejecutar: `python cliente.py`
3. Verás las 4 operaciones CRUD (GET, POST, PUT, DELETE) probadas contra el servidor local