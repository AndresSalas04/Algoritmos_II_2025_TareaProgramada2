"""
prueba.py

Programa principal para resolver problemas algorítmicos.

Tarea de Estructuras de Datos y Análisis de Algoritmos.

Programado por:
    Braulio José Solano Rojas
"""

import random
from typing import List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.padding import Padding

from tiempo import MedidorTiempo
from asign1a1 import ProblemaAsigna1a1, SolucionAsigna1a1
from mochila import ProblemaMochila, SolucionMochila
from vendedor import ProblemaVendedor, SolucionVendedor
from recursos import DistribucionRecursos, SolucionDistribucion


console = Console()


def crear_marco(titulo: str = "") -> Panel:
    """
    Crea un marco decorativo.
    
    Args:
        titulo: Título opcional para el marco
        
    Returns:
        Panel de Rich configurado
    """
    return Panel(
        "",
        title=f"[bold white]{titulo}[/bold white]" if titulo else "",
        border_style="white",
        box=box.DOUBLE,
        expand=True,
        height=24
    )


def mostrar_menu_principal():
    """Muestra el menú principal del programa."""
    console.clear()
    
    contenido = Text()
    contenido.append("\n" * 3)
    contenido.append(" " * 29 + "Resolución de problemas\n\n", style="bold white")
    contenido.append(" " * 21 + "[", style="white")
    contenido.append("1", style="bright_white")
    contenido.append("] Problema de asignación 1 a 1\n", style="white")
    contenido.append(" " * 21 + "[", style="white")
    contenido.append("2", style="bright_white")
    contenido.append("] Problema de distribución de un recurso\n", style="white")
    contenido.append(" " * 21 + "[", style="white")
    contenido.append("3", style="bright_white")
    contenido.append("] Problema de la mochila\n", style="white")
    contenido.append(" " * 21 + "[", style="white")
    contenido.append("4", style="bright_white")
    contenido.append("] Problema del vendedor\n", style="white")
    contenido.append(" " * 21 + "[", style="white")
    contenido.append("5", style="bright_white")
    contenido.append("] Salir\n", style="white")
    
    panel = Panel(
        contenido,
        border_style="white",
        box=box.DOUBLE,
        expand=False,
        width=80
    )
    
    console.print(panel)


def mostrar_menu_metodos():
    """Muestra el menú de métodos de resolución."""
    console.clear()
    
    contenido = Text()
    contenido.append("\n" * 3)
    contenido.append(" " * 30 + "Métodos de resolución\n\n", style="bold white")
    contenido.append(" " * 15 + "[", style="white")
    contenido.append("1", style="bright_white")
    contenido.append("] Búsqueda Greedy\n", style="white")
    contenido.append(" " * 15 + "[", style="white")
    contenido.append("2", style="bright_white")
    contenido.append("] Búsqueda Exhaustiva Pura\n", style="white")
    contenido.append(" " * 15 + "[", style="white")
    contenido.append("3", style="bright_white")
    contenido.append("] Búsqueda Exhaustiva con Ramificación y Acotamiento\n", style="white")
    contenido.append(" " * 15 + "[", style="white")
    contenido.append("4", style="bright_white")
    contenido.append("] Regresar al menú principal\n", style="white")
    
    panel = Panel(
        contenido,
        border_style="white",
        box=box.DOUBLE,
        expand=False,
        width=80
    )
    
    console.print(panel)


