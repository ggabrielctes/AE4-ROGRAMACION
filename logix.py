MAX_MODULOS = 15
MAX_ECUACIONES = 5
ARCHIVOS_MATRIZ = ["matriz_actual.txt", "matriz_reestructurada.txt", "subgrafo_anexo.txt"]


# ---------- Utilidades de entrada y salida ----------

# Completa un texto con espacios hasta el ancho pedido (para alinear columnas)
def rellenar(texto, ancho):
    texto = str(texto)
    while len(texto) < ancho:
        texto = texto + " "
    return texto


# Une los elementos de una lista en un solo texto, con un separador entre ellos
def unir(lista, separador):
    texto = ""
    for i in range(len(lista)):
        if i > 0:
            texto = texto + separador
        texto = texto + str(lista[i])
    return texto


# Devuelve True si el texto es un número entero (con signo opcional)
def es_entero(texto):
    if len(texto) == 0:
        return False
    inicio = 0
    if texto[0] == "-":
        inicio = 1
    if inicio == len(texto):
        return False
    for i in range(inicio, len(texto)):
        if texto[i] < "0" or texto[i] > "9":
            return False
    return True


# Devuelve True si el texto es un número real (admite un punto decimal)
def es_numero(texto):
    puntos = 0
    sin_punto = ""
    for letra in texto:
        if letra == ".":
            puntos = puntos + 1
        else:
            sin_punto = sin_punto + letra
    return puntos <= 1 and es_entero(sin_punto)


# Pide un entero por teclado hasta que esté entre minimo y maximo
def leer_entero(mensaje, minimo, maximo):
    texto = input(mensaje).strip()
    while not es_entero(texto) or int(texto) < minimo or int(texto) > maximo:
        print("  Valor inválido. Debe ser un entero entre", minimo, "y", maximo)
        texto = input(mensaje).strip()
    return int(texto)


# Pide un número real por teclado hasta que sea válido
def leer_numero(mensaje):
    texto = input(mensaje).strip()
    while not es_numero(texto):
        print("  Valor inválido. Ingrese un número (ej.: 12 o 4.5)")
        texto = input(mensaje).strip()
    return float(texto)


# Muestra un número sin decimales si es entero, o con 2 decimales si no
def formato(numero):
    numero = round(numero, 2)
    if numero == int(numero):
        return str(int(numero))
    return str(numero)


# Muestra una matriz con los códigos como encabezado de filas y columnas
def mostrar_matriz(codigos, matriz, titulo):
    print()
    print(titulo)
    linea = "      "
    for c in codigos:
        linea = linea + rellenar(c, 5)
    print(linea)
    for i in range(len(matriz)):
        linea = rellenar(codigos[i], 6)
        for j in range(len(matriz[i])):
            linea = linea + rellenar(matriz[i][j], 5)
        print(linea)


