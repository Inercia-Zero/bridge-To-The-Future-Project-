
import os
import re
import uuid
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

GRAPH_DIR = "generated_graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)

x = sp.symbols("x")

def _save_plot(fig):
    path = os.path.join(GRAPH_DIR, f"{uuid.uuid4().hex}.png")
    fig.savefig(path, bbox_inches="tight", dpi=180)
    plt.close(fig)
    return path

def _plot_function(expr_text: str):
    expr_text = expr_text.replace("^", "**")
    expr_text = expr_text.replace("f(x)=", "").replace("y=", "").replace(" ", "")
    expr = sp.sympify(expr_text)
    f = sp.lambdify(x, expr, "numpy")
    xs = np.linspace(-10, 10, 500)
    ys = f(xs)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, linewidth=2)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_title("Gráfico da função")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    return _save_plot(fig)

def _plot_mru():
    t = np.linspace(0, 10, 200)
    s = 2 + 3 * t
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, s, linewidth=2)
    ax.set_title("Exemplo de gráfico do MRU")
    ax.set_xlabel("t")
    ax.set_ylabel("s(t)")
    ax.grid(True, alpha=0.3)
    return _save_plot(fig)

def _plot_mruv():
    t = np.linspace(0, 10, 200)
    s = 1 + 2*t + 0.5*1.5*(t**2)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, s, linewidth=2)
    ax.set_title("Exemplo de gráfico do MRUV")
    ax.set_xlabel("t")
    ax.set_ylabel("s(t)")
    ax.grid(True, alpha=0.3)
    return _save_plot(fig)

def maybe_generate_graph(user_text: str, mentor: str):
    t = (user_text or "").lower()

    if mentor == "Matemática" and ("gráfico" in t or "grafico" in t):
        match = re.search(r"(?:f\(x\)\s*=|y\s*=)\s*([^\n\r]+)", user_text, flags=re.IGNORECASE)
        if match:
            try:
                return _plot_function(match.group(0))
            except Exception:
                return None

    if mentor == "Física":
        if "mruv" in t and ("gráfico" in t or "grafico" in t):
            return _plot_mruv()
        if "mru" in t and ("gráfico" in t or "grafico" in t):
            return _plot_mru()

    return None
