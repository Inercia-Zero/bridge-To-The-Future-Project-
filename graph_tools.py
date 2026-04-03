import os
import re
import uuid
import numpy as np
import matplotlib.pyplot as plt

GRAPH_DIR = "generated_graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)


def detect_graph_request(text: str) -> bool:
    text = (text or "").lower()

    keywords = [
        "grafico",
        "gráfico",
        "plot",
        "desenhe",
        "gere",
        "represente",
        "função afim",
        "funcao afim",
        "reta",
        "parábola",
        "parabola",
    ]

    return any(k in text for k in keywords)


def extract_function(text: str):
    text = (text or "").lower().replace("^", "**")

    # y = ...
    match = re.search(r"y\s*=\s*([0-9x\+\-\*/\.\(\)\s\*]+)", text)
    if match:
        return match.group(1).strip()

    # f(x) = ...
    match = re.search(r"f\s*\(\s*x\s*\)\s*=\s*([0-9x\+\-\*/\.\(\)\s\*]+)", text)
    if match:
        return match.group(1).strip()

    return None


def infer_default_function(text: str):
    text = (text or "").lower()

    if "função afim" in text or "funcao afim" in text or "reta" in text:
        return "x + 1"

    if "função quadrática" in text or "funcao quadratica" in text or "parábola" in text or "parabola" in text:
        return "x**2"

    return "x"


def save_plot(fig):
    filename = f"graph_{uuid.uuid4().hex}.png"
    path = os.path.join(GRAPH_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=180)
    plt.close(fig)
    return path


def plot_function(func_str: str):
    x = np.linspace(-10, 10, 400)

    try:
        y = eval(func_str, {"x": x, "np": np})
    except Exception:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, linewidth=2)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, alpha=0.3)
    ax.set_title(f"Gráfico de y = {func_str}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    return save_plot(fig)


def plot_mru():
    t = np.linspace(0, 10, 300)
    s = 2 + 3 * t

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, s, linewidth=2)
    ax.set_title("Gráfico do MRU")
    ax.set_xlabel("t")
    ax.set_ylabel("s(t)")
    ax.grid(True, alpha=0.3)

    return save_plot(fig)


def plot_mruv():
    t = np.linspace(0, 10, 300)
    s = 1 + 2 * t + 0.5 * 1.5 * (t ** 2)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, s, linewidth=2)
    ax.set_title("Gráfico do MRUV")
    ax.set_xlabel("t")
    ax.set_ylabel("s(t)")
    ax.grid(True, alpha=0.3)

    return save_plot(fig)


def maybe_generate_graph(user_input: str, mentor: str):
    text = (user_input or "").lower()

    if mentor not in ["Matemática", "Física"]:
        return None

    if mentor == "Física":
        if ("mruv" in text) and detect_graph_request(text):
            return plot_mruv()
        if ("mru" in text) and detect_graph_request(text):
            return plot_mru()

    if detect_graph_request(text):
        func = extract_function(text)

        if not func:
            func = infer_default_function(text)

        return plot_function(func)

    return None
