from datetime import date

import pytest

from servicios.catalogo.repositorio import RepositorioLibrosEnMemoria
from servicios.catalogo.servicio import ServicioCatalogo
from servicios.multas.calculadora import PoliticaMultas
from servicios.prestamos.servicio import ServicioPrestamos


class RelojFalso:
    """Permite controlar la fecha 'actual' dentro de las pruebas."""

    def __init__(self, hoy: date):
        self.hoy = hoy

    def __call__(self) -> date:
        return self.hoy


@pytest.fixture
def catalogo():
    servicio = ServicioCatalogo(RepositorioLibrosEnMemoria())
    servicio.agregar_libro("978-1", "Cien años de soledad", "Gabriel García Márquez", 2)
    servicio.agregar_libro("978-2", "Clean Code", "Robert C. Martin", 1)
    servicio.agregar_libro("978-3", "Clean Architecture", "Robert C. Martin", 1)
    return servicio


@pytest.fixture
def reloj():
    return RelojFalso(date(2026, 11, 2))


@pytest.fixture
def prestamos(catalogo, reloj):
    return ServicioPrestamos(catalogo, PoliticaMultas(), reloj=reloj)
