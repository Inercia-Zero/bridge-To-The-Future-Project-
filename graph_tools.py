import os
import re
import uuid
import numpy as np
import matplotlib.pyplot as plt

GRAPH_DIR = "generated_graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)


def _save(fig):
    path = os.path.join(GRAPH_DIR, f"graph_{uuid.uuid4().hex}.png")
    fig.savefig(path, bbox_inches="tight", dpi=180)
    plt.close(fig)
    return path


# =========================================================
# DETECÇÃO DE PEDIDO DE GRÁFICO
# =========================================================
def is_graph_request(text: str):
    text = (text or "").lower()

    keywords = [
        "gráfico",
        "grafico",
        "plote",
        "plot",
        "desenhe",
        "função",
        "funcao",
        "parábola",
        "parabola",
        "(",
        ",",
    ]

    return any(k in text for k in keywords)


# =========================================================
# DETECTAR PONTOS (x,y)
# =========================================================
def extract_points(text: str):
    matches = re.findall(r"\((-?\d+\.?\d*),\s*(-?\d+\.?\d*)\)", text)
    if matches:
        return [(float(x), float(y)) for x, y in matches]
    return None


# =========================================================
# FUNÇÃO AFIM
# =========================================================
def generate_linear():
    x = np.linspace(-10, 10, 100)
    y = x  # padrão

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(0)
    ax.axvline(0)
    ax.set_title("Função afim: y = x")

    return _save(fig), "Gráfico de uma função afim (reta)."


# =========================================================
# FUNÇÃO QUADRÁTICA INTELIGENTE
# =========================================================
def generate_quadratic(text: str):
    text = text.lower()

    x = np.linspace(-10, 10, 200)

    # 🔥 CASO: a < 0
    if "a < 0" in text or "a menor que 0" in text:
        a = -1
        b = 2
        c = 1
        y = a * x**2 + b * x + c

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.axhline(0)
        ax.axvline(0)

        ax.set_title("Parábola com a < 0 (aberta para baixo)")

        return _save(fig), "Aqui está um gráfico de função quadrática com a < 0 (parábola para baixo)."

    # 🔥 CASO: a > 0
    if "a > 0" in text or "a maior que 0" in text:
        y = x**2

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.axhline(0)
        ax.axvline(0)

        ax.set_title("Parábola com a > 0 (aberta para cima)")

        return _save(fig), "Aqui está um gráfico de função quadrática com a > 0."

    # padrão
    y = x**2
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(0)
    ax.axvline(0)
    ax.set_title("Função quadrática padrão")

    return _save(fig), "Aqui está um gráfico de exemplo de função quadrática."


# =========================================================
# GRÁFICO DE PONTOS
# =========================================================
def generate_points_graph(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    fig, ax = plt.subplots()
    ax.scatter(xs, ys)

    for i, (x, y) in enumerate(points):
        ax.text(x, y, f"({x},{y})")

    ax.axhline(0)
    ax.axvline(0)
    ax.set_title("Gráfico de pontos fornecidos")

    return _save(fig), "Aqui estão os pontos plotados no plano cartesiano."


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================
def maybe_generate_graph(user_input: str, mentor: str):
    if mentor not in ["Matemática", "Física"]:
        return None, None

    if not is_graph_request(user_input):
        return None, None

    # 🔥 prioridade 1 → pontos
    points = extract_points(user_input)
    if points:
        return generate_points_graph(points)

    text = user_input.lower()

    # 🔥 prioridade 2 → função quadrática
    if "segundo grau" in text or "quadrática" in text or "parábola" in text:
        return generate_quadratic(text)

    # 🔥 prioridade 3 → função afim
    if "afim" in text or "reta" in text:
        return generate_linear()

    return None, None
