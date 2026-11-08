"""Servicio de multas: calcula el cobro por devolución atrasada."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PoliticaMultas:
    """Reglas configurables (antes estaban como números fijos en el código)."""

    tarifa_diaria: int = 500      # CLP por día de atraso
    dias_gracia: int = 0
    tope: int = 10_000            # monto máximo por préstamo

    def calcular(self, fecha_limite: date, fecha_devolucion: date) -> int:
        """Monto en CLP según días de atraso, con días de gracia y tope."""
        dias_atraso = (fecha_devolucion - fecha_limite).days - self.dias_gracia
        if dias_atraso <= 0:
            return 0
        return min(dias_atraso * self.tarifa_diaria, self.tope)
