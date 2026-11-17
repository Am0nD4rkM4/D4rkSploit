# escaner_nmap.py — módulo scan/nmap de D4rkSploit
# Escanea puertos con nmap, la herramienta de Kali, y dice
# qué puertos están abiertos y qué servicio hay en cada uno.
# Solo para tu propia máquina o un objetivo con permiso.
#
# ¿Qué es esto?
# nmap no es de Python, es un programa externo que trae Kali.
# Python no lo crea, solo lo llama con subprocess y lee lo que
# nmap imprime, igual que si lo corrieras tú en la terminal.
import subprocess

# NOMBRE es como se ve el módulo en la consola: scan/nmap.
NOMBRE = "scan/nmap"
# DESCRIPCION es lo que sale en "mostrar modulos".
DESCRIPCION = "Escanea puertos con nmap y dice qué servicio hay en cada uno"

# OPCIONES son los datos que el módulo necesita.
# OBJETIVO es la máquina a escanear, 127.0.0.1 es tu propia máquina.
# PUERTOS son los puertos a revisar, separados por comas.
OPCIONES = {"OBJETIVO": "127.0.0.1", "PUERTOS": "22,80,443"}


def run(opciones):
    # opciones es el diccionario con OBJETIVO y PUERTOS.
    objetivo = opciones["OBJETIVO"]
    puertos = opciones["PUERTOS"]
    print(f"[*] Escaneando {objetivo} (puertos {puertos}) con nmap ...")
    try:
        # subprocess.run corre un programa externo y espera a que termine.
        # ["nmap", "-sV", "-p", puertos, objetivo] es el comando completo:
        # nmap -sV -p 22,80,443 127.0.0.1
        # -sV le pide a nmap que averigüe qué servicio hay en cada puerto.
        # -p le dice qué puertos revisar.
        # capture_output=True guarda lo que nmap imprime, en vez de
        # dejarlo salir directo a la pantalla.
        # text=True lo guarda como texto, no como bytes.
        resultado = subprocess.run(
            ["nmap", "-sV", "-p", puertos, objetivo],
            capture_output=True, text=True, timeout=60
        )
    except FileNotFoundError:
        # FileNotFoundError es "no encontré el programa nmap".
        print("[!] nmap no está instalado en esta máquina.")
        print("[!] En Kali viene instalado. Prueba con: sudo apt install nmap")
        return
    except subprocess.TimeoutExpired:
        # TimeoutExpired es "pasaron 60 segundos y nmap no terminó".
        print("[!] nmap tardó demasiado (más de 60 segundos).")
        return

    # returncode es 0 si nmap terminó bien, otro número si falló.
    if resultado.returncode != 0:
        print(f"[!] nmap falló: {resultado.stderr.strip()}")
        return

    # resultado.stdout es todo lo que nmap imprimió, como un texto largo.
    # splitlines() lo parte en líneas, una por renglón.
    abiertos = 0
    for linea in resultado.stdout.splitlines():
        # Las líneas de puertos dicen algo como "22/tcp open ssh".
        # Si la línea tiene "/tcp" o "/udp", es una línea de puerto.
        if "/tcp" in linea or "/udp" in linea:
            print(f"    {linea.strip()}")
            # Si además dice "open", ese puerto está abierto.
            if "open" in linea:
                abiertos += 1

    print(f"\n[*] Puertos abiertos: {abiertos}")
    if abiertos == 0:
        print("[+] Bien: ningún puerto de los revisados está abierto.")
    else:
        print("[!] Revisa los puertos abiertos: cada uno es una puerta de entrada.")
