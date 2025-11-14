import requests
import subprocess 
import sys # Añadimos sys para un exit más limpio en caso de fallo

def obtener_ip_publica():
    """Detecta y devuelve la IP pública actual utilizando un servicio externo."""
    URL = "https://api.ipify.org"
    try:
        respuesta = requests.get(URL, timeout=10) # Añadimos timeout para ser robustos
        respuesta.raise_for_status() 
        ip_publica = respuesta.text.strip()
        return ip_publica
    except requests.RequestException as e:
        print(f"Error al obtener la IP pública: {e}")
        return None

#Funcion que lee la ip guardada en el archivo ip.txt
def leer_ip_anterior(nombre_archivo="ip.txt"):
    """Lee y devuelve la IP guardada del archivo."""
    try:
        with open(nombre_archivo, 'r') as f:
            return f.readline().strip() 
    except FileNotFoundError:
        # Devuelve "" si el archivo no existe
        return "" 

#Funcion que guarda la nueva ip en el arhivo si cambio
def escribir_ip_nueva(ip, nombre_archivo="ip.txt"):
    """Escribe la nueva IP en el archivo."""
    try:
        with open(nombre_archivo, 'w') as f:
            f.write(ip)
        print(f"Archivo {nombre_archivo} actualizado a {ip}")
    except Exception as e:
        print(f"Error al escribir en el archivo {nombre_archivo}: {e}")

#Ejecutamos los comandos git, para subir nuestra nueva ip al repositorio
def ejecutar_comandos_git():
    """Ejecuta los comandos Git necesarios para publicar el cambio de IP."""
    
    # Lista de comandos a ejecutar
    comandos = [
        ["git", "add", "ip.txt"],
        # Si no hay cambios, 'git commit' fallará, pero el check=True
        # es mejor dejarlo para detectar otros errores
        ["git", "commit", "-m", "Auto-update IP"],
        ["git", "push", "origin", "main"] # Asume que tu rama principal es 'main'
    ]

    for comando in comandos:
        try:
            # Ejecuta el comando. 'check=True' lanza un error si el comando falla.
            # Agregamos stderr y stdout al output
            resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
            print(f"Comando {' '.join(comando)} completado con éxito.")
            # Imprime el output de Git
            if resultado.stdout:
                print(f"  -> {resultado.stdout.strip()}")
            
        except subprocess.CalledProcessError as e:
            # Esto captura errores de Git (ej. no hay conexión o no hay 'origin')
            print(f"⛔️ Error al ejecutar {' '.join(comando)}:")
            print(e.stderr)
            # Manejamos un caso especial: si commit no tiene nada que hacer
            if "nothing to commit" in e.stderr:
                print("⚠️ Git commit ejecutado sin cambios, continuando con push...")
                continue # Pasa al siguiente comando (push)
            return # Detiene la ejecución si hay un error de Git grave
        except FileNotFoundError:
            print("⛔️ ERROR: Git no encontrado. Asegúrate de que Git esté instalado.")
            return
            print("✅ ¡El repositorio remoto se ha actualizado con la nueva IP!")

#Ejecucion de programa. comprobamos ip, verificamos con archivo y llamamos a git si cambio
def main():
    ip_nueva = obtener_ip_publica() 
    if ip_nueva:
        ip_anterior = leer_ip_anterior()

        # Compara las IPs para determinar si se necesita la actualización de Git
        if ip_nueva != ip_anterior:
            print(f"IP ha cambiado: {ip_anterior} -> {ip_nueva}. ¡Iniciando actualización de Git!")
            
            # 1. Actualizar el archivo local
            escribir_ip_nueva(ip_nueva)
            
            # 2. Ejecutar los comandos de Git
            ejecutar_comandos_git() 

        else:
            print(f"La IP ({ip_nueva}) no ha cambiado. No se requiere actualización.")
    else:
        print("No se pudo obtener la IP pública. Saliendo...")


# Punto de entrada del script, esto ejecuta esto en primer lugar
if __name__ == "__main__":
    main()