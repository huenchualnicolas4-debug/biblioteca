"""Acceso a datos del catálogo.

RepositorioLibros define el contrato (principio de inversión de dependencias).
La implementación en memoria usa un índice invertido para que la búsqueda
no recorra todo el catálogo; en producción se reemplazaría por una
implementación sobre PostgreSQL o Elasticsearch sin tocar el servicio.
"""
import re
from abc import ABC, abstractmethod

from servicios.catalogo.modelos import Libro


def extraer_palabras(texto: str) -> set[str]:
    """Normaliza un texto a un conjunto de palabras en minúscula."""
    return set(re.findall(r"\w+", texto.lower()))


class RepositorioLibros(ABC):
    """Contrato que debe cumplir cualquier almacenamiento de libros."""

    @abstractmethod
    def guardar(self, libro: Libro) -> None:
        """Inserta o actualiza un libro."""

    @abstractmethod
    def obtener(self, isbn: str) -> Libro | None:
        """Busca por ISBN; None si no existe."""

    @abstractmethod
    def buscar_por_palabra(self, palabra: str) -> list[Libro]:
        """Libros cuyo título o autor contiene la palabra."""


class RepositorioLibrosEnMemoria(RepositorioLibros):
    """Implementación en memoria con índice invertido palabra -> ISBN."""

    def __init__(self):
        self._libros: dict[str, Libro] = {}
        self._indice: dict[str, set[str]] = {}

    def guardar(self, libro: Libro) -> None:
        self._libros[libro.isbn] = libro
        for palabra in extraer_palabras(f"{libro.titulo} {libro.autor}"):
            self._indice.setdefault(palabra, set()).add(libro.isbn)

    def obtener(self, isbn: str) -> Libro | None:
        return self._libros.get(isbn)

    def buscar_por_palabra(self, palabra: str) -> list[Libro]:
        isbns = self._indice.get(palabra.lower(), set())
        return [self._libros[isbn] for isbn in isbns]
