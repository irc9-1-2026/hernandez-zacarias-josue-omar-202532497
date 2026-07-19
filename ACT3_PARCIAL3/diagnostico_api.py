import requests, json, os
from dotenv import load_dotenv

# Ruta absoluta al .env de este proyecto específico (funciona sin importar
# desde qué carpeta se ejecute el script)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path, override=True)

API_KEY = os.getenv("API_KEY")
print("Leyendo .env desde:", env_path)
print("API_KEY cargada:", API_KEY)
print()

# Headers con la API key para las peticiones a ReqRes
HEADERS_REQRES = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# httpstat.us a veces cierra la conexión si no detecta un User-Agent de
# navegador (el default de requests, "python-requests/x.x", lo rechaza)
HEADERS_HTTPSTAT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


# ── Clasificar un código de estado por categoría ──────────────
def clasificar_status(codigo):
    """Devuelve un dict con categoría, nombre y acción sugerida."""
    if 200 <= codigo <= 299:
        return {"categoria": "2xx", "tipo": "Éxito",
                "accion": "Procesar la respuesta normalmente"}
    elif 300 <= codigo <= 399:
        return {"categoria": "3xx", "tipo": "Redirección",
                "accion": "Seguir la redirección o actualizar la URL"}
    elif codigo == 400:
        return {"categoria": "4xx", "tipo": "Bad Request",
                "accion": "Revisar el formato del body o los parámetros enviados"}
    elif codigo == 401:
        return {"categoria": "4xx", "tipo": "Unauthorized",
                "accion": "Revisar las credenciales o el token de autenticación"}
    elif codigo == 403:
        return {"categoria": "4xx", "tipo": "Forbidden",
                "accion": "Verificar permisos del token o usuario"}
    elif codigo == 404:
        return {"categoria": "4xx", "tipo": "Not Found",
                "accion": "El recurso no existe, verificar la URL o el ID"}
    elif codigo == 429:
        return {"categoria": "4xx", "tipo": "Too Many Requests",
                "accion": "Esperar antes de reintentar (rate limit)"}
    elif 500 <= codigo <= 599:
        return {"categoria": "5xx", "tipo": "Error del servidor",
                "accion": "El problema está en el servidor, no en tu código. Reportar."}
    return {"categoria": "desconocido", "tipo": "?", "accion": "Consultar documentación"}


# ── Hacer petición y generar registro de diagnóstico ──────────
def diagnosticar_url(metodo, url, **kwargs):
    """Realiza la petición y devuelve un dict con todo el diagnóstico."""
    try:
        r = requests.request(metodo, url, timeout=8, **kwargs)
        info = clasificar_status(r.status_code)
        return {
            "url":        url,
            "metodo":     metodo.upper(),
            "status":     r.status_code,
            "categoria":  info["categoria"],
            "tipo":       info["tipo"],
            "accion":     info["accion"],
            "exitoso":    200 <= r.status_code <= 299,
        }
    except requests.exceptions.Timeout:
        return {"url": url, "metodo": metodo.upper(),
                "error": "Timeout", "accion": "El servidor tardó demasiado, reintentar más tarde", "exitoso": False}
    except requests.exceptions.ConnectionError as e:
        print(f"  -> ConnectionError detalle ({url}):", e)  # debug temporal
        return {"url": url, "metodo": metodo.upper(),
                "error": "Sin conexión", "accion": "Verificar red y URL", "exitoso": False}


# ── Generar la tabla de diagnóstico en JSON ───────────────────
def generar_tabla_diagnostico(pruebas, archivo_salida="diagnostico.json"):
    """
    pruebas: lista de dicts con claves "metodo", "url" y opcionalmente "body"
    Ejemplo: [{"metodo": "GET", "url": "https://..."}]
    """
    resultados = []
    for prueba in pruebas:
        kwargs = {}
        # Si la URL es de reqres, le mandamos los headers con la key
        if "reqres.in" in prueba["url"]:
            kwargs["headers"] = HEADERS_REQRES
        elif "httpstat.us" in prueba["url"]:
            kwargs["headers"] = HEADERS_HTTPSTAT
        # Si la prueba trae un body, lo mandamos como JSON
        if "body" in prueba:
            kwargs["json"] = prueba["body"]
        resultado = diagnosticar_url(prueba["metodo"], prueba["url"], **kwargs)
        resultados.append(resultado)
        estado = "✅" if resultado.get("exitoso") else "❌"
        print(f"{estado} {resultado['metodo']:6} {resultado.get('status','ERR')} — {resultado['url']}")

    tabla = {
        "total_pruebas":  len(resultados),
        "exitosas":       sum(1 for r in resultados if r.get("exitoso")),
        "fallidas":       sum(1 for r in resultados if not r.get("exitoso")),
        "resultados":     resultados,
    }
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(tabla, f, indent=2, ensure_ascii=False)
    return tabla


if __name__ == "__main__":
    pruebas = [
        {"metodo": "GET",    "url": "https://reqres.in/api/users/1"},
        {"metodo": "GET",    "url": "https://reqres.in/api/users/9999"},                       # 404
        {"metodo": "POST",   "url": "https://reqres.in/api/users",
         "body": {"name": "Ana Torres", "job": "Network Engineer"}},                            # 201
        {"metodo": "DELETE", "url": "https://reqres.in/api/users/2"},                          # 204
        {"metodo": "GET",    "url": "https://httpstat.us/500"},                                # 500
        {"metodo": "GET",    "url": "https://httpstat.us/401"},                                # 401
    ]
    tabla = generar_tabla_diagnostico(pruebas)
    print("\nResumen:", json.dumps({"total": tabla["total_pruebas"],
        "exitosas": tabla["exitosas"], "fallidas": tabla["fallidas"]}, indent=2))