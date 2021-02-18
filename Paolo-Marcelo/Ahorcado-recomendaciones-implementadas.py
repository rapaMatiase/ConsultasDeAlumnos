
import os
import random

palabraAdivinada = []
letrasEscritas = []
intentos = 6
palabraSecretaAjustes = "1"
nombreArchivoGrupos = "grupos.txt"


def prepararPalabra(original):
    global palabraAdivinada
    original = original.lower()
    palabraAdivinada = []
    for letra in original:
        palabraAdivinada.append({
            "letra": letra,
            "adivinada": False,
        })

def imprimirPalabra():
    for letraCompuesta in palabraAdivinada: 
        if letraCompuesta["adivinada"]:
            print(letraCompuesta["letra"], end="")
        else:
            print("-", end="")
    print("")


def imprimirPalabraOriginal():
    for letraCompuesta in palabraAdivinada:
        print(letraCompuesta["letra"], end="")


def descubrirLetra(letraDeUsuario):
    global palabraAdivinada
    global letrasEscritas
    global intentos
    letraDeUsuario = letraDeUsuario.lower()
    if letraDeUsuario in letrasEscritas:
        return
    else:
        letrasEscritas.append(letraDeUsuario)
    if not letraEstaEnPalabra(letraDeUsuario):
        intentos -= 1
    else:
        for letraCompuesta in palabraAdivinada:
            if letraCompuesta["letra"] == letraDeUsuario:
                letraCompuesta["adivinada"] = True


def letraEstaEnPalabra(letra):
    global palabraAdivinada
    for letraCompuesta in palabraAdivinada:
        if letraCompuesta["letra"] == letra:
            return True
    return False


"""
CONSEJO 2
Los dibujos estan muy lindos, pero agrega un monton de lienas
repetidas en el codigo. Al ser caracteres de texto estaticos, se podrian
guardar en archivos de texto en una carpeta.
"""

def imprimirAhorcado():
    file_intento = "Dibujos/intento-{}.txt".format(intentos)
    f = open(file_intento, "r")
    print(f.read())

def dibujarIntentos():
    print("Intentos restantes: " + str(intentos))


def haGanado():
    global palabraAdivinada
    for letra in palabraAdivinada:
        if not letra["adivinada"]:
            return False
    return True


def instrucciones():
    print("""
INSTRUCCIONES
El objetivo de este juego es descubrir una palabra adivinando las letras que la componen.
1. Debes seleccionar de qué conjunto de palabras quisieras jugar
2. Inicias con """ + str(intentos) + " vidas" +
          """
3. Ingresa una letra que creas vaya en la palabra a adivinar
Suerte con el juego
""")


def obtenerPalabra():
    print("Jugar con: ")
    grupos = obtenerGrupos()
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupo = grupos[indice]
    palabras = obtenerPalabrasDeGrupo(grupo)
    return random.choice(palabras)


def jugar():
    global letrasEscritas
    global intentos
    intentos = 6
    letrasEscritas = []
    palabra = obtenerPalabra()
    prepararPalabra(palabra)
    while True:
        imprimirAhorcado()
        dibujarIntentos()
        imprimirPalabra()
        descubrirLetra(input("Ingresa la letra: ")) 
        if intentos <= 0:
            print("Perdiste. La palabra era: ")
            imprimirPalabraOriginal()
            return
        if haGanado():
            print("Ganaste")
            return


def ajustes():
    if input("Ingrese la contraseña: ") != palabraSecretaAjustes:
        print("Contraseña incorrecta")
        return
    menu = """
1. Eliminar grupo de palabras
2. Crear grupo de palabras
3. Modificar grupo de palabras
"""
    grupos = obtenerGrupos()

    eleccion = int(input(menu))
    if eleccion <= 0 or eleccion > 3:
        print("No válido")
        return
    if eleccion == 1:
        eliminarGrupoDePalabras(grupos)
    elif eleccion == 2:
        crearGrupoDePalabras(grupos)
    elif eleccion == 3:
        modificarGrupoDePalabras(grupos)


def eliminarGrupoDePalabras(grupos):
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupoEliminado = grupos[indice]
    del grupos[indice]
    os.unlink(grupoEliminado + ".txt")
    escribirGrupos(grupos)


def imprimirGruposYSolicitarIndice(grupos):
    for i, grupo in enumerate(grupos):
        print(f"{i + 1}. {grupo}")
    return int(input("Seleccione el grupo: ")) - 1


def crearGrupoDePalabras(grupos):
    grupo = input("Ingrese el nombre del grupo: ")
    palabras = solicitarPalabrasParaNuevoGrupo()
    escribirPalabrasDeGrupo(palabras, grupo)
    grupos.append(grupo)
    escribirGrupos(grupos)
    print("Grupo creado correctamente")


def escribirGrupos(grupos):
    with open(nombreArchivoGrupos, "w") as archivo:
        for grupo in grupos:
            archivo.write(grupo + "\n")


def escribirPalabrasDeGrupo(palabras, grupo):
    with open(grupo + ".txt", "w") as archivo:
        for palabra in palabras:
            archivo.write(palabra + "\n")


def solicitarPalabrasParaNuevoGrupo():
    palabras = []
    while True:
        palabra = input("Ingrese la palabra. Deje la cadena vacía si quiere terminar: ")
        if palabra == "":
            return palabras
        palabras.append(palabra)


def modificarGrupoDePalabras(grupos):
    indice = imprimirGruposYSolicitarIndice(grupos)
    grupoQueSeCambia = grupos[indice]
    palabras = obtenerPalabrasDeGrupo(grupoQueSeCambia)
    menu = """
1. Cambiar una palabra
2. Agregar una palabra
3. Eliminar una palabra
Seleccione: """
    eleccion = int(input(menu))
    if eleccion <= 0 or eleccion > 3:
        print("No válido")
        return
    if eleccion == 1:
        cambiarUnaPalabra(grupoQueSeCambia, palabras)
    elif eleccion == 2:
        agregarUnaPalabra(grupoQueSeCambia, palabras)
    elif eleccion == 3:
        eliminarUnaPalabra(grupoQueSeCambia, palabras)


def cambiarUnaPalabra(grupo, palabras):
    indice = imprimirPalabrasYSolicitarIndice(palabras)
    palabraCambiada = palabras[indice]
    print("Se cambia la palabra " + palabraCambiada)
    nuevaPalabra = input("Ingrese la nueva palabra: ")
    palabras[indice] = nuevaPalabra
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra cambiada correctamente")


def agregarUnaPalabra(grupo, palabras):
    palabra = input("Ingrese la palabra que se agrega: ")
    palabras.append(palabra)
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra agregada correctamente")


def eliminarUnaPalabra(grupo, palabras):
    indice = imprimirPalabrasYSolicitarIndice(palabras)
    del palabras[indice]
    escribirPalabrasDeGrupo(palabras, grupo)
    print("Palabra eliminada correctamente")


def imprimirPalabrasYSolicitarIndice(palabras):   
    for i, palabra in enumerate(palabras):
        print(f"{i + 1}. {palabra}")
    return int(input("Seleccione la palabra: ")) - 1

"""
Aca tenes codigo repetido en estas dos fucniones, no se puede simplificar en una sola?
"""
def obtenerGrupos():
    grupos = []
    with open(nombreArchivoGrupos) as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            grupos.append(linea)
    return grupos


def obtenerPalabrasDeGrupo(grupo):
    palabras = []
    with open(grupo + ".txt") as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            palabras.append(linea)
    return palabras


def prepararArchivo():
    if not os.path.isfile(nombreArchivoGrupos):
        with open(nombreArchivoGrupos, "w") as archivo:
            archivo.write("")


"""
CONSEJO 3
Existen varios if para los menus, se podira cambiar algunos de estos por diccionarios.
"""
diccionario_menu = {
    "1": jugar,
    "2": instrucciones,
    "3":ajustes
}

"""
CONSEJO 1
Al ser un juego por consola, es necesario imprimier mucho contenido por la 
consola para el juego. Por lo que seria razonable, crear una carpete de archivos donde 
tener un archivo de texto con el contenido de cada grafico o intrucciones. Asi el codigo
quedarama mas limpio. Te dejo un ejemplo. 
"""
def get_content_file(file_name):
    f = open(file_name, "r")
    content = f.read()
    return content

def menu_principal():
    menu = get_content_file("Archivos/menu.txt")
    print(menu)
    #Ya no hace falta hacer el pase a int eleccion = int(input(menu)) 
    eleccion = input(menu)
    valores_validos = diccionario_menu.keys()
    if not eleccion in valores_validos:
        exit()
    else:
        diccionario_menu[eleccion]()

def main():
    prepararArchivo()
    while True:
        menu_principal()


main()
