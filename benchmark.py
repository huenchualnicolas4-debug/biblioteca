"""Compara el tiempo de búsqueda del sistema heredado vs. el servicio nuevo.

Uso: python benchmark.py   (genera resultados_benchmark.csv; luego python graficar.py)
"""
import csv
import random
import statistics
import time

from legacy.sistema_monolitico import SistemaBiblioteca
from servicios.catalogo.repositorio import RepositorioLibrosEnMemoria
from servicios.catalogo.servicio import ServicioCatalogo

PALABRAS = ["historia", "datos", "python", "java", "redes", "chile", "medicina",
            "software", "algoritmos", "poesia", "derecho", "economia", "arte"]
TAMANOS = [1_000, 5_000, 10_000, 50_000, 100_000]
CONSULTAS = 200


def generar_libros(n, rng):
    """Crea n libros con títulos aleatorios reproducibles."""
    for i in range(n):
        titulo = " ".join(rng.sample(PALABRAS, 3)) + f" vol{i}"
        yield f"isbn-{i}", titulo, f"Autor {i % 500}", 2


def medir(funcion, consultas):
    """Tiempo promedio por consulta en milisegundos."""
    tiempos = []
    for texto in consultas:
        inicio = time.perf_counter()
        funcion(texto)
        tiempos.append((time.perf_counter() - inicio) * 1000)
    return statistics.mean(tiempos)


def main():
    rng = random.Random(42)
    filas = []
    for n in TAMANOS:
        heredado = SistemaBiblioteca()
        nuevo = ServicioCatalogo(RepositorioLibrosEnMemoria())
        for isbn, titulo, autor, cant in generar_libros(n, rng):
            heredado.agregar_libro(isbn, titulo, autor, cant)
            nuevo.agregar_libro(isbn, titulo, autor, cant)
        consultas = [f"vol{rng.randrange(n)}" for _ in range(CONSULTAS)]
        t_her = medir(heredado.buscar, consultas)
        t_nue = medir(nuevo.buscar, consultas)
        filas.append((n, round(t_her, 4), round(t_nue, 4)))
        print(f"{n:>7} libros | heredado {t_her:8.3f} ms | nuevo {t_nue:6.4f} ms")

    with open("resultados_benchmark.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["libros", "heredado_ms", "nuevo_ms"])
        escritor.writerows(filas)
    return filas


if __name__ == "__main__":
    main()
