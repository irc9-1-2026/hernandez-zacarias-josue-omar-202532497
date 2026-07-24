"""
Aplicativo web local - Consulta de Cócteles (TheCocktailDB)
Backend: FastAPI
Autor: Arturo Ivan Hernandez Hernandez

Ejecutar con:  uvicorn main:app --reload
Luego abrir:   http://127.0.0.1:8000
"""

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI(title="Consulta de Cócteles", version="1.0.0")

BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"

# Sirve los archivos estáticos (CSS/JS) desde la carpeta /static
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------------------------------------------------------------------
# Helper: normaliza un drink de la API a un formato limpio para el frontend
# ---------------------------------------------------------------------------
def formatear_drink(drink: dict) -> dict:
    ingredientes = []
    for i in range(1, 16):
        nombre = drink.get(f"strIngredient{i}")
        medida = drink.get(f"strMeasure{i}")
        if nombre and nombre.strip():
            texto = nombre.strip()
            if medida and medida.strip():
                texto = f"{medida.strip()} {texto}"
            ingredientes.append(texto)

    return {
        "id": drink.get("idDrink"),
        "nombre": drink.get("strDrink"),
        "categoria": drink.get("strCategory"),
        "tipo": drink.get("strAlcoholic"),
        "vaso": drink.get("strGlass"),
        "instrucciones": drink.get("strInstructionsES")
        or drink.get("strInstructions"),
        "imagen": drink.get("strDrinkThumb"),
        "ingredientes": ingredientes,
    }


# ---------------------------------------------------------------------------
# Endpoints de la API interna
# ---------------------------------------------------------------------------
@app.get("/api/buscar")
async def buscar(nombre: str = Query(..., description="Nombre del cóctel")):
    """Busca cócteles por nombre."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/search.php", params={"s": nombre})
        data = r.json()

    drinks = data.get("drinks")
    if not drinks:
        return JSONResponse({"resultados": [], "mensaje": "Sin resultados"})
    return {"resultados": [formatear_drink(d) for d in drinks]}


@app.get("/api/ingrediente")
async def por_ingrediente(nombre: str = Query(..., description="Ingrediente")):
    """Busca cócteles que contengan un ingrediente (lista básica)."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/filter.php", params={"i": nombre})
        data = r.json()

    drinks = data.get("drinks")
    if not drinks or drinks == "None Found":
        return JSONResponse({"resultados": [], "mensaje": "Sin resultados"})
    resultados = [
        {
            "id": d.get("idDrink"),
            "nombre": d.get("strDrink"),
            "imagen": d.get("strDrinkThumb"),
        }
        for d in drinks
    ]
    return {"resultados": resultados}


@app.get("/api/categoria")
async def por_categoria(nombre: str = Query(..., description="Categoría")):
    """Busca cócteles por categoría."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/filter.php", params={"c": nombre})
        data = r.json()

    drinks = data.get("drinks")
    if not drinks or drinks == "None Found":
        return JSONResponse({"resultados": [], "mensaje": "Sin resultados"})
    resultados = [
        {
            "id": d.get("idDrink"),
            "nombre": d.get("strDrink"),
            "imagen": d.get("strDrinkThumb"),
        }
        for d in drinks
    ]
    return {"resultados": resultados}


@app.get("/api/detalle/{id_drink}")
async def detalle(id_drink: str):
    """Devuelve el detalle completo de un cóctel por su ID."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/lookup.php", params={"i": id_drink})
        data = r.json()

    drinks = data.get("drinks")
    if not drinks:
        return JSONResponse({"error": "No encontrado"}, status_code=404)
    return formatear_drink(drinks[0])


@app.get("/api/aleatorio")
async def aleatorio():
    """Devuelve un cóctel aleatorio."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/random.php")
        data = r.json()
    return formatear_drink(data["drinks"][0])


@app.get("/api/categorias")
async def listar_categorias():
    """Lista las categorías disponibles (para el menú desplegable)."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(f"{BASE_URL}/list.php", params={"c": "list"})
        data = r.json()
    cats = [c["strCategory"] for c in data.get("drinks", [])]
    return {"categorias": cats}


# ---------------------------------------------------------------------------
# Página principal
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()
