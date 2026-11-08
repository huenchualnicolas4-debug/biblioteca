from datetime import date

import pytest

from servicios.errores import (LibroNoEncontrado, LimitePrestamosAlcanzado,
                               PrestamoNoEncontrado, PrestamoYaDevuelto,
                               SinEjemplaresDisponibles)


def test_prestar_fija_fecha_limite_a_14_dias(prestamos):
    prestamo = prestamos.prestar("u1", "978-1")
    assert prestamo.fecha_limite == date(2026, 11, 16)
    assert prestamo.activo


def test_prestar_descuenta_stock_del_catalogo(prestamos, catalogo):
    prestamos.prestar("u1", "978-1")
    assert catalogo.obtener("978-1").ejemplares_disponibles == 1


def test_no_se_puede_prestar_libro_sin_stock(prestamos):
    prestamos.prestar("u1", "978-2")
    with pytest.raises(SinEjemplaresDisponibles):
        prestamos.prestar("u2", "978-2")


def test_no_se_puede_prestar_libro_inexistente(prestamos):
    with pytest.raises(LibroNoEncontrado):
        prestamos.prestar("u1", "000")


def test_limite_de_tres_prestamos_activos(prestamos):
    for isbn in ("978-1", "978-2", "978-3"):
        prestamos.prestar("u1", isbn)
    with pytest.raises(LimitePrestamosAlcanzado):
        prestamos.prestar("u1", "978-1")


def test_devolver_a_tiempo_no_genera_multa(prestamos, catalogo, reloj):
    prestamo = prestamos.prestar("u1", "978-2")
    reloj.hoy = date(2026, 11, 10)
    assert prestamos.devolver(prestamo.id) == 0
    assert catalogo.obtener("978-2").ejemplares_disponibles == 1
    assert not prestamo.activo


def test_devolver_con_atraso_genera_multa(prestamos, reloj):
    prestamo = prestamos.prestar("u1", "978-2")
    reloj.hoy = date(2026, 11, 20)  # 4 días de atraso
    assert prestamos.devolver(prestamo.id) == 2_000


def test_devolucion_libera_cupo_del_usuario(prestamos):
    ids = [prestamos.prestar("u1", isbn).id for isbn in ("978-1", "978-2", "978-3")]
    prestamos.devolver(ids[0])
    assert prestamos.prestar("u1", "978-1").activo


def test_devolver_dos_veces_lanza_error(prestamos):
    prestamo = prestamos.prestar("u1", "978-1")
    prestamos.devolver(prestamo.id)
    with pytest.raises(PrestamoYaDevuelto):
        prestamos.devolver(prestamo.id)


def test_devolver_prestamo_inexistente_lanza_error(prestamos):
    with pytest.raises(PrestamoNoEncontrado):
        prestamos.devolver(999)
