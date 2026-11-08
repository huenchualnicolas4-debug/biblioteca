"""Servicio de préstamos: presta y recibe devoluciones.

Recibe sus dependencias por constructor (inyección de dependencias), lo que
permite probarlo con un reloj falso y, en una arquitectura distribuida,
reemplazar el catálogo local por un cliente HTTP del microservicio de catálogo.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from itertools import count
from typing import Callable

from servicios.catalogo.servicio import ServicioCatalogo
from servicios.errores import (LimitePrestamosAlcanzado, PrestamoNoEncontrado,
                               PrestamoYaDevuelto)
from servicios.multas.calculadora import PoliticaMultas


@dataclass
class Prestamo:
    """Registro de un préstamo; fecha_devolucion es None mientras está activo."""

    id: int
    usuario_id: str
    isbn: str
    fecha_prestamo: date
    fecha_limite: date
    fecha_devolucion: date | None = None
    multa: int = 0

    @property
    def activo(self) -> bool:
        """True si el libro aún no se devuelve."""
        return self.fecha_devolucion is None


class ServicioPrestamos:
    """Única responsabilidad: ciclo de vida de los préstamos."""

    def __init__(self, catalogo: ServicioCatalogo, politica: PoliticaMultas,
                 reloj: Callable[[], date] = date.today,
                 dias_prestamo: int = 14, max_prestamos: int = 3):
        self._catalogo = catalogo
        self._politica = politica
        self._reloj = reloj
        self._dias_prestamo = dias_prestamo
        self._max_prestamos = max_prestamos
        self._prestamos: dict[int, Prestamo] = {}
        self._ids = count(1)

    def prestamos_activos(self, usuario_id: str) -> list[Prestamo]:
        """Préstamos aún no devueltos por el usuario."""
        return [p for p in self._prestamos.values()
                if p.usuario_id == usuario_id and p.activo]

    def prestar(self, usuario_id: str, isbn: str) -> Prestamo:
        """Crea un préstamo si el usuario tiene cupo y hay stock."""
        if len(self.prestamos_activos(usuario_id)) >= self._max_prestamos:
            raise LimitePrestamosAlcanzado(usuario_id)
        self._catalogo.reservar_ejemplar(isbn)
        hoy = self._reloj()
        prestamo = Prestamo(next(self._ids), usuario_id, isbn, hoy,
                            hoy + timedelta(days=self._dias_prestamo))
        self._prestamos[prestamo.id] = prestamo
        return prestamo

    def devolver(self, prestamo_id: int) -> int:
        """Cierra el préstamo, libera el ejemplar y devuelve la multa en CLP."""
        prestamo = self._prestamos.get(prestamo_id)
        if prestamo is None:
            raise PrestamoNoEncontrado(prestamo_id)
        if not prestamo.activo:
            raise PrestamoYaDevuelto(prestamo_id)
        prestamo.fecha_devolucion = self._reloj()
        prestamo.multa = self._politica.calcular(prestamo.fecha_limite,
                                                 prestamo.fecha_devolucion)
        self._catalogo.liberar_ejemplar(prestamo.isbn)
        return prestamo.multa
