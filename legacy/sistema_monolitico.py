"""Versión heredada (monolítica) del sistema de biblioteca.

Se conserva solo como punto de comparación para el análisis de calidad
y las pruebas de rendimiento. NO se debe usar en código nuevo.
"""
import datetime


class SistemaBiblioteca:
    def __init__(self):
        self.libros = []
        self.prestamos = []
        self.usuarios = []

    def agregar_libro(self, isbn, titulo, autor, cantidad):
        self.libros.append({"isbn": isbn, "titulo": titulo, "autor": autor,
                            "cantidad": cantidad, "disponibles": cantidad})

    def buscar(self, texto):
        res = []
        for l in self.libros:
            if texto.lower() in l["titulo"].lower() or texto.lower() in l["autor"].lower():
                res.append(l)
        return res

    def prestar(self, usuario, isbn):
        n = 0
        for p in self.prestamos:
            if p["usuario"] == usuario and p["devuelto"] == False:
                n = n + 1
        if n >= 3:
            print("error: usuario con muchos prestamos")
            return None
        for l in self.libros:
            if l["isbn"] == isbn:
                if l["disponibles"] > 0:
                    l["disponibles"] = l["disponibles"] - 1
                    p = {"id": len(self.prestamos) + 1, "usuario": usuario, "isbn": isbn,
                         "fecha": datetime.date.today(),
                         "limite": datetime.date.today() + datetime.timedelta(days=14),
                         "devuelto": False, "multa": 0}
                    self.prestamos.append(p)
                    return p
                else:
                    print("error: no hay ejemplares")
                    return None
        print("error: libro no existe")
        return None

    def devolver(self, id):
        for p in self.prestamos:
            if p["id"] == id:
                if p["devuelto"] == True:
                    return 0
                p["devuelto"] = True
                hoy = datetime.date.today()
                if hoy > p["limite"]:
                    d = (hoy - p["limite"]).days
                    m = d * 500
                    if m > 10000:
                        m = 10000
                    p["multa"] = m
                for l in self.libros:
                    if l["isbn"] == p["isbn"]:
                        l["disponibles"] = l["disponibles"] + 1
                return p["multa"]
        return -1
