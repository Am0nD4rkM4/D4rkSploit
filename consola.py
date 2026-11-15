# consola.py — la consola del framework, como msfconsole
# Comandos: help, show modules, use <modulo>, show options,
# set <opcion> <valor>, run, back, exit
# Solo para tu propia máquina o un objetivo con permiso.
#
# ¿Qué es esto?
# Es el esqueleto del framework: sin él, cada módulo sería un programa
# distinto. La consola es la que los carga y los corre, igual que
# msfconsole carga los módulos de Metasploit.
from modulos import cabeceras

# MODULOS es un diccionario.
# La llave es el nombre del módulo, como "vuln/http_headers",
# y el valor es el módulo en sí (el archivo modulos/cabeceras.py).
# Así la consola puede buscar un módulo por su nombre, igual que tú
# buscas algo en un diccionario por su llave.
# Cada módulo es un archivo en modulos/, con NOMBRE, DESCRIPCION,
# OPCIONES y una función run(opciones).
MODULOS = {
    cabeceras.NOMBRE: cabeceras,
}


def mostrar_ayuda():
    # Esta función solo imprime los comandos, no devuelve nada.
    print("\nComandos:")
    print("  help              muestra esta ayuda")
    print("  show modules      lista los módulos disponibles")
    print("  use <modulo>      elige un módulo (ej: use vuln/http_headers)")
    print("  show options      muestra las opciones del módulo elegido")
    print("  set <opcion> <valor>   cambia una opción (ej: set URL https://example.com)")
    print("  run               corre el módulo elegido")
    print("  back              vuelve a no tener módulo elegido")
    print("  exit              salir")


def main():
    # main() es el director, como en el Mini InfoForge.
    # modulo guarda el módulo elegido, o None si no hay ninguno.
    # None significa "nada", "vacío".
    # opciones guarda las opciones del módulo elegido, como URL.
    modulo = None
    opciones = {}
    print("D4rkSploit — framework personal de pruebas de penetración")
    print("Solo para tu propia máquina o un objetivo con permiso.")
    print("Escribe 'help' para ver los comandos.")
    # while True es un bucle infinito: la consola no se cierra sola,
    # solo se sale con el comando exit, que hace break.
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
        texto = input(prompt).strip()
        # Si escribiste solo Enter (texto vacío), no hacemos nada
        # y volvemos a mostrar el prompt.
        if texto == "":
            continue
        # texto.split() parte lo que escribiste en palabras.
        # "use vuln/http_headers".split() da ["use", "vuln/http_headers"].
        # partes[0] es el comando, partes[1] es el argumento.
        partes = texto.split()
        comando = partes[0]

        if comando == "exit":
            print("Hasta luego, Luis.")
            # break rompe el while True y se acaba el programa.
            break
        elif comando == "help":
            mostrar_ayuda()
        # show modules: len(partes) == 2 significa que escribiste
        # exactamente dos palabras, "show" y "modules".
        elif comando == "show" and len(partes) == 2 and partes[1] == "modules":
            print("\nMódulos disponibles:")
            # for nombre, mod in MODULOS.items() recorre el diccionario
            # por parejas llave-valor: nombre es la llave, mod es el valor.
            for nombre, mod in MODULOS.items():
                print(f"  {nombre}  —  {mod.DESCRIPCION}")
        elif comando == "show" and len(partes) == 2 and partes[1] == "options":
            if modulo is None:
                print("Primero elige un módulo con 'use <modulo>'.")
            else:
                print("\nOpciones:")
                # Recorremos las opciones por parejas llave-valor.
                for clave, valor in opciones.items():
                    print(f"  {clave} = {valor}")
        elif comando == "use" and len(partes) == 2:
            nombre = partes[1]
            # in busca la llave en el diccionario: si el módulo existe.
            if nombre in MODULOS:
                modulo = MODULOS[nombre]
                # dict(modulo.OPCIONES) hace una COPIA de las opciones
                # del módulo. Si no copiáramos, 'set' cambiaría las
                # opciones del módulo original para siempre, y eso
                # no queremos: cada vez que eliges el módulo, sus
                # opciones deben volver a su valor por defecto.
                opciones = dict(modulo.OPCIONES)
                print(f"[*] Módulo elegido: {nombre}")
            else:
                print(f"Ese módulo no existe. Prueba 'show modules'.")
        # set necesita exactamente tres palabras: "set", la opción
        # y el valor, por ejemplo "set URL https://example.com".
        elif comando == "set" and len(partes) == 3:
            if modulo is None:
                print("Primero elige un módulo con 'use <modulo>'.")
            elif partes[1] in opciones:
                opciones[partes[1]] = partes[2]
                print(f"{partes[1]} = {partes[2]}")
            else:
                print(f"Esa opción no existe en este módulo. Prueba 'show options'.")
        elif comando == "run":
            if modulo is None:
                print("Primero elige un módulo con 'use <modulo>'.")
            else:
                # Aquí la consola le pasa las opciones al módulo
                # y el módulo hace su trabajo.
                modulo.run(opciones)
        elif comando == "back":
            # back olvida el módulo elegido y sus opciones.
            modulo = None
            opciones = {}
            print("[*] Sin módulo elegido.")
        else:
            print("Comando no reconocido. Escribe 'help'.")


# Esta llamada, en la columna 0 y sin nada después, es la que
# arranca el programa: llama a main().
main()
