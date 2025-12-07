"""
demo.py

Script de demostración para probar los algoritmos sin interfaz interactiva.
"""

from asign1a1 import ProblemaAsigna1a1
from mochila import ProblemaMochila
from vendedor import ProblemaVendedor
from recursos import DistribucionRecursos
from tiempo import MedidorTiempo
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def demo_asignacion():
    """Demostración del problema de asignación 1 a 1."""
    console.print("\n[bold cyan]═══ PROBLEMA DE ASIGNACIÓN 1 A 1 ═══[/bold cyan]\n")
    
    # Matriz de ejemplo 4x4
    matriz = [
        [0, 0, 0, 0, 0],  # Índice 0 no se usa
        [0, 50, 70, 30, 60],  # Ítem 1
        [0, 80, 40, 90, 50],  # Ítem 2
        [0, 60, 30, 70, 80],  # Ítem 3
        [0, 70, 80, 60, 40]   # Ítem 4
    ]
    
    # Mostrar matriz
    tabla = Table(title="Matriz de Ganancias", box=box.ROUNDED)
    tabla.add_column("i\\j", style="cyan")
    for j in range(1, 5):
        tabla.add_column(str(j), style="yellow")
    
    for i in range(1, 5):
        fila = [str(i)]
        for j in range(1, 5):
            fila.append(str(matriz[i][j]))
        tabla.add_row(*fila)
    
    console.print(tabla)
    
    problema = ProblemaAsigna1a1(matriz, 4)
    
    # Probar los tres métodos
    console.print("\n[bold yellow]1. Búsqueda Greedy:[/bold yellow]")
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    solucion = problema.busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    
    asignaciones = [f"I{i}→J{solucion.asignado[i]}" for i in range(1, 5)]
    console.print(f"   Solución: {', '.join(asignaciones)}")
    console.print(f"   Ganancia: [green]{solucion.ganancia}[/green]")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")
    
    console.print("\n[bold yellow]2. Búsqueda Exhaustiva Pura:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    
    asignaciones = [f"I{i}→J{solucion.asignado[i]}" for i in range(1, 5)]
    console.print(f"   Solución: {', '.join(asignaciones)}")
    console.print(f"   Ganancia: [green]{solucion.ganancia}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")
    
    console.print("\n[bold yellow]3. Ramificación y Acotamiento:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    
    asignaciones = [f"I{i}→J{solucion.asignado[i]}" for i in range(1, 5)]
    console.print(f"   Solución: {', '.join(asignaciones)}")
    console.print(f"   Ganancia: [green]{solucion.ganancia}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")


def demo_mochila():
    """Demostración del problema de la mochila."""
    console.print("\n\n[bold cyan]═══ PROBLEMA DE LA MOCHILA ═══[/bold cyan]\n")
    
    peso = [10, 20, 30, 40]
    beneficio = [60, 100, 120, 80]
    capacidad = 50
    
    # Mostrar datos
    tabla = Table(title="Ítems Disponibles", box=box.ROUNDED)
    tabla.add_column("Ítem", style="cyan")
    tabla.add_column("Peso", style="yellow")
    tabla.add_column("Beneficio", style="green")
    tabla.add_column("B/P", style="magenta")
    
    for i in range(len(peso)):
        tabla.add_row(
            str(i + 1),
            str(peso[i]),
            str(beneficio[i]),
            f"{beneficio[i]/peso[i]:.2f}"
        )
    
    console.print(tabla)
    console.print(f"\n[bold]Capacidad de la mochila:[/bold] {capacidad}")
    
    problema = ProblemaMochila(peso, beneficio, capacidad, len(peso))
    
    # Probar métodos
    console.print("\n[bold yellow]1. Búsqueda Greedy:[/bold yellow]")
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    solucion = problema.busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    
    seleccionados = [str(i) for i in range(1, len(peso) + 1) if solucion.mochila[i]]
    console.print(f"   Ítems seleccionados: {', '.join(seleccionados)}")
    console.print(f"   Beneficio: [green]{solucion.beneficio}[/green]")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")
    
    console.print("\n[bold yellow]2. Búsqueda Exhaustiva Pura:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    
    seleccionados = [str(i) for i in range(1, len(peso) + 1) if solucion.mochila[i]]
    console.print(f"   Ítems seleccionados: {', '.join(seleccionados)}")
    console.print(f"   Beneficio: [green]{solucion.beneficio}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")

    console.print("\n[bold yellow]3. Ramificación y Acotamiento:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()

    seleccionados = [str(i) for i in range(1, len(peso) + 1) if solucion.mochila[i]]
    console.print(f"   Ítems seleccionados: {', '.join(seleccionados)}")
    console.print(f"   Beneficio: [green]{solucion.beneficio}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")

def demo_vendedor():
    """Demostración del problema del vendedor viajero."""
    console.print("\n\n[bold cyan]═══ PROBLEMA DEL VENDEDOR VIAJERO ═══[/bold cyan]\n")
    
    # Matriz de distancias 5x5
    matriz = [
        [0, 0, 0, 0, 0, 0],  # Índice 0 no se usa
        [0, 0, 10, 15, 20, 25],  # Ciudad a
        [0, 10, 0, 35, 25, 30],  # Ciudad b
        [0, 15, 35, 0, 30, 20],  # Ciudad c
        [0, 20, 25, 30, 0, 15],  # Ciudad d
        [0, 25, 30, 20, 15, 0]   # Ciudad e
    ]
    
    # Mostrar matriz
    tabla = Table(title="Matriz de Distancias", box=box.ROUNDED)
    tabla.add_column("", style="cyan")
    for j in range(1, 6):
        tabla.add_column(chr(j + 96), style="yellow")
    
    for i in range(1, 6):
        fila = [chr(i + 96)]
        for j in range(1, 6):
            fila.append(str(matriz[i][j]))
        tabla.add_row(*fila)
    
    console.print(tabla)
    
    problema = ProblemaVendedor(matriz, 5)
    
    # Probar métodos
    console.print("\n[bold yellow]1. Búsqueda Greedy:[/bold yellow]")
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    solucion = problema.busqueda_greedy()
    tiempo = timer.intervalo_tiempo()

    camino = [chr(solucion.camino[i] + 96) for i in range(1, 6)]
    camino.append('a')  # regresar a la ciudad inicial
    console.print(f"   Camino: {'-'.join(camino)}")
    console.print(f"   Costo: [green]{solucion.costo}[/green]")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")
    
    console.print("\n[bold yellow]2. Búsqueda Exhaustiva Pura:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    
    camino = [chr(solucion.camino[i] + 96) for i in range(1, 6)]
    camino.append('a')  # regresar a la ciudad inicial
    console.print(f"   Camino: {'-'.join(camino)}")
    console.print(f"   Costo: [green]{solucion.costo}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")

    console.print("\n[bold yellow]3. Ramificación y Acotamiento:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    
    camino = [chr(solucion.camino[i] + 96) for i in range(1, 6)]
    camino.append('a')
    console.print(f"   Camino: {'-'.join(camino)}")
    console.print(f"   Costo: [green]{solucion.costo}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")

def demo_recursos():
    """Demostración del problema de distribución de recursos."""
    console.print("\n\n[bold cyan]═══ PROBLEMA DE DISTRIBUCIÓN DE RECURSOS ═══[/bold cyan]\n")
    
    # Matriz donde matriz[i][j] = ganancia de asignar i recursos al ítem j
    matriz = [
        [0, 0, 0, 0],       # 0 recursos
        [0, 40, 30, 50],    # 1 recurso
        [0, 70, 80, 90],    # 2 recursos
        [0, 100, 110, 120], # 3 recursos
        [0, 120, 130, 140]  # 4 recursos
    ]
    
    recursos_totales = 4
    itemes = 3
    
    # Mostrar matriz
    tabla = Table(title="Matriz de Ganancias", box=box.ROUNDED)
    tabla.add_column("Recursos\\Ítem", style="cyan")
    for j in range(1, itemes + 1):
        tabla.add_column(str(j), style="yellow")
    
    for i in range(recursos_totales + 1):
        fila = [str(i)]
        for j in range(1, itemes + 1):
            fila.append(str(matriz[i][j]))
        tabla.add_row(*fila)
    
    console.print(tabla)
    console.print(f"\n[bold]Recursos totales disponibles:[/bold] {recursos_totales}")
    
    problema = DistribucionRecursos(matriz, recursos_totales, itemes)
    
    # Probar métodos
    console.print("\n[bold yellow]1. Búsqueda Greedy:[/bold yellow]")
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    solucion = problema.busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    
    distribuciones = [f"Ítem{i}: {solucion.distribucion[i]}" for i in range(1, itemes + 1)]
    console.print(f"   Distribución: {', '.join(distribuciones)}")
    console.print(f"   Ganancia: [green]{solucion.ganancia}[/green]")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")
    
    console.print("\n[bold yellow]2. Búsqueda Exhaustiva Pura:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    
    distribuciones = [f"Ítem{i}: {solucion.distribucion[i]}" for i in range(1, itemes + 1)]
    console.print(f"   Distribución: {', '.join(distribuciones)}")
    console.print(f"   Ganancia: [green]{solucion.ganancia}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")

    console.print("\n[bold yellow]3. Ramificación y Acotamiento:[/bold yellow]")
    timer.cargar_tiempo()
    solucion = problema.busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()

    distribuciones = [f"Ítem{i}: {solucion.distribucion[i]}" for i in range(1, itemes + 1)]
    console.print(f"   Distribución: {', '.join(distribuciones)}")
    console.print(f"   Ganancia: [green]{solucion.ganancia}[/green]")
    console.print(f"   Soluciones exploradas: {solucion.soluciones_factibles}")
    console.print(f"   Tiempo: {timer.formato_tiempo(tiempo)}")

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold white]Demostración de Problemas Algorítmicos[/bold white]\n",
        border_style="cyan",
        box=box.DOUBLE
    ))
    
    demo_asignacion()
    demo_mochila()
    demo_vendedor()
    demo_recursos()
    
    console.print("\n\n[bold green]¡Demostración completada![/bold green]\n")
