# dns.py — módulo recon/dns de D4rkSploit
# Pregunta al DNS de un dominio, con dig, la herramienta de Kali,
# y dice a qué IP apunta y qué registros tiene.
# Solo para tu propia máquina o un objetivo con permiso.
#
# ¿Qué es esto?
# dig no es de Python, es un programa externo que trae Kali.
# Python no lo crea, solo lo llama con subprocess y lee lo que
# dig imprime, igual que hicimos con nmap en scan/nmap.
# DNS es el sistema que traduce un nombre, como example.com,
# a una IP, como 93.184.216.34, para que tu máquina sepa
# a dónde conectarse.
import subprocess

# NOMBRE es como se ve el módulo en la consola: recon/dns.
NOMBRE = "recon/dns"
# DESCRIPCION es lo que sale en "mostrar modulos".
DESCRIPCION = "Pregunta al DNS de un dominio con dig (IP y registros)"

# OPCIONES son los datos que el módulo necesita.
# DOMINIO es el nombre a consultar, sin https:// y sin / al final.
OPCIONES = {"DOMINIO": "example.com"}


def preguntar(dominio, tipo):
    # Pregunta un solo tipo de registro con dig.
    # ["dig", "+short", dominio, tipo] es el comando completo:
    # dig +short example.com A
    # +short le pide a dig que imprima solo la respuesta, sin
    # el texto largo de la consulta.
    # A es la IP del dominio, MX es el servidor de correo,
    # NS es el servidor de nombres que responde por ese dominio.
    try:
        resultado = subprocess.run(
            ["dig", "+short", dominio, tipo],
            capture_output=True, text=True, timeout=15
        )
    except FileNotFoundError:
        # FileNotFoundError es "no encontré el programa dig".
        return None, "dig no está instalado"
    except subprocess.TimeoutExpired:
        return None, "dig tardó demasiado (más de 15 segundos)"

    # strip() quita los espacios y saltos de línea de los bordes.
    # splitlines() parte la respuesta en líneas, una por registro.
    lineas = [linea.strip() for linea in resultado.stdout.splitlines() if linea.strip()]
    return lineas, None


def run(opciones):
    # opciones es el diccionario con DOMINIO.
    dominio = opciones["DOMINIO"]
    print(f"[*] Consultando DNS de {dominio} con dig ...")

    # Cada tipo de registro se pregunta por separado.
    # Un diccionario: la llave es el tipo, el valor es para qué sirve.
    tipos = {
        "A": "la IP del dominio",
        "MX": "el servidor de correo",
        "NS": "el servidor de nombres",
    }
    total = 0
    for tipo, para_que in tipos.items():
        lineas, error = preguntar(dominio, tipo)
        if error:
            print(f"[!] {tipo}: {error}")
            continue
        if not lineas:
            print(f"[-] {tipo}: sin registros ({para_que})")
            continue
        total += len(lineas)
        print(f"[+] {tipo} ({para_que}):")
        for linea in lineas:
            print(f"    {linea}")

    print(f"\n[*] Registros encontrados: {total}")
    if total == 0:
        print("[!] No se encontró nada: revisa que el dominio esté bien escrito.")
