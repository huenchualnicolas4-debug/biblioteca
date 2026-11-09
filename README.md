# Sistema de Gestión de Bibliotecas – Universidad X

Prototipo en Python de la nueva arquitectura del sistema de bibliotecas,
separado en tres servicios con responsabilidades únicas:

| Servicio | Carpeta | Responsabilidad |
|---|---|---|
| Catálogo | `servicios/catalogo` | Alta de libros, búsqueda indexada, stock |
| Préstamos | `servicios/prestamos` | Prestar, devolver, límite por usuario |
| Multas | `servicios/multas` | Cálculo de multas configurable |

`legacy/` contiene la versión monolítica original, usada solo para comparar.

## Cómo ejecutar

```bash
pip install -r requirements.txt          # herramientas locales (incluye matplotlib)
pytest --cov=servicios --cov-report=term-missing   # 26 pruebas, 100 % cobertura
pylint servicios legacy                             # análisis estático
python benchmark.py && python graficar.py           # rendimiento heredado vs nuevo
```

## Flujo de trabajo (GitHub Flow)

1. Crear una rama desde `main`: `feature/<nombre>` o `fix/<nombre>`.
2. Commits pequeños con mensaje descriptivo.
3. Abrir Pull Request: la CI (`.github/workflows/ci.yml`) corre pytest y pylint.
4. Revisión de código por un par antes de hacer merge a `main`.