def problema_asignacion_1a1():
    """Resuelve el problema de asignación 1 a 1."""
    console.clear()
    
    # Solicitar tamaño
    console.print(Panel(
        "Digite el número de ítemes (menor o igual a 100) a los cuales se\n"
        "les asignará otro ítem:",
        border_style="white",
        box=box.DOUBLE
    ))
    
    while True:
        tamano = IntPrompt.ask("Tamaño")
        if tamano <= 100:
            break
        console.print("[red]El tamaño debe ser menor o igual a 100[/red]")
    
    # Determinar si generar aleatoriamente
    if tamano > 10:
        aleatoria = True
    else:
        aleatoria = Confirm.ask("¿Desea generar las ganancias aleatoriamente?")
    
    # Crear matriz de ganancias
    matriz_ganancias = [[0] * (tamano + 1) for _ in range(tamano + 1)]
    
    if aleatoria:
        console.print("\n[cyan]Generando matriz aleatoria...[/cyan]\n")
        
        if tamano <= 11:
            # Mostrar la matriz si es pequeña
            tabla = Table(show_header=True, header_style="bold white",
                         box=box.SIMPLE)
            tabla.add_column("i\\j", style="white")
            for j in range(1, tamano + 1):
                tabla.add_column(str(j), style="bright_white")
            
            for i in range(1, tamano + 1):
                fila = [str(i)]
                for j in range(1, tamano + 1):
                    matriz_ganancias[i][j] = random.randint(0, 299)
                    fila.append(str(matriz_ganancias[i][j]))
                tabla.add_row(*fila)
            
            console.print(tabla)
        else:
            for i in range(1, tamano + 1):
                for j in range(1, tamano + 1):
                    matriz_ganancias[i][j] = random.randint(0, 299)
    else:
        console.print("\n[cyan]Digite la ganancia de asignar el ítem i al ítem j:[/cyan]\n")
        for i in range(1, tamano + 1):
            for j in range(1, tamano + 1):
                valor = IntPrompt.ask(f"Ganancia[{i}][{j}]")
                matriz_ganancias[i][j] = valor
    
    Prompt.ask("\nPulse ENTER para continuar")
    
    # Crear problema
    problema = ProblemaAsigna1a1(matriz_ganancias, tamano)
    
    # Menú de métodos
    while True:
        mostrar_menu_metodos()
        opcion = Prompt.ask("Digite una opción", choices=["1", "2", "3", "4"])
        
        if opcion == "4":
            break
        
        timer = MedidorTiempo()
        solucion = None
        
        if opcion == "1":
            timer.cargar_tiempo()
            solucion = problema.busqueda_greedy()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "2":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_pura()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "3":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_ra()
            tiempo = timer.intervalo_tiempo()
        
        if solucion:
            imprimir_solucion_asignacion(solucion, tiempo, tamano)


def imprimir_solucion_asignacion(solucion: SolucionAsigna1a1, 
                                 tiempo: dict, tamano: int):
    """Imprime la solución del problema de asignación."""
    console.clear()
    
    # Construir texto de la solución
    texto_solucion = "La solución es: "
    asignaciones = []
    for i in range(1, tamano + 1):
        asignaciones.append(f"I{i}→J{solucion.asignado[i]}")
    texto_solucion += ", ".join(asignaciones) + "."
    
    contenido = f"{texto_solucion}\n\n"
    contenido += f"Con una ganancia de {solucion.ganancia}.\n\n"
    contenido += f"El tiempo transcurrido para encontrar la solución fue: "
    contenido += f"{tiempo['horas']:02d}:{tiempo['minutos']:02d}:{tiempo['segundos']:02d},{tiempo['centesimas']:02d}."
    
    if solucion.soluciones_factibles > 0:
        contenido += f"\n\nEl número de soluciones factibles fue {solucion.soluciones_factibles}."
    
    panel = Panel(
        contenido,
        title="[bold white]Resultado[/bold white]",
        border_style="white",
        box=box.DOUBLE
    )
    
    console.print(panel)
    Prompt.ask("\nPulse ENTER para continuar")


