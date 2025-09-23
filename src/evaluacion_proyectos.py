"""
Módulo para evaluación de proyectos estudiantiles
Autor: Andres
Fecha: Septiembre 2025
"""

def calcular_puntaje_equipo(datos_equipo):
    """
    Calcula el  de un equipo según la fórmula establecida.
    
    Args:
        datos_equipo (dict): Diccionario con 'innovacion', 'presentacion', 'errores'
    
    Returns:
        int: Puntaje total del equipo
    """
    innovacion = datos_equipo['innovacion'] * 3
    presentacion = datos_equipo['presentacion'] * 1
    penalizacion = -1 if datos_equipo['errores'] else 0
    
    return innovacion + presentacion + penalizacion

def procesar_ronda(ronda_datos, acumulado):
    """
    Procesa una ronda completa de evaluaciones.
    
    Args:
        ronda_datos (dict): Datos de todos los equipos en la ronda
        acumulado (dict): Diccionario acumulador de resultados
    
    Returns:
        tuple: (nombre_mejor_equipo, puntaje_mejor_equipo)
    """
    puntajes_ronda = {}
    
    # Usar map() para calcular todos los puntajes (cumple requisito)
    equipos = list(ronda_datos.keys())
    datos = list(ronda_datos.values())
    puntajes = list(map(calcular_puntaje_equipo, datos))
    
    # Combinar equipos con sus puntajes
    for equipo, puntaje in zip(equipos, puntajes):
        puntajes_ronda[equipo] = puntaje
        
        # Inicializar acumulado si no existe el equipo
        if equipo not in acumulado:
            acumulado[equipo] = {
                'innovacion_total': 0,
                'presentacion_total': 0,
                'errores_total': 0,
                'veces_mejor': 0,
                'puntos_total': 0
            }
        
        # Actualizar totales acumulados
        acumulado[equipo]['innovacion_total'] += ronda_datos[equipo]['innovacion']
        acumulado[equipo]['presentacion_total'] += ronda_datos[equipo]['presentacion']
        acumulado[equipo]['errores_total'] += int(ronda_datos[equipo]['errores'])
        acumulado[equipo]['puntos_total'] += puntaje
    
    # Encontrar el mejor equipo de la ronda
    mejor_equipo = max(puntajes_ronda, key=puntajes_ronda.get)
    acumulado[mejor_equipo]['veces_mejor'] += 1
    
    return mejor_equipo, max(puntajes_ronda.values())

def mostrar_tabla(acumulado, numero_ronda):
    """
    Muestra tabla formateada de resultados ordenada por puntos totales.
    
    Args:
        acumulado (dict): Datos acumulados de todos los equipos
        numero_ronda (int/str): Número de ronda o "Final"
    """
    print(f"\nRanking Actualizado - Ronda {numero_ronda}")
    print("-" * 80)
    print(f"{'Equipo':<10} {'Innovación':<12} {'Presentación':<14} {'Errores':<8} {'Mejores':<8} {'Puntos Total':<12}")
    print("-" * 80)
    
    # Ordenar equipos por puntos totales (descendente)
    equipos_ordenados = sorted(acumulado.items(), 
                              key=lambda x: x[1]['puntos_total'], 
                              reverse=True)
    
    for equipo, datos in equipos_ordenados:
        print(f"{equipo:<10} {datos['innovacion_total']:<12} {datos['presentacion_total']:<14} "
              f"{datos['errores_total']:<8} {datos['veces_mejor']:<8} {datos['puntos_total']:<12}")

def ejecutar_evaluacion(evaluaciones):
    """
    Función principal que ejecuta todo el sistema de evaluación.
    
    Args:
        evaluaciones (list): Lista de diccionarios con datos de cada ronda
    
    Returns:
        dict: Resultados finales acumulados
    """
    print("Resultados de la Feria de Ciencias - Sistema de Evaluación")
    print("=" * 60)
    
    acumulado = {}
    
    # Procesar cada ronda
    for i, ronda in enumerate(evaluaciones, 1):
        print(f"\n=== RONDA {i} ===")
        
        mejor_equipo, mejor_puntaje = procesar_ronda(ronda, acumulado)
        print(f"Mejor Equipo de la Ronda: {mejor_equipo} ({mejor_puntaje} puntos)")
        
        mostrar_tabla(acumulado, i)
    
    # Mostrar resultados finales
    print("\n" + "="*60)
    print("RESULTADOS FINALES")
    print("="*60)
    
    # Encontrar ganadores (equipos con máximo puntaje)
    max_puntos = max(datos['puntos_total'] for datos in acumulado.values())
    ganadores = [equipo for equipo, datos in acumulado.items() 
                if datos['puntos_total'] == max_puntos]
    
    print(f"Equipos Ganadores: {', '.join(ganadores)} ({max_puntos} puntos)")
    
    mostrar_tabla(acumulado, "Final")
    
    return acumulado

# Para testing directo del módulo
if __name__ == "__main__":
    # Datos de ejemplo para pruebas
    evaluaciones_test = [
        {
            'EquipoA': {'innovacion': 2, 'presentacion': 1, 'errores': True},
            'EquipoB': {'innovacion': 1, 'presentacion': 0, 'errores': False},
        }
    ]
    ejecutar_evaluacion(evaluaciones_test)
