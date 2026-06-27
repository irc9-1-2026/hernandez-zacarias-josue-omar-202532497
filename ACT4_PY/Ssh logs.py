"""
ssh_logs.py — Lectura remota de archivos de log mediante SSH
Autor: Josue Omar Hernandez Zacarias
Descripción: Establece una conexión SSH segura y recupera el contenido
             de un archivo de log alojado en un servidor remoto.
"""

import paramiko


def leer_log_remoto(
    host: str,
    usuario: str,
    password: str,
    ruta_remota: str,
    puerto: int = 22,
    timeout: int = 8,
) -> str:
    """
    Se conecta a un servidor remoto mediante SSH y retorna el contenido
    del archivo de log especificado como cadena de texto.

    Lanza FileNotFoundError si el archivo no existe en el servidor remoto.
    """
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        cliente.connect(
            hostname=host,
            port=puerto,
            username=usuario,
            password=password,
            timeout=timeout,
        )

        _, stdout, stderr = cliente.exec_command(f"cat {ruta_remota}")

        contenido = stdout.read().decode("utf-8", errors="replace")
        errores   = stderr.read().decode("utf-8", errors="replace")

        if errores:
            raise FileNotFoundError(
                f"El servidor reportó un error al leer '{ruta_remota}': {errores.strip()}"
            )

        return contenido

    finally:
        cliente.close()