def problema_distribucion():
    """Resuelve el problema de distribución de recursos."""
    console.clear()
    
    console.print(Panel(
        "Digite el número de recursos disponibles:",
        border_style="white",
        box=box.DOUBLE
    ))
    recursos = IntPrompt.ask("Recursos")
    
    console.print(Panel(
        "Digite el número de ítemes a los que asignar recursos:",
        border_style="white",
        box=box.DOUBLE
    ))
    itemes = IntPrompt.ask("Ítemes")
    
    # Determinar si generar aleatoriamente
    if recursos > 10 or itemes > 10:
        aleatoria = True
    else:
        aleatoria = Confirm.ask("¿Desea generar las ganancias aleatoriamente?")
    
    # Crear matriz de ganancias
    matriz = [[0] * (itemes + 1) for _ in range(recursos + 1)]
    
    if aleatoria:
        console.print("\n[cyan]Generando matriz aleatoria...[/cyan]\n")
        for i in range(recursos + 1):
            for j in range(1, itemes + 1):
                matriz[i][j] = random.randint(0, 299)
    else:
        console.print("\n[cyan]Digite la ganancia de asignar i recursos al ítem j:[/cyan]\n")
        for i in range(recursos + 1):
            for j in range(1, itemes + 1):
                valor = IntPrompt.ask(f"Ganancia[{i}][{j}]")
                matriz[i][j] = valor
    
    Prompt.ask("\nPulse ENTER para continuar")
    
    # Crear problema
    problema = DistribucionRecursos(matriz, recursos, itemes)
    
    # Menú de métodos
    while True:
        mostrar_menu_metodos()
        opcion = Prompt.ask("Digite una opción", choices=["1", "2", "3", "4"])
        
        if opcion == "4":
            break
        
        timer = MedidorTiempo()
        solucion = None
        
        if opcion == "1":
            timer.cargar_tiempo()
            solucion = problema.busqueda_greedy()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "2":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_pura()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "3":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_ra()
            tiempo = timer.intervalo_tiempo()
        
        if solucion:
            imprimir_solucion_distribucion(solucion, tiempo, itemes)


def imprimir_solucion_distribucion(solucion: SolucionDistribucion,
                                   tiempo: dict, itemes: int):
    """Imprime la solución del problema de distribución."""
    console.clear()
    
    # Construir texto de la solución
    texto_solucion = "La distribución es: "
    distribuciones = []
    for i in range(1, itemes + 1):
        distribuciones.append(f"Ítem{i}: {solucion.distribucion[i]} recursos")
    texto_solucion += ", ".join(distribuciones) + "."
    
    contenido = f"{texto_solucion}\n\n"
    contenido += f"Con una ganancia de {solucion.ganancia}.\n\n"
    contenido += f"El tiempo transcurrido para encontrar la solución fue: "
    contenido += f"{tiempo['horas']:02d}:{tiempo['minutos']:02d}:{tiempo['segundos']:02d},{tiempo['centesimas']:02d}."
    
    if solucion.soluciones_factibles > 0:
        contenido += f"\n\nEl número de soluciones factibles fue {solucion.soluciones_factibles}."
    
    panel = Panel(
        contenido,
        title="[bold white]Resultado[/bold white]",
        border_style="white",
        box=box.DOUBLE
    )
    
    console.print(panel)
    Prompt.ask("\nPulse ENTER para continuar")


