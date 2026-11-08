"""Genera grafico_rendimiento.png a partir de resultados_benchmark.csv."""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

with open("resultados_benchmark.csv", encoding="utf-8") as f:
    filas = list(csv.DictReader(f))
n = [int(r["libros"]) for r in filas]
her = [float(r["heredado_ms"]) for r in filas]
nue = [float(r["nuevo_ms"]) for r in filas]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=200)
fig.patch.set_facecolor("#ffffff"); ax.set_facecolor("#ffffff")
ax.plot(n, her, color="#2a78d6", lw=2, marker="o", ms=5, label="Monolito heredado (búsqueda lineal)")
ax.plot(n, nue, color="#eb6834", lw=2, marker="o", ms=5, label="Servicio de catálogo (índice invertido)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xticks(n); ax.set_xticklabels([f"{x:,}".replace(",", ".") for x in n])
ax.set_xlabel("Libros en el catálogo", color="#52514e")
ax.set_ylabel("ms por búsqueda (log)", color="#52514e")
ax.annotate(f"{her[-1]:.1f} ms".replace(".", ","), (n[-1], her[-1]), xytext=(-8, 8), textcoords="offset points", ha="right", color="#0b0b0b")
ax.annotate(f"{nue[-1]:.4f} ms".replace(".", ","), (n[-1], nue[-1]), xytext=(-8, 8), textcoords="offset points", ha="right", color="#0b0b0b")
ax.grid(True, which="major", color="#e6e5e1", lw=0.6)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color("#b5b4ae")
ax.tick_params(colors="#52514e")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=8.5)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
fig.tight_layout()
fig.savefig("grafico_rendimiento.png", facecolor=fig.get_facecolor())
