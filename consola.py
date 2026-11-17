# consola.py — la consola del framework, como msfconsole
# Comandos en español: ayuda, mostrar modulos, usar <modulo>,
# mostrar opciones, poner <opcion> <valor>, correr, volver, salir
# Solo para tu propia máquina o un objetivo con permiso.
#
# ¿Qué es esto?
# Es el esqueleto del framework: sin él, cada módulo sería un programa
# distinto. La consola es la que los carga y los corre, igual que
# msfconsole carga los módulos de Metasploit.
from modulos import cabeceras, escaner_nmap

# MODULOS es un diccionario.
# La llave es el nombre del módulo, como "vuln/http_headers",
# y el valor es el módulo en sí (el archivo modulos/cabeceras.py).
# Así la consola puede buscar un módulo por su nombre, igual que tú
# buscas algo en un diccionario por su llave.
# Cada módulo es un archivo en modulos/, con NOMBRE, DESCRIPCION,
# OPCIONES y una función run(opciones).
# Para agregar un módulo nuevo, se importa aquí y se agrega una
# línea en este diccionario, como la de escaner_nmap.
MODULOS = {
    cabeceras.NOMBRE: cabeceras,
    escaner_nmap.NOMBRE: escaner_nmap,
}


def mostrar_ayuda():
    # Esta función solo imprime los comandos, no devuelve nada.
    print("\nComandos:")
    print("  ayuda             muestra esta ayuda (en inglés: help)")
    print("  mostrar modulos   lista los módulos disponibles (show modules)")
    print("  usar <modulo>     elige un módulo (ej: usar vuln/http_headers)")
    print("  mostrar opciones  muestra las opciones del módulo elegido")
    print("  poner <opcion> <valor>  cambia una opción (ej: poner URL https://example.com)")
    print("  correr            corre el módulo elegido (run)")
    print("  volver            vuelve a no tener módulo elegido (back)")
    print("  salir             salir (exit)")