def problema_mochila():
    """Resuelve el problema de la mochila."""
    console.clear()
    
    console.print(Panel(
        "Digite el número de ítemes disponibles:",
        border_style="white",
        box=box.DOUBLE
    ))
    
    while True:
        tamano = IntPrompt.ask("Tamaño")
        if tamano <= 100:
            break
        console.print("[red]El tamaño debe ser menor o igual a 100[/red]")
    
    console.print(Panel(
        "Digite la capacidad de la mochila:",
        border_style="white",
        box=box.DOUBLE
    ))
    capacidad = IntPrompt.ask("Capacidad")
    
    # Determinar si generar aleatoriamente
    if tamano > 10:
        aleatoria = True
    else:
        aleatoria = Confirm.ask("¿Desea generar pesos y beneficios aleatoriamente?")
    
    # Crear arrays de peso y beneficio
    peso = [0] * tamano
    beneficio = [0] * tamano
    
    if aleatoria:
        console.print("\n[cyan]Generando datos aleatorios...[/cyan]\n")
        
        if tamano <= 11:
            tabla = Table(show_header=True, header_style="bold white",
                         box=box.SIMPLE)
            tabla.add_column("Ítem", style="white")
            tabla.add_column("Peso", style="bright_white")
            tabla.add_column("Beneficio", style="bright_white")
            
            for i in range(tamano):
                peso[i] = random.randint(1, 50)
                beneficio[i] = random.randint(1, 299)
                tabla.add_row(str(i + 1), str(peso[i]), str(beneficio[i]))
            
            console.print(tabla)
        else:
            for i in range(tamano):
                peso[i] = random.randint(1, 50)
                beneficio[i] = random.randint(1, 299)
    else:
        console.print("\n[cyan]Digite el peso y beneficio de cada ítem:[/cyan]\n")
        for i in range(tamano):
            peso[i] = IntPrompt.ask(f"Peso del ítem {i + 1}")
            beneficio[i] = IntPrompt.ask(f"Beneficio del ítem {i + 1}")
    
    Prompt.ask("\nPulse ENTER para continuar")
    
    # Crear problema
    problema = ProblemaMochila(peso, beneficio, capacidad, tamano)
    
    # Menú de métodos
    while True:
        mostrar_menu_metodos()
        opcion = Prompt.ask("Digite una opción", choices=["1", "2", "3", "4"])
        
        if opcion == "4":
            break
        
        timer = MedidorTiempo()
        solucion = None
        
        if opcion == "1":
            timer.cargar_tiempo()
            solucion = problema.busqueda_greedy()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "2":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_pura()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "3":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_ra()
            tiempo = timer.intervalo_tiempo()
        
        if solucion:
            imprimir_solucion_mochila(solucion, tiempo, tamano, peso, beneficio)


def imprimir_solucion_mochila(solucion: SolucionMochila, tiempo: dict,
                              tamano: int, peso: List[int], beneficio: List[int]):
    """Imprime la solución del problema de la mochila."""
    console.clear()
    
    # Construir texto de la solución
    items_seleccionados = []
    peso_total = 0
    for i in range(1, tamano + 1):
        if solucion.mochila[i]:
            items_seleccionados.append(str(i))
            peso_total += peso[i - 1]
    
    contenido = f"Los ítemes seleccionados son: {', '.join(items_seleccionados) if items_seleccionados else 'Ninguno'}.\n\n"
    contenido += f"Con un beneficio total de {solucion.beneficio}.\n"
    contenido += f"Peso total: {peso_total}.\n\n"
    contenido += f"El tiempo transcurrido para encontrar la solución fue: "
    contenido += f"{tiempo['horas']:02d}:{tiempo['minutos']:02d}:{tiempo['segundos']:02d},{tiempo['centesimas']:02d}."
    
    if solucion.soluciones_factibles > 0:
        contenido += f"\n\nEl número de soluciones factibles fue {solucion.soluciones_factibles}."
    
    panel = Panel(
        contenido,
        title="[bold white]Resultado[/bold white]",
        border_style="white",
        box=box.DOUBLE
    )
    
    console.print(panel)
    Prompt.ask("\nPulse ENTER para continuar")


