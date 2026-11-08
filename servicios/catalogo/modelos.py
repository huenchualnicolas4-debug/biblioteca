"""Modelos del servicio de catálogo."""
from dataclasses import dataclass


@dataclass
class Libro:
    """Un título del catálogo con su stock de ejemplares."""

    isbn: str
    titulo: str
    autor: str
    ejemplares_totales: int
    ejemplares_disponibles: int = -1

    def __post_init__(self):
        if self.ejemplares_totales < 1:
            raise ValueError("Un libro debe tener al menos un ejemplar")
        if self.ejemplares_disponibles == -1:
            self.ejemplares_disponibles = self.ejemplares_totales