def main():
    # main() es el director, como en el Mini InfoForge.
    # modulo guarda el módulo elegido, o None si no hay ninguno.
    # None significa "nada", "vacío".
    # opciones guarda las opciones del módulo elegido, como URL.
    modulo = None
    opciones = {}
    print("D4rkSploit — framework personal de pruebas de penetración")
    print("Solo para tu propia máquina o un objetivo con permiso.")
    print("Escribe 'ayuda' para ver los comandos.")
    # while True es un bucle infinito: la consola no se cierra sola,
    # solo se sale con el comando salir, que hace break.
    while True:
        # El prompt cambia según tengas un módulo elegido o no,
        # igual que en msfconsole.
        # Si no hay módulo, el prompt es "darksploit> ".
        # Si hay módulo, es "darksploit(vuln/http_headers)> ".
        # f"..." es un f-string: mete el valor de modulo.NOMBRE
        # dentro del texto.
        if modulo is None:
            prompt = "darksploit> "
        else:
            prompt = f"darksploit({modulo.NOMBRE})> "
        # input() lee lo que escribes, .strip() le quita los espacios
        # de los lados, por si escribiste un espacio de más.
        # .lower() lo pasa todo a minúsculas, para que "Ayuda" y
        # "ayuda" sean lo mismo.
        texto = input(prompt).strip().lower()
        # Si escribiste solo Enter (texto vacío), no hacemos nada
        # y volvemos a mostrar el prompt.
        if texto == "":
            continue
        # texto.split() parte lo que escribiste en palabras.
        # "usar vuln/http_headers".split() da ["usar", "vuln/http_headers"].
        # partes[0] es el comando, partes[1] es el argumento.
        partes = texto.split()
        comando = partes[0]

        # Cada comando tiene su nombre en español y, entre paréntesis,
        # su nombre en inglés de Metasploit, por si lo ves en otro lado.
        # "in" con una tupla busca si el comando es uno de los dos:
        # comando in ("salir", "exit") es True si es "salir" o "exit".
        if comando in ("salir", "exit"):
            print("Hasta luego, Luis.")
            # break rompe el while True y se acaba el programa.
            break
        elif comando in ("ayuda", "help"):
            mostrar_ayuda()
        # mostrar modulos: len(partes) == 2 significa que escribiste
        # exactamente dos palabras, "mostrar" y "modulos".
        elif comando == "mostrar" and len(partes) == 2 and partes[1] == "modulos":
            print("\nMódulos disponibles:")
            # for nombre, mod in MODULOS.items() recorre el diccionario
            # por parejas llave-valor: nombre es la llave, mod es el valor.
            for nombre, mod in MODULOS.items():
                print(f"  {nombre}  —  {mod.DESCRIPCION}")
        elif comando == "mostrar" and len(partes) == 2 and partes[1] == "opciones":
            if modulo is None:
                print("Primero elige un módulo con 'usar <modulo>'.")
            else:
                print("\nOpciones:")
                # Recorremos las opciones por parejas llave-valor.
                for clave, valor in opciones.items():
                    print(f"  {clave} = {valor}")
        # show modules y show options también funcionan, por si los
        # escribes en inglés como en Metasploit.
        elif comando == "show" and len(partes) == 2 and partes[1] == "modules":
            print("\nMódulos disponibles:")
            for nombre, mod in MODULOS.items():
                print(f"  {nombre}  —  {mod.DESCRIPCION}")
        elif comando == "show" and len(partes) == 2 and partes[1] == "options":
            if modulo is None:
                print("Primero elige un módulo con 'usar <modulo>'.")
            else:
                print("\nOpciones:")
                for clave, valor in opciones.items():
                    print(f"  {clave} = {valor}")
        elif comando in ("usar", "use") and len(partes) == 2:
            nombre = partes[1]
            # in busca la llave en el diccionario: si el módulo existe.
            if nombre in MODULOS:
                modulo = MODULOS[nombre]
                # dict(modulo.OPCIONES) hace una COPIA de las opciones
                # del módulo. Si no copiáramos, 'poner' cambiaría las
                # opciones del módulo original para siempre, y eso
                # no queremos: cada vez que eliges el módulo, sus
                # opciones deben volver a su valor por defecto.
                opciones = dict(modulo.OPCIONES)
                print(f"[*] Módulo elegido: {nombre}")
            else:
                print(f"Ese módulo no existe. Prueba 'mostrar modulos'.")
        # poner necesita exactamente tres palabras: "poner", la opción
        # y el valor, por ejemplo "poner URL https://example.com".
        # Ojo: como todo el texto se pasa a minúsculas con .lower(),
        # la opción y el valor también quedan en minúsculas. Por eso
        # las opciones del módulo van en mayúsculas en el código,
        # pero aquí las comparamos con .upper(): "url".upper() es "URL".
        elif comando in ("poner", "set") and len(partes) == 3:
            if modulo is None:
                print("Primero elige un módulo con 'usar <modulo>'.")
            elif partes[1].upper() in opciones:
                opciones[partes[1].upper()] = partes[2]
                print(f"{partes[1].upper()} = {partes[2]}")
            else:
                print(f"Esa opción no existe en este módulo. Prueba 'mostrar opciones'.")
        elif comando in ("correr", "run"):
            if modulo is None:
                print("Primero elige un módulo con 'usar <modulo>'.")
            else:
                # Aquí la consola le pasa las opciones al módulo
                # y el módulo hace su trabajo.
                modulo.run(opciones)
        elif comando in ("volver", "back"):
            # volver olvida el módulo elegido y sus opciones.
            modulo = None
            opciones = {}
            print("[*] Sin módulo elegido.")
        else:
            print("Comando no reconocido. Escribe 'ayuda'.")


# Esta llamada, en la columna 0 y sin nada después, es la que
# arranca el programa: llama a main().
main()
