# Archivo: wismyip_updater.py
# Descripción: Detecta la IP pública, sincroniza el repositorio y la publica en GitHub (DynDNS).
# Se ejecuta en la Raspberry Pi mediante Cron.

import requests
import subprocess 
import sys 
import os

def ejecutar_comando_simple(comando, descripcion="Ejecutando comando Git"):
    """Ejecuta un comando de sistema simple e imprime el resultado."""
    print(f"--- {descripcion} ---")
    try:
        # Ejecuta el comando, lanza excepción si falla.
        # Captura stdout y stderr
        resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
        print(f"Comando '{' '.join(comando)}' completado con éxito.")
        
        # Imprime la salida si existe y no es el mensaje genérico de git
        if resultado.stdout.strip() and "up-to-date" not in resultado.stdout:
            print(f"  -> Salida: {resultado.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⛔️ ERROR al ejecutar '{' '.join(comando)}':")
        # Mostramos la salida de error de Git
        print(e.stderr.strip())
        return False
    except FileNotFoundError:
        print("⛔️ ERROR: Git no encontrado. Asegúrate de que Git esté instalado.")
        return False

def obtener_ip_publica():
    """Detecta y devuelve la IP pública actual."""
    URL = "https://api.ipify.org"
    try:
        respuesta = requests.get(URL, timeout=10) 
        respuesta.raise_for_status() 
        ip_publica = respuesta.text.strip()
        return ip_publica
    except requests.RequestException as e:
        print(f"Error al obtener la IP pública: {e}")
        return None
    
def leer_ip_anterior(nombre_archivo="ip.txt"):
    """Lee y devuelve la IP guardada del archivo."""
    try:
        with open(nombre_archivo, 'r') as f:
            return f.readline().strip() 
    except FileNotFoundError:
        return "" 

def escribir_ip_nueva(ip, nombre_archivo="ip.txt"):
    """Escribe la nueva IP en el archivo."""
    try:
        with open(nombre_archivo, 'w') as f:
            f.write(ip)
        print(f"Archivo {nombre_archivo} actualizado a {ip}")
    except Exception as e:
        print(f"Error al escribir en el archivo {nombre_archivo}: {e}")

def ejecutar_comandos_git():
    """Ejecuta los comandos Git (add, commit, push) para publicar el cambio."""
    
    # Comandos para subir los cambios
    comandos = [
        ["git", "add", "ip.txt"],
        ["git", "commit", "-m", "Auto-update IP"],
        ["git", "push", "origin", "master:main"] 
    ]

    for comando in comandos:
        if not ejecutar_comando_simple(comando, f"Ejecutando {comando[1]}"):
            # Si el commit no tiene cambios, salimos limpiamente.
            if comando[1] == "commit":
                continue 
            return 

    print("✅ ¡El repositorio remoto se ha actualizado con la nueva IP!")

def main():
    # Asegura que el script se ejecute en su propio directorio (necesario para Cron)
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__))) 
        print(f"Directorio actual: {os.getcwd()}")
    except Exception as e:
        print(f"Error al cambiar de directorio: {e}")
        return

    # PASO 1: SINCRONIZACIÓN (Solución al problema de edición manual)
    # Descarga la última IP conocida desde GitHub para evitar re-subir la misma IP.
    ejecutar_comando_simple(["git", "pull", "origin", "main"], "Sincronizando IP anterior desde GitHub")
    
    # PASO 2: Obtener las IPs
    ip_nueva = obtener_ip_publica() 
    if not ip_nueva:
        return 

    ip_anterior = leer_ip_anterior()

    # PASO 3: Comparar y Actualizar
    if ip_nueva != ip_anterior:
        print(f"IP ha cambiado: {ip_anterior} -> {ip_nueva}. ¡Iniciando actualización de Git!")
        
        escribir_ip_nueva(ip_nueva)
        ejecutar_comandos_git() 

    else:
        print(f"La IP ({ip_nueva}) no ha cambiado. No se requiere actualización.")

if __name__ == "__main__":
    main()