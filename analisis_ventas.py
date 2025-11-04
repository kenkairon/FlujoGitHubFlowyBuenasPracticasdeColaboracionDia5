"""
analisis_venta.py

Plantilla para un dashboard de ventas con matplotlib.
Incluye:
- configuración de colores corporativos por defecto
- funciones utilitarias para configurar estilo global
- funciones ejemplo para generar gráficas típicas de ventas

Uso:
from analisis_venta import set_default_style, generar_dashboard

set_default_style()
fig = generar_dashboard(df)  # df debe contener columnas: 'fecha', 'categoria', 'ventas'

"""

from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# -----------------------------
# Colores corporativos por defecto
# -----------------------------
CORPORATE_COLORS = [
    "#0B5FFF",  # Azul primario
    "#00B37E",  # Verde secundario
    "#FFB020",  # Amarillo/Accent
    "#E11D48",  # Rojo/Accent
    "#7C3AED",  # Morado
    "#06B6D4",  # Cyan
]

# Opciones de estilo por defecto
DEFAULT_STYLE = {
    "figure.figsize": (12, 7),
    "axes.titlesize": 16,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "lines.linewidth": 2,
    "grid.alpha": 0.25,
}

# -----------------------------
# Funciones de configuración
# -----------------------------

def set_default_style(colors: Optional[list] = None, style_opts: Optional[dict] = None) -> None:
    if colors is None:
        colors = CORPORATE_COLORS
    if style_opts is None:
        style_opts = DEFAULT_STYLE

    plt.rcParams.update(style_opts)
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "#FBFBFD"
    plt.rcParams["grid.color"] = "#DDE6F6"
    plt.rcParams["axes.edgecolor"] = "#2B2B2B"
    plt.rcParams["axes.grid"] = True


# -----------------------------
# Funciones utilitarias de gráfico
# -----------------------------

def _format_eje_fecha(ax, fecha_col: str = "fecha"):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")


def plot_ventas_tiempo(ax, df: pd.DataFrame, fecha_col: str = "fecha", ventas_col: str = "ventas"):
    series = df.groupby(fecha_col)[ventas_col].sum().sort_index()
    ax.plot(series.index, series.values, marker="o")
    ax.set_title("Ventas en el tiempo")
    ax.set_ylabel("Ventas")
    _format_eje_fecha(ax, fecha_col)


def plot_ventas_por_categoria(ax, df: pd.DataFrame, cat_col: str = "categoria", ventas_col: str = "ventas", top_n: int = 8):
    agg = df.groupby(cat_col)[ventas_col].sum().sort_values(ascending=False)
    agg_to_plot = agg.head(top_n)
    ax.bar(agg_to_plot.index.astype(str), agg_to_plot.values)
    ax.set_title(f"Top {len(agg_to_plot)} categorías por ventas")
    ax.set_ylabel("Ventas")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")


def plot_participacion_pie(ax, df: pd.DataFrame, cat_col: str = "categoria", ventas_col: str = "ventas", top_n: int = 6):
    agg = df.groupby(cat_col)[ventas_col].sum().sort_values(ascending=False)
    top = agg.head(top_n)
    others = agg.iloc[top_n:].sum()
    if others > 0:
        top["Otros"] = others
    ax.pie(top.values, labels=top.index.astype(str), autopct="%1.1f%%", startangle=140)
    ax.set_title("Participación por categoría")


# -----------------------------
# Generador de dashboard
# -----------------------------

def generar_dashboard(df: pd.DataFrame, fecha_col: str = "fecha", cat_col: str = "categoria", ventas_col: str = "ventas") -> plt.Figure:
    if fecha_col not in df.columns or cat_col not in df.columns or ventas_col not in df.columns:
        raise ValueError(f"El DataFrame debe contener las columnas: {fecha_col}, {cat_col}, {ventas_col}")

    df_copy = df.copy()
    if not np.issubdtype(df_copy[fecha_col].dtype, np.datetime64):
        df_copy[fecha_col] = pd.to_datetime(df_copy[fecha_col])

    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    ax_time = axs[0, 0]
    ax_bar = axs[0, 1]
    ax_pie = axs[1, 0]
    ax_empty = axs[1, 1]

    plot_ventas_tiempo(ax_time, df_copy, fecha_col, ventas_col)
    plot_ventas_por_categoria(ax_bar, df_copy, cat_col, ventas_col)
    plot_participacion_pie(ax_pie, df_copy, cat_col, ventas_col)

    total_ventas = df_copy[ventas_col].sum()
    promedio_diario = df_copy.groupby(fecha_col)[ventas_col].sum().mean()
    ax_empty.axis("off")
    texto_kpi = (
        f"Total ventas: {total_ventas:,.0f}\n"
        f"Promedio diario: {promedio_diario:,.0f}\n"
        f"Días: {df_copy[fecha_col].nunique()}\n"
        f"Categorías: {df_copy[cat_col].nunique()}"
    )
    ax_empty.text(0.02, 0.95, texto_kpi, va="top", fontsize=12, family="monospace")

    fig.suptitle("Dashboard de Ventas", fontsize=20)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig


if __name__ == "__main__":
    set_default_style()
    fechas = pd.date_range(end=pd.Timestamp.today(), periods=30)
    categorias = ["A", "B", "C", "D", "E"]
    data = []
    rng = np.random.default_rng(42)
    for f in fechas:
        for c in categorias:
            data.append({"fecha": f, "categoria": c, "ventas": rng.integers(50, 500)})
    df_demo = pd.DataFrame(data)
    fig = generar_dashboard(df_demo)
    plt.show()
