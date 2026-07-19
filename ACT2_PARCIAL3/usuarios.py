import requests, json, os
from dotenv import load_dotenv

# Ruta absoluta al .env de este proyecto específico (funciona sin importar
# desde qué carpeta se ejecute el script)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path, override=True)

BASE    = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

# Headers que se reutilizan en todas las peticiones
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

TIMEOUT = 10  # segundos


def _debug(r):
    """Imprime detalles de la respuesta para diagnosticar errores."""
    print(f"  -> Status: {r.status_code}")
    print(f"  -> Respuesta: {r.text[:300]}")


# ── GET — listar usuarios ─────────────────────────────────────
def listar_usuarios(pagina=1):
    try:
        r = requests.get(
            f"{BASE}/users",
            params={"page": pagina},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        _debug(r)
        return r.json() if r.status_code == 200 else {"error": r.status_code, "detail": r.text}
    except requests.RequestException as e:
        return {"error": "request_failed", "detail": str(e)}


# ── POST — crear usuario ──────────────────────────────────────
def crear_usuario(nombre, puesto):
    try:
        r = requests.post(
            f"{BASE}/users",
            json={"name": nombre, "job": puesto},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        _debug(r)
        return r.json() if r.status_code == 201 else {"error": r.status_code, "detail": r.text}
    except requests.RequestException as e:
        return {"error": "request_failed", "detail": str(e)}


# ── PUT — actualizar usuario ──────────────────────────────────
def actualizar_usuario(user_id, nombre, puesto):
    try:
        r = requests.put(
            f"{BASE}/users/{user_id}",
            json={"name": nombre, "job": puesto},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        _debug(r)
        return r.json() if r.status_code == 200 else {"error": r.status_code, "detail": r.text}
    except requests.RequestException as e:
        return {"error": "request_failed", "detail": str(e)}


# ── DELETE — eliminar usuario ─────────────────────────────────
def eliminar_usuario(user_id):
    try:
        r = requests.delete(f"{BASE}/users/{user_id}", headers=HEADERS, timeout=TIMEOUT)
        _debug(r)
        return {"ok": True} if r.status_code == 204 else {"error": r.status_code, "detail": r.text}
    except requests.RequestException as e:
        return {"error": "request_failed", "detail": str(e)}


if __name__ == "__main__":
    print("Leyendo .env desde:", env_path)
    print("BASE:", BASE)
    print("API_KEY real:", API_KEY)
    print()

    print("Usuarios:", json.dumps(listar_usuarios(), indent=2))
    print("Nuevo:", json.dumps(crear_usuario("Ana Torres", "Network Engineer"), indent=2))
    print("Actualizado:", json.dumps(actualizar_usuario(2, "Ana Torres", "Senior NE"), indent=2))
    print("Eliminado:", json.dumps(eliminar_usuario(2), indent=2))