# Lee las líneas útiles de un archivo (sin vacías ni comentarios con #)
def leer_lineas(ruta):
    lineas = []
    archivo = open(ruta, "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if len(linea) > 0 and linea[0] != "#":
            lineas.append(linea)
    archivo.close()
    return lineas


# ---------- TDA Cola (lista + posición del frente) ----------

# Crea una cola vacía: [elementos, posición del frente]
def crear_cola():
    return [[], 0]


# Agrega un dato al final de la cola
def encolar(cola, dato):
    cola[0].append(dato)


# Devuelve el dato del frente y avanza el frente una posición
def desencolar(cola):
    dato = cola[0][cola[1]]
    cola[1] = cola[1] + 1
    return dato


# Devuelve True si ya no quedan datos por atender
def cola_vacia(cola):
    return cola[1] == len(cola[0])


# ---------- TDA Grafo (lista de códigos + matriz de adyacencia) ----------

# Crea una matriz de n filas y m columnas llena de ceros
def matriz_ceros(n, m):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(m):
            fila.append(0)
        matriz.append(fila)
    return matriz


# Copia una matriz elemento por elemento
def copiar_matriz(matriz):
    copia = []
    for fila in matriz:
        nueva = []
        for valor in fila:
            nueva.append(valor)
        copia.append(nueva)
    return copia


# Búsqueda secuencial: posición de un dato en la lista, o -1 si no está
def buscar_secuencial(lista, dato):
    for i in range(len(lista)):
        if lista[i] == dato:
            return i
    return -1


# ---------- Registros de módulos y carga de la matriz (entrada de RF3) ----------

# Carga los registros [código, nombre, descripción] (el archivo está ordenado por código)
def cargar_registros(ruta):
    registros = []
    for linea in leer_lineas(ruta):
        campos = linea.split(";")
        if len(campos) == 3:
            registros.append([campos[0].strip(), campos[1].strip(), campos[2].strip()])
    return registros


# Controla que los registros estén ordenados por código (lo necesita la búsqueda binaria)
def registros_ordenados(registros):
    for i in range(1, len(registros)):
        if registros[i - 1][0] > registros[i][0]:
            return False
    return True


# Búsqueda binaria de un código en los registros ordenados; cuenta las comparaciones
def buscar_binaria(registros, codigo):
    izquierda = 0
    derecha = len(registros) - 1
    comparaciones = 0
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        comparaciones = comparaciones + 1
        if registros[medio][0] == codigo:
            return medio, comparaciones
        if registros[medio][0] < codigo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1, comparaciones


# Búsqueda secuencial de un código en los registros; cuenta las comparaciones
def buscar_registro_secuencial(registros, codigo):
    for i in range(len(registros)):
        if registros[i][0] == codigo:
            return i, i + 1
    return -1, len(registros)


# Nombre de un módulo a partir de su código (o "-" si no tiene registro)
def nombre_modulo(registros, codigo):
    posicion, comparaciones = buscar_binaria(registros, codigo)
    if posicion == -1:
        return "-"
    return registros[posicion][1]


# Controla que la matriz sea cuadrada, de 0 y 1, y de hasta 15 módulos
def validar_matriz(codigos, matriz):
    n = len(codigos)
    if n == 0 or n > MAX_MODULOS:
        print("  La cantidad de módulos debe estar entre 1 y", MAX_MODULOS)
        return False
    if len(matriz) != n:
        print("  La matriz debe tener", n, "filas")
        return False
    for i in range(n):
        if len(matriz[i]) != n:
            print("  La fila", i + 1, "no tiene", n, "valores")
            return False
        for j in range(n):
            if matriz[i][j] != 0 and matriz[i][j] != 1:
                print("  La matriz solo admite 0 y 1")
                return False
    for i in range(n):
        for j in range(i + 1, n):
            if codigos[i] == codigos[j]:
                print("  Código repetido:", codigos[i])
                return False
    return True


# lee los códigos (primera línea) y la matriz de adyacencia de un archivo
def cargar_matriz_archivo(ruta):
    lineas = leer_lineas(ruta)
    if len(lineas) == 0:
        return [], []
    codigos = lineas[0].upper().split()
    matriz = []
    for k in range(1, len(lineas)):
        fila = []
        for valor in lineas[k].split():
            if valor == "1":
                fila.append(1)
            elif valor == "0":
                fila.append(0)
            else:
                fila.append(-1)
        matriz.append(fila)
    if not validar_matriz(codigos, matriz):
        return [], []
    return codigos, matriz


# carga los módulos y de quién depende cada uno por teclado
def cargar_matriz_teclado():
    n = leer_entero("Cantidad de módulos (1 a 15): ", 1, MAX_MODULOS)
    codigos = []
    for i in range(n):
        codigo = input("  Código del módulo " + str(i + 1) + ": ").strip().upper()
        while len(codigo) == 0 or buscar_secuencial(codigos, codigo) != -1:
            print("  Código vacío o repetido")
            codigo = input("  Código del módulo " + str(i + 1) + ": ").strip().upper()
        codigos.append(codigo)
    matriz = matriz_ceros(n, n)
    for i in range(n):
        texto = input("  " + codigos[i] + " depende de (códigos separados por espacio, Enter = ninguno): ")
        for destino in texto.upper().split():
            j = buscar_secuencial(codigos, destino)
            if j == -1:
                print("  ", destino, "no existe y se ignora")
            elif j == i:
                print("  Un módulo no puede depender de sí mismo; se ignora")
            else:
                matriz[i][j] = 1
    return codigos, matriz





# Posición del mayor valor de una lista (si hay empate, el primero)
def posicion_del_maximo(lista):
    mayor = 0
    for i in range(1, len(lista)):
        if lista[i] > lista[mayor]:
            mayor = i
    return mayor


# ---------- RF3: El sistema debe listar los módulos afectados por la modificación de un módulo ----------

# Producto booleano de matrices: c[i][j] = 1 si existe k con a[i][k] = 1 y b[k][j] = 1
def producto_booleano(a, b):
    n = len(a)
    c = matriz_ceros(n, n)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if a[i][k] == 1 and b[k][j] == 1:
                    c[i][j] = 1
    return c


# RF3: alcanzabilidad A* = A v A[2] v A[3] ... hasta que una potencia no agregue unos nuevos
def alcanzabilidad(matriz, mostrar_pasos):
    n = len(matriz)
    total = copiar_matriz(matriz)
    potencia = copiar_matriz(matriz)
    exponente = 1
    nuevos = 1
    while nuevos > 0 and exponente < n:
        exponente = exponente + 1
        potencia = producto_booleano(potencia, matriz)
        nuevos = 0
        for i in range(n):
            for j in range(n):
                if potencia[i][j] == 1 and total[i][j] == 0:
                    total[i][j] = 1
                    nuevos = nuevos + 1
        if mostrar_pasos:
            print("  A[" + str(exponente) + "] agrega", nuevos, "unos nuevos")
    return total


# Cuenta los unos de una matriz (pares de módulos alcanzables)
def contar_unos(matriz):
    total = 0
    for fila in matriz:
        for valor in fila:
            total = total + valor
    return total


# RF3: módulos afectados si se cambia el de la columna j (los 1 de esa columna de A*)
def afectados(codigos, total, j):
    lista = []
    for i in range(len(codigos)):
        if total[i][j] == 1 and i != j:
            lista.append(codigos[i])
    return lista



# ---------- Árbol de impacto (recorrido en anchura con la cola) ----------

# Arma el árbol de impacto: cada nodo es [código, código del padre, nivel]
def arbol_de_impacto(codigos, matriz, j):
    n = len(codigos)
    visitado = []
    for i in range(n):
        visitado.append(False)
    arbol = [[codigos[j], "-", 0]]
    visitado[j] = True
    cola = crear_cola()
    encolar(cola, [j, 0])
    while not cola_vacia(cola):
        elemento = desencolar(cola)
        actual = elemento[0]
        nivel = elemento[1]
        for i in range(n):
            if matriz[i][actual] == 1 and not visitado[i]:
                visitado[i] = True
                arbol.append([codigos[i], codigos[actual], nivel + 1])
                encolar(cola, [i, nivel + 1])
    return arbol


# Muestra el árbol nivel por nivel: cada módulo con el módulo que le pasó el cambio
def mostrar_arbol(arbol):
    nivel_maximo = arbol[len(arbol) - 1][2]
    print("  Nivel 0 (raíz): " + arbol[0][0])
    for nivel in range(1, nivel_maximo + 1):
        linea = "  Nivel " + str(nivel) + ": "
        for nodo in arbol:
            if nodo[2] == nivel:
                linea = linea + nodo[0] + " (por " + nodo[1] + ")  "
        print(linea)




# ---------- RF5: El sistema debe resolver sistemas de ecuaciones lineales de hasta 5 x 5 ----------

# Copia la matriz de coeficientes y le agrega los términos independientes como última columna
def armar_ampliada(coeficientes, terminos):
    ampliada = []
    for i in range(len(coeficientes)):
        fila = []
        for j in range(len(coeficientes)):
            fila.append(float(coeficientes[i][j]))
        fila.append(float(terminos[i]))
        ampliada.append(fila)
    return ampliada


# Si el pivote es 0, le suma una fila de abajo que tenga valor en esa columna (no cambia el det)
def arreglar_pivote(matriz, c):
    k = c + 1
    while k < len(matriz) and abs(matriz[k][c]) < 0.000001:
        k = k + 1
    if k == len(matriz):
        return False
    for j in range(len(matriz[c])):
        matriz[c][j] = matriz[c][j] + matriz[k][j]
    return True


# Determinante: 2x2 por fórmula, 3x3 por Sarrus, 4x4 y 5x5 por triangulación
def determinante(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    if n == 3:
        positivos = m[0][0] * m[1][1] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1]
        negativos = m[0][2] * m[1][1] * m[2][0] + m[0][0] * m[1][2] * m[2][1] + m[0][1] * m[1][0] * m[2][2]
        return positivos - negativos
    a = copiar_matriz(m)
    det = 1
    for c in range(n):
        if abs(a[c][c]) < 0.000001:
            if not arreglar_pivote(a, c):
                return 0
        det = det * a[c][c]
        for i in range(c + 1, n):
            factor = a[i][c] / a[c][c]
            for j in range(n):
                a[i][j] = a[i][j] - factor * a[c][j]
    return det


# Muestra la matriz ampliada [M | B] de un paso de Gauss-Jordan
def mostrar_ampliada(ampliada, operacion):
    print("  " + operacion)
    for fila in ampliada:
        linea = "    [ "
        for j in range(len(fila) - 1):
            linea = linea + rellenar(formato(fila[j]), 8)
        print(linea + "| " + formato(fila[len(fila) - 1]) + " ]")


# RF5: Gauss-Jordan sobre [M | B]; devuelve la solución o [] si no es compatible determinado
def gauss_jordan(coeficientes, terminos, mostrar_pasos):
    n = len(coeficientes)
    if abs(determinante(coeficientes)) < 0.000001:
        return []
    ampliada = armar_ampliada(coeficientes, terminos)
    if mostrar_pasos:
        mostrar_ampliada(ampliada, "Matriz ampliada inicial")
    for c in range(n):
        if abs(ampliada[c][c]) < 0.000001:
            arreglar_pivote(ampliada, c)
            if mostrar_pasos:
                mostrar_ampliada(ampliada, "Pivote nulo: a F" + str(c + 1) + " se le suma una fila de abajo")
        pivote = ampliada[c][c]
        for j in range(n + 1):
            ampliada[c][j] = ampliada[c][j] / pivote
        if mostrar_pasos:
            mostrar_ampliada(ampliada, "F" + str(c + 1) + " <- F" + str(c + 1) + " / " + formato(pivote))
        for i in range(n):
            if i != c and ampliada[i][c] != 0:
                factor = ampliada[i][c]
                for j in range(n + 1):
                    ampliada[i][j] = ampliada[i][j] - factor * ampliada[c][j]
                if mostrar_pasos:
                    mostrar_ampliada(ampliada, "F" + str(i + 1) + " <- F" + str(i + 1) + " - (" + formato(factor) + ") F" + str(c + 1))
    solucion = []
    for i in range(n):
        solucion.append(round(ampliada[i][n], 6))
    return solucion


# Verifica la solución sustituyendo en cada ecuación (M · X = B)
def verificar_solucion(coeficientes, terminos, solucion):
    for i in range(len(coeficientes)):
        suma = 0
        for j in range(len(solucion)):
            suma = suma + coeficientes[i][j] * solucion[j]
        if abs(suma - terminos[i]) > 0.001:
            return False
    return True


# Lee un sistema desde archivo: cada línea tiene los coeficientes y al final el término independiente
def cargar_sistema_archivo(ruta):
    coeficientes = []
    terminos = []
    for linea in leer_lineas(ruta):
        valores = linea.split()
        fila = []
        for k in range(len(valores) - 1):
            fila.append(float(valores[k]))
        coeficientes.append(fila)
        terminos.append(float(valores[len(valores) - 1]))
    return coeficientes, terminos


# Lee un sistema de hasta 5 x 5 por teclado
def cargar_sistema_teclado():
    n = leer_entero("Cantidad de incógnitas (1 a 5): ", 1, MAX_ECUACIONES)
    coeficientes = []
    terminos = []
    for i in range(n):
        print("  Ecuación", i + 1)
        fila = []
        for j in range(n):
            fila.append(leer_numero("    coeficiente " + str(j + 1) + ": "))
        coeficientes.append(fila)
        terminos.append(leer_numero("    término independiente: "))
    return coeficientes, terminos












# ---------- Opciones del menú ----------

def opcion_cargar_archivo():
    print("  Archivos disponibles:")
    for i in range(len(ARCHIVOS_MATRIZ)):
        print("   ", i + 1, "-", ARCHIVOS_MATRIZ[i])
    numero = leer_entero("  Elija un archivo: ", 1, len(ARCHIVOS_MATRIZ))
    return ARCHIVOS_MATRIZ[numero - 1]



def opcion_alcanzabilidad(codigos, matriz):
    total = alcanzabilidad(matriz, True)
    mostrar_matriz(codigos, total, "Matriz de alcanzabilidad A*")
    print("  Pares alcanzables (unos en A*):", contar_unos(total))
    impacto = []
    print("  Cantidad de módulos afectados si cambia cada uno:")
    for j in range(len(codigos)):
        impacto.append(len(afectados(codigos, total, j)))
        print("    " + rellenar(codigos[j], 6) + str(impacto[j]))
    i = posicion_del_maximo(impacto)
    print("  Mayor impacto:", codigos[i], "afecta a", impacto[i], "módulos")


def opcion_afectados(codigos, matriz):
    texto = input("Módulos que se modifican (códigos separados por espacio): ").upper().split()
    total = alcanzabilidad(matriz, False)
    impacto = []
    for codigo in texto:
        j = buscar_secuencial(codigos, codigo)
        if j == -1:
            print("  El módulo", codigo, "no existe y se ignora")
        else:
            lista = afectados(codigos, total, j)
            print("  Si cambia", codigo, "se afectan", len(lista), "módulos:", unir(lista, " "))
            print("  Árbol de impacto de " + codigo + ":")
            mostrar_arbol(arbol_de_impacto(codigos, matriz, j))
            if buscar_secuencial(impacto, codigo) == -1:
                impacto.append(codigo)
            for m in lista:
                if buscar_secuencial(impacto, m) == -1:
                    impacto.append(m)
    if len(impacto) > 0:
        print("  Impacto total del cambio:", len(impacto), "módulos ->", unir(impacto, " "))



def opcion_sistema():
    print("  1. Usar la Tabla 6 (sistema_tabla6.txt)")
    print("  2. Ingresar un sistema por teclado")
    if leer_entero("  Opción: ", 1, 2) == 1:
        coeficientes, terminos = cargar_sistema_archivo("sistema_tabla6.txt")
    else:
        coeficientes, terminos = cargar_sistema_teclado()
    det = determinante(coeficientes)
    print("  det(M) =", formato(det))
    if abs(det) < 0.000001:
        print("  det = 0: el sistema NO es compatible determinado (no tiene solución única)")
        return
    print("  det distinto de 0: sistema compatible determinado (solución única)")
    solucion = gauss_jordan(coeficientes, terminos, True)
    nombres = ["x", "y", "z", "w", "v"]
    for i in range(len(solucion)):
        print("  " + nombres[i] + " =", formato(solucion[i]))
    if verificar_solucion(coeficientes, terminos, solucion):
        print("  Verificación por sustitución: correcta")
    else:
        print("  Verificación por sustitución: NO coincide")







def opcion_buscar(registros):
    codigo = input("Código a buscar: ").strip().upper()
    posicion, comparaciones = buscar_registro_secuencial(registros, codigo)
    print("  Búsqueda secuencial:", comparaciones, "comparaciones")
    posicion, comparaciones = buscar_binaria(registros, codigo)
    print("  Búsqueda binaria:", comparaciones, "comparaciones")
    if posicion == -1:
        print("  No existe un módulo con código", codigo)
    else:
        r = registros[posicion]
        print("  " + r[0] + " | " + r[1] + " | " + r[2])



# ---------- Pruebas documentadas ----------

# Compara lo esperado con lo obtenido y muestra la prueba como en el informe
def probar(numero, descripcion, entrada, esperado, obtenido, contador):
    print()
    print("Prueba " + str(numero) + ": " + descripcion)
    print("  Entrada:  " + entrada)
    print("  Esperado: " + str(esperado))
    print("  Obtenido: " + str(obtenido))
    if esperado == obtenido:
        print("  Resultado: OK")
        contador[0] = contador[0] + 1
    else:
        print("  Resultado: FALLA")
        contador[1] = contador[1] + 1



# ---------- Menú principal ----------

def ejecutar_pruebas():
    contador = [0, 0]
    codigos, matriz = cargar_matriz_archivo("matriz_actual.txt")
    total = alcanzabilidad(matriz, False)
    codigos2, matriz2 = cargar_matriz_archivo("matriz_reestructurada.txt")
    total2 = alcanzabilidad(matriz2, False)

    probar(1, "Módulos afectados si cambia INV (RF3)", "matriz_actual.txt, módulo INV",
           ["PED", "ROB", "ASG", "RUT", "SEG", "ENT", "REP"],
           afectados(codigos, total, buscar_secuencial(codigos, "INV")), contador)
    probar(2, "Pares alcanzables antes y después de reestructurar (RF3)", "matriz_actual.txt y matriz_reestructurada.txt",
           [40, 35], [contar_unos(total), contar_unos(total2)], contador)
    probar(3, "Caso límite: módulo del que no depende nadie (RF3)", "matriz_actual.txt, módulo REP",
           [], afectados(codigos, total, buscar_secuencial(codigos, "REP")), contador)
    sub_codigos, sub_matriz = cargar_matriz_archivo("subgrafo_anexo.txt")
    probar(4, "Subgrafo del Anexo manual: unos de A* (RF3)", "subgrafo_anexo.txt",
           19, contar_unos(alcanzabilidad(sub_matriz, False)), contador)
    probar(5, "Caso límite: matriz con un valor distinto de 0 y 1", "fila con un 2",
           False, validar_matriz(["A", "B"], [[0, 2], [0, 0]]), contador)
    nombres = []
    for i in range(16):
        nombres.append("M" + str(i))
    probar(6, "Caso límite: más de 15 módulos", "16 módulos",
           False, validar_matriz(nombres, matriz_ceros(16, 16)), contador)

    coef, term = cargar_sistema_archivo("sistema_tabla6.txt")
    probar(7, "Sistema de la Tabla 6 por Gauss-Jordan (RF5)", "sistema_tabla6.txt",
           [11, [12, 20, 35]], [determinante(coef), gauss_jordan(coef, term, False)], contador)
    probar(8, "Caso límite: sistema con det = 0 (RF5)", "x + y = 2 ; 2x + 2y = 4",
           [0, []], [determinante([[1, 1], [2, 2]]), gauss_jordan([[1, 1], [2, 2]], [2, 4], False)], contador)
    probar(9, "Caso límite: primer pivote igual a 0 (RF5)", "0x + y = 3 ; x + y = 5",
           [2, 3], gauss_jordan([[0, 1], [1, 1]], [3, 5], False), contador)

    registros = cargar_registros("modulos.txt")
    probar(10, "Caso límite: búsqueda binaria de un código inexistente", "código XYZ",
           -1, buscar_binaria(registros, "XYZ")[0], contador)

    print()
    print("Pruebas correctas:", contador[0], "| Fallidas:", contador[1])


# ---------- Menú principal ----------

def mostrar_menu(archivo_actual):
    print()
    print("-------------------- LOGIX-Analyzer --------------------")
    print(" Sistema cargado:", archivo_actual)
    print("  1. Cargar sistema desde archivo")
    print("  2. Cargar sistema desde teclado")
    print("  3. Ver la matriz de alcanzabilidad (base de RF3)")
    print("  4. Listar los módulos afectados por la modificación de un módulo (RF3)")
    print("  5. Resolver un sistema de ecuaciones lineales de hasta 5 x 5 (RF5)")
    print("  6. Buscar un módulo por código")
    print("  7. Ejecutar las pruebas")
    print("  0. Salir")


def menu():
    registros = cargar_registros("modulos.txt")
    if not registros_ordenados(registros):
        print("Aviso: modulos.txt no está ordenado por código; la búsqueda binaria puede fallar")
    archivo_actual = "matriz_actual.txt"
    codigos, matriz = cargar_matriz_archivo(archivo_actual)
    opcion = -1
    while opcion != 0:
        mostrar_menu(archivo_actual)
        opcion = leer_entero("Opción: ", 0, 7)
        if opcion == 1:
            ruta = opcion_cargar_archivo()
            nuevos_codigos, nueva_matriz = cargar_matriz_archivo(ruta)
            if len(nuevos_codigos) > 0:
                codigos = nuevos_codigos
                matriz = nueva_matriz
                archivo_actual = ruta
                mostrar_matriz(codigos, matriz, "Matriz cargada")
        elif opcion == 2:
            codigos, matriz = cargar_matriz_teclado()
            archivo_actual = "(teclado)"
            mostrar_matriz(codigos, matriz, "Matriz cargada")
        elif opcion == 3:
            opcion_alcanzabilidad(codigos, matriz)
        elif opcion == 4:
            opcion_afectados(codigos, matriz)
        elif opcion == 5:
            opcion_sistema()
        elif opcion == 6:
            opcion_buscar(registros)
        elif opcion == 7:
            ejecutar_pruebas()
    print("Fin del programa.")


if __name__ == "__main__":
    menu()
