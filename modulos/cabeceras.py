# modulos/cabeceras.py — módulo vuln/http_headers
# Revisa las cabeceras de seguridad de una web y dice cuáles faltan.
# No rompe nada: solo lee cabeceras, como un navegador.
import urllib.request

# Nombre que se usa en la consola con "use"
NOMBRE = "vuln/http_headers"
DESCRIPCION = "Revisa cabeceras de seguridad de una web (faltan = más expuesta)"

# Las opciones que pide este módulo, con su valor por defecto.
# URL es la dirección de la web a revisar.
OPCIONES = {"URL": "https://example.com"}

# Las cabeceras de seguridad que buscamos.
# Cada una protege de algo distinto; si falta, la web queda más expuesta.
CABECERAS_SEGURIDAD = {
    "Strict-Transport-Security": "obliga a usar HTTPS",
    "Content-Security-Policy": "limita de dónde se carga contenido",
    "X-Frame-Options": "evita que la web se meta en un iframe (clickjacking)",
    "X-Content-Type-Options": "evita que el navegador adivine el tipo de archivo",
    "Referrer-Policy": "controla qué se envía en el Referer",
    "Permissions-Policy": "limita cámara, micrófono y geolocalización",
}


def run(opciones):
    url = opciones["URL"]
    print(f"[*] Revisando {url} ...")
    try:
        respuesta = urllib.request.urlopen(url, timeout=5)
    except Exception as error:
        print(f"[!] No se pudo conectar: {error}")
        return

    # Pasamos las cabeceras a minúsculas para comparar sin importar
    # si el servidor las escribe en mayúsculas o minúsculas.
    cabeceras = {}
    for clave, valor in respuesta.headers.items():
        cabeceras[clave.lower()] = valor

    presentes = 0
    total = len(CABECERAS_SEGURIDAD)
    for nombre, para_que in CABECERAS_SEGURIDAD.items():
        if nombre.lower() in cabeceras:
            print(f"[+] {nombre}: presente ({para_que})")
            presentes += 1
        else:
            print(f"[-] {nombre}: FALTA ({para_que})")

    print(f"\n[*] Seguridad de cabeceras: {presentes}/{total}")
    if presentes == total:
        print("[+] Bien: todas las cabeceras de seguridad están presentes.")
    elif presentes == 0:
        print("[!] Mal: no hay ninguna cabecera de seguridad.")
    else:
        print("[!] Revisa las que faltan: cada una que falta deja un hueco.")
