# 🍸 Consulta de Cócteles

Aplicativo web local que consulta la API gratuita **TheCocktailDB**.

**Stack:** Python (FastAPI) + HTML + CSS + JavaScript

## Estructura
```
cocktail-app/
├── main.py              # Backend FastAPI
├── requirements.txt     # Dependencias
└── static/
    ├── index.html       # Interfaz
    ├── style.css        # Estilos
    └── app.js           # Lógica del frontend
```

## Instalación y ejecución

1. Abrir una terminal en la carpeta del proyecto.

2. (Opcional pero recomendado) Crear un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac / Linux
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Levantar el servidor:
   ```bash
   uvicorn main:app --reload
   ```

5. Abrir en el navegador:
   ```
   http://127.0.0.1:8000
   ```

## Funcionalidades
- 🔍 Buscar cóctel por nombre
- 🧪 Buscar por ingrediente
- 📂 Filtrar por categoría (menú desplegable)
- 🎲 Cóctel aleatorio ("Sorpréndeme")
- 📋 Ver detalle: imagen, ingredientes con medidas, vaso, tipo y preparación

## Documentación automática de la API
FastAPI genera docs interactivas en:
```
http://127.0.0.1:8000/docs
```

## API usada
TheCocktailDB (gratuita, sin API key): https://www.thecocktaildb.com/api.php
