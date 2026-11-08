"""Excepciones de dominio compartidas por los servicios."""


class ErrorBiblioteca(Exception):
    """Error base del sistema de biblioteca."""


class LibroNoEncontrado(ErrorBiblioteca):
    """El ISBN solicitado no existe en el catálogo."""


class SinEjemplaresDisponibles(ErrorBiblioteca):
    """Todos los ejemplares del libro están prestados."""


class LimitePrestamosAlcanzado(ErrorBiblioteca):
    """El usuario ya tiene el máximo de préstamos activos."""


class PrestamoNoEncontrado(ErrorBiblioteca):
    """El identificador de préstamo no existe."""


class PrestamoYaDevuelto(ErrorBiblioteca):
    """Se intentó devolver un préstamo que ya estaba cerrado."""
