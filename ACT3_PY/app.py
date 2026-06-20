from flask import Flask, render_template, jsonify
import platform
import psutil
import os

app = Flask(__name__)

HOSTNAME = os.getenv('COMPUTERNAME', os.getenv('HOSTNAME', 'Servidor_Local'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/datos")
def datos():
    try:
        sistema_operativo = platform.system()

        # Captura instantánea de CPU (intervalo pequeño para no congelar la petición web)
        uso_cpu = int(psutil.cpu_percent(interval=0.05))
        uso_ram = int(psutil.virtual_memory().percent)

        # Validación de ruta de disco según sistema operativo
        ruta_disco = 'C:\\' if sistema_operativo == 'Windows' else '/'
        try:
            uso_disco = int(psutil.disk_usage(ruta_disco).percent)
        except:
            uso_disco = 0

        # Captura y depuración estricta de procesos para evitar errores en JavaScript
        procesos_html = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                # Solo tomamos procesos accesibles y con datos válidos
                p_info = proc.info
                if p_info and p_info.get('name') and p_info.get('pid') is not None:
                    cpu_p = p_info.get('cpu_percent')
                    # Si el sistema devuelve None, lo convertimos a 0.0 de forma segura
                    p_info['cpu_percent'] = float(cpu_p) if cpu_p is not None else 0.0
                    procesos_html.append(p_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Ordenar por consumo de CPU y extraer los 5 principales
        top_cinco_html = sorted(procesos_html, key=lambda p: p['cpu_percent'], reverse=True)[:5]

        return jsonify({
            "status": "success",
            "os": sistema_operativo,
            "cpu": uso_cpu,
            "memoria": uso_ram,
            "disco": uso_disco,
            "procesos": top_cinco_html
        })

    except Exception as e:
        # En caso de un error interno, devolvemos un JSON seguro para que el HTML no se congele
        return jsonify({
            "status": "error",
            "os": platform.system(),
            "cpu": 0,
            "memoria": 0,
            "disco": 0,
            "procesos": []
        })

if __name__ == "__main__":
    # Ejecución en modo desarrollo
    app.run(debug=True, port=5000)