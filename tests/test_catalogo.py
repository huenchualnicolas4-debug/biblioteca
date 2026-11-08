import pytest

from servicios.catalogo.modelos import Libro
from servicios.errores import LibroNoEncontrado, SinEjemplaresDisponibles


def test_libro_nuevo_tiene_todos_sus_ejemplares_disponibles():
    libro = Libro("1", "Título", "Autor", 3)
    assert libro.ejemplares_disponibles == 3


def test_libro_sin_ejemplares_es_invalido():
    with pytest.raises(ValueError):
        Libro("1", "Título", "Autor", 0)


def test_buscar_por_autor(catalogo):
    resultados = catalogo.buscar("martin")
    assert [libro.isbn for libro in resultados] == ["978-3", "978-2"]


def test_buscar_no_distingue_mayusculas(catalogo):
    assert catalogo.buscar("SOLEDAD")[0].isbn == "978-1"


def test_buscar_varias_palabras_exige_todas(catalogo):
    resultados = catalogo.buscar("clean code")
    assert [libro.isbn for libro in resultados] == ["978-2"]


def test_buscar_sin_coincidencias_o_texto_vacio(catalogo):
    assert catalogo.buscar("python") == []
    assert catalogo.buscar("   ") == []


def test_obtener_isbn_inexistente_lanza_error(catalogo):
    with pytest.raises(LibroNoEncontrado):
        catalogo.obtener("no-existe")


def test_reservar_descuenta_un_ejemplar(catalogo):
    catalogo.reservar_ejemplar("978-1")
    assert catalogo.obtener("978-1").ejemplares_disponibles == 1


def test_reservar_sin_stock_lanza_error(catalogo):
    catalogo.reservar_ejemplar("978-2")
    with pytest.raises(SinEjemplaresDisponibles):
        catalogo.reservar_ejemplar("978-2")


def test_liberar_nunca_supera_el_total(catalogo):
    catalogo.liberar_ejemplar("978-2")
    assert catalogo.obtener("978-2").ejemplares_disponibles == 1
