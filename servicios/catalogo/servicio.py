"""Servicio de catálogo: alta de libros, búsqueda y control de stock."""
from servicios.catalogo.modelos import Libro
from servicios.catalogo.repositorio import RepositorioLibros, extraer_palabras
from servicios.errores import LibroNoEncontrado, SinEjemplaresDisponibles


class ServicioCatalogo:
    """Única responsabilidad: administrar libros y su disponibilidad."""

    def __init__(self, repositorio: RepositorioLibros):
        self._repo = repositorio

    def agregar_libro(self, isbn: str, titulo: str, autor: str, ejemplares: int) -> Libro:
        """Registra un título nuevo en el catálogo."""
        libro = Libro(isbn, titulo, autor, ejemplares)
        self._repo.guardar(libro)
        return libro

    def obtener(self, isbn: str) -> Libro:
        """Devuelve el libro o lanza LibroNoEncontrado."""
        libro = self._repo.obtener(isbn)
        if libro is None:
            raise LibroNoEncontrado(isbn)
        return libro

    def buscar(self, texto: str) -> list[Libro]:
        """Devuelve los libros que contienen TODAS las palabras buscadas."""
        palabras = extraer_palabras(texto)
        if not palabras:
            return []
        conjuntos = [{libro.isbn for libro in self._repo.buscar_por_palabra(p)}
                     for p in palabras]
        isbns = set.intersection(*conjuntos)
        return sorted((self.obtener(i) for i in isbns), key=lambda libro: libro.titulo)

    def reservar_ejemplar(self, isbn: str) -> None:
        """Descuenta un ejemplar disponible (se usa al prestar)."""
        libro = self.obtener(isbn)
        if libro.ejemplares_disponibles == 0:
            raise SinEjemplaresDisponibles(isbn)
        libro.ejemplares_disponibles -= 1
        self._repo.guardar(libro)

    def liberar_ejemplar(self, isbn: str) -> None:
        """Devuelve un ejemplar al stock (se usa al devolver)."""
        libro = self.obtener(isbn)
        if libro.ejemplares_disponibles < libro.ejemplares_totales:
            libro.ejemplares_disponibles += 1
            self._repo.guardar(libro)
