from datetime import date

import pytest

from servicios.multas.calculadora import PoliticaMultas

LIMITE = date(2026, 11, 16)


@pytest.mark.parametrize("devolucion, esperado", [
    (date(2026, 11, 10), 0),       # antes de la fecha límite
    (date(2026, 11, 16), 0),       # justo el día límite
    (date(2026, 11, 17), 500),     # 1 día de atraso
    (date(2026, 11, 26), 5_000),   # 10 días de atraso
    (date(2026, 12, 31), 10_000),  # supera el tope
])
def test_calculo_de_multa(devolucion, esperado):
    assert PoliticaMultas().calcular(LIMITE, devolucion) == esperado


def test_dias_de_gracia_se_descuentan():
    politica = PoliticaMultas(dias_gracia=2)
    assert politica.calcular(LIMITE, date(2026, 11, 18)) == 0
    assert politica.calcular(LIMITE, date(2026, 11, 19)) == 500
