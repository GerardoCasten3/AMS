import random

numero_individuos = 20  # Número de individuos en la población inicial
long_secuencia = 10  # Longitud de la secuencia de nucleótidos, ajustado para coincidir con la secuencia objetivo
tamano_torneo = 10  # Tamaño del torneo
tasa_seleccion = 0.5  # Tasa de selección
tasa_cruzamiento = 0.8
tasa_mutacion = 0.5
tasa_gaps = 0.2  # Por ejemplo, una tasa de agregar gaps del 20%
secuencia_objetivo = 'AGTCAGATCG'

# ------------------ 1.- POBLACIÓN GENERADA --------------------
def generar_poblacion_inicial(num_individuos, longitud_secuencia):
    poblacion = []
    for _ in range(num_individuos):
        individuo = ''.join(random.choice('ACGT') for _ in range(longitud_secuencia))
        poblacion.append(individuo)
    return poblacion

# ------------------ 2.- EVALUACIÓN DE INDIVIDUOS --------------------
def evaluar_individuo(individuo, secuencia_objetivo):
    similitud = calcular_similitud_secuencia(individuo, secuencia_objetivo)
    print(f"Similitud del individuo {individuo} con la secuencia objetivo: {similitud}")
    
    num_espacios = individuo.count('-')
    return similitud, 0, len(individuo), num_espacios

# Función para evaluar la población y calcular el promedio de similitud
def evaluar_poblacion(poblacion, secuencia_objetivo):
    similitudes = [calcular_similitud_secuencia(individuo, secuencia_objetivo) for individuo in poblacion]
    promedio_similitud = sum(similitudes) / len(similitudes)
    return promedio_similitud


# ------------------ FUNCIONES DE APTITUD ------------------
def calcular_similitud_secuencia(individuo, secuencia_objetivo):
    num_coincidencias = sum(a == b for a, b in zip(individuo, secuencia_objetivo))
    return num_coincidencias / len(secuencia_objetivo)

def seleccion_mejor_mitad(poblacion, secuencia_objetivo):
    evaluaciones = [(individuo, calcular_similitud_secuencia(individuo, secuencia_objetivo)) for individuo in poblacion]
    evaluaciones.sort(key=lambda x: x[1], reverse=True)
    seleccionados = [evaluacion[0] for evaluacion in evaluaciones[:len(evaluaciones) // 2]]
    return seleccionados

# ------------------ OPERACIONES GENÉTICAS ------------------
def cruzamiento(individuo1, individuo2):
    punto = random.randint(1, len(individuo1) - 1)
    hijo1 = individuo1[:punto] + individuo2[punto:]
    hijo2 = individuo2[:punto] + individuo1[punto:]
    return hijo1, hijo2

def mutacion(individuo, tasa_mutacion, tasa_gaps):
    individuo_mutado = ''
    for char in individuo:
        if random.random() < tasa_mutacion:
            # Mutar el carácter actual
            individuo_mutado += random.choice('ACGT')
        else:
            # No mutar el carácter actual
            individuo_mutado += char
    return individuo_mutado

# ------------------ EJEMPLO DE EJECUCIÓN ------------------
poblacion_inicial = generar_poblacion_inicial(numero_individuos, long_secuencia)
print("\nPoblación Inicial:")
for individuo in poblacion_inicial:
    print(individuo)

# Evaluar población inicial (simplificado para demostración)
print("\nEvaluación de Individuos:\n")
for individuo in poblacion_inicial:
    aptitudes = evaluar_individuo(individuo, secuencia_objetivo)

# Evaluación de la población inicial
promedio_similitud = evaluar_poblacion(poblacion_inicial, secuencia_objetivo)
print(f"Promedio de similitud con la secuencia objetivo: {promedio_similitud:.3f}")
print('\nNueva Población Seleccionada (Mejor Mitad): \n')

num_generaciones = 1  # Número de generaciones

# Bucle para iterar hasta que se encuentre la secuencia objetivo
while promedio_similitud < 1.0:
    print(f"\nGeneración {num_generaciones}")
    # Seleccionar la mejor mitad de la población
    nueva_poblacion = seleccion_mejor_mitad(poblacion_inicial, secuencia_objetivo)
    print("\nNueva Población Seleccionada:")
    for individuo in nueva_poblacion:
        print(individuo)

    # Evaluar población después de la selección
    promedio_similitud = evaluar_poblacion(nueva_poblacion, secuencia_objetivo)
    print(f"Promedio de similitud con la secuencia objetivo: {promedio_similitud:.3f}")

    if promedio_similitud == 1.0:
        break
    else:
        # Verificar si todos los padres son iguales entre sí
        if all(padre == nueva_poblacion[0] for padre in nueva_poblacion):
            print("Todos los padres son iguales. Terminando el bucle.")
            break
        
        # Cruzamiento
        # Elegir todos los individuos de la mejor mitad como padres
        padres = nueva_poblacion

        # Eliminar padres duplicados para evitar repeticiones al elegir padres para cruzamiento
        padres = list(set(padres))
        print("\nPadres para cruzamiento:", padres)

        # Contador para controlar cuántos individuos se han agregado a la población
        individuos_agregados = 0

        # Copia fija de la población original para iterar sobre ella
        for padre in nueva_poblacion[:]:  
            # Lista para almacenar los nuevos hijos generados por cada padre
            nuevos_hijos = []
            # Generar dos hijos por cada padre
            for _ in range(2):
                # Elegir otro padre al azar (diferente al padre actual)
                otro_padre = random.choice(nueva_poblacion)
                while otro_padre == padre:
                    otro_padre = random.choice(nueva_poblacion)
                # Cruzamiento para obtener dos nuevos individuos
                hijo1, hijo2 = cruzamiento(padre, otro_padre)
                # Mutar los nuevos individuos
                hijo1 = mutacion(hijo1, tasa_mutacion, tasa_gaps)
                hijo2 = mutacion(hijo2, tasa_mutacion, tasa_gaps)
                # Agregar los hijos a la lista de nuevos individuos
                nuevos_hijos.extend([hijo1, hijo2])
            # Calcular cuántos nuevos individuos se agregarán a la población
            num_nuevos = min(20 - len(nueva_poblacion), len(nuevos_hijos))
            # Agregar los nuevos hijos generados por este padre a la población
            nueva_poblacion.extend(nuevos_hijos[:num_nuevos])
            # Actualizar el contador de individuos agregados
            individuos_agregados += num_nuevos
            # Detener la iteración si se han agregado suficientes individuos
            if individuos_agregados >= 20:
                break

        # Imprimir la población resultante
        print("Población después de generar hijos:")
        for individuo in nueva_poblacion:
            print(individuo)
        
    # Evaluar población después de la selección
    promedio_similitud = evaluar_poblacion(nueva_poblacion, secuencia_objetivo)
    print(f"Promedio de similitud con la secuencia objetivo: {promedio_similitud:.3f}")

    # Actualizar la población inicial con la nueva población
    poblacion_inicial = nueva_poblacion
    # Incrementar el contador de generaciones
    num_generaciones += 1