def problema_vendedor():
    """Resuelve el problema del vendedor viajero."""
    console.clear()
    
    console.print(Panel(
        "Digite el número de ciudades (menor o igual a 100) que se van a visitar:",
        border_style="white",
        box=box.DOUBLE
    ))
    
    while True:
        tamano = IntPrompt.ask("Tamaño")
        if tamano <= 100:
            break
        console.print("[red]El tamaño debe ser menor o igual a 100[/red]")
    
    # Determinar si generar aleatoriamente
    if tamano > 10:
        aleatoria = True
    else:
        aleatoria = Confirm.ask("¿Desea generar las distancias entre ciudades aleatoriamente?")
    
    # Crear matriz de adyacencia
    matriz = [[0] * (tamano + 1) for _ in range(tamano + 1)]
    
    # Diagonal en cero
    for i in range(1, tamano + 1):
        matriz[i][i] = 0
    
    if aleatoria:
        console.print("\n[cyan]Generando matriz aleatoria...[/cyan]\n")
        
        if tamano <= 11:
            tabla = Table(show_header=True, header_style="bold white",
                         box=box.SIMPLE)
            tabla.add_column("", style="white")
            for j in range(1, tamano + 1):
                tabla.add_column(chr(j + 96), style="bright_white")
            
            for i in range(1, tamano + 1):
                fila = [chr(i + 96)]
                for j in range(1, tamano + 1):
                    if i == j:
                        fila.append("0")
                    elif i < j:
                        matriz[i][j] = random.randint(1, 299)
                        matriz[j][i] = matriz[i][j]
                        fila.append(str(matriz[i][j]))
                    else:
                        fila.append(str(matriz[i][j]))
                tabla.add_row(*fila)
            
            console.print(tabla)
        else:
            for i in range(1, tamano + 1):
                for j in range(i + 1, tamano + 1):
                    matriz[i][j] = random.randint(1, 299)
                    matriz[j][i] = matriz[i][j]
    else:
        console.print("\n[cyan]Digite la distancia de la ciudad i a la ciudad j:[/cyan]\n")
        for i in range(1, tamano + 1):
            for j in range(i + 1, tamano + 1):
                valor = IntPrompt.ask(f"Distancia[{chr(i + 96)}][{chr(j + 96)}]")
                matriz[i][j] = valor
                matriz[j][i] = valor
    
    Prompt.ask("\nPulse ENTER para continuar")
    
    # Crear problema
    problema = ProblemaVendedor(matriz, tamano)
    
    # Menú de métodos
    while True:
        mostrar_menu_metodos()
        opcion = Prompt.ask("Digite una opción", choices=["1", "2", "3", "4"])
        
        if opcion == "4":
            break
        
        timer = MedidorTiempo()
        solucion = None
        
        if opcion == "1":
            timer.cargar_tiempo()
            solucion = problema.busqueda_greedy()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "2":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_pura()
            tiempo = timer.intervalo_tiempo()
        elif opcion == "3":
            timer.cargar_tiempo()
            solucion = problema.busqueda_exhaustiva_ra()
            tiempo = timer.intervalo_tiempo()
        
        if solucion:
            imprimir_solucion_vendedor(solucion, tiempo, tamano)


def imprimir_solucion_vendedor(solucion: SolucionVendedor, tiempo: dict, tamano: int):
    """Imprime la solución del problema del vendedor."""
    console.clear()
    
    # Construir texto del camino
    camino = []
    for i in range(1, tamano + 1):
        if solucion.camino[i]:
            camino.append(solucion.camino[i])
    camino.append('a')  # Regresar al inicio
    
    contenido = f"El camino del vendedor es: {'-'.join(camino)}.\n\n"
    contenido += f"Con un costo de {solucion.costo}.\n\n"
    contenido += f"El tiempo transcurrido para encontrar la solución fue: "
    contenido += f"{tiempo['horas']:02d}:{tiempo['minutos']:02d}:{tiempo['segundos']:02d},{tiempo['centesimas']:02d}."
    
    if solucion.soluciones_factibles > 0:
        contenido += f"\n\nEl número de soluciones factibles fue {solucion.soluciones_factibles}."
    
    panel = Panel(
        contenido,
        title="[bold white]Resultado[/bold white]",
        border_style="white",
        box=box.DOUBLE
    )
    
    console.print(panel)
    Prompt.ask("\nPulse ENTER para continuar")


def main():
    """Función principal del programa."""
    random.seed()
    
    while True:
        mostrar_menu_principal()
        opcion = Prompt.ask("Digite una opción", choices=["1", "2", "3", "4", "5"])
        
        if opcion == "1":
            problema_asignacion_1a1()
        elif opcion == "2":
            problema_distribucion()
        elif opcion == "3":
            problema_mochila()
        elif opcion == "4":
            problema_vendedor()
        elif opcion == "5":
            console.clear()
            console.print("[bold green]¡Hasta luego![/bold green]")
            break


if __name__ == "__main__":
    main()
