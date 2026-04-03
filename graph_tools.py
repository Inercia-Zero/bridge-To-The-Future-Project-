import os
import re
import uuid
import numpy as np
import matplotlib.pyplot as plt

GRAPH_DIR = "generated_graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)


def _save_plot(fig):
    filename = f"graph_{uuid.uuid4().hex}.png"
    path = os.path.join(GRAPH_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=180)
    plt.close(fig)
    return path


def _detect_graph_request(text: str) -> bool:
    text = (text or "").lower()
    keywords = [
        "grafico", "gráfico", "plot", "plote", "desenhe",
        "gere", "represente", "plano cartesiano",
        "pontos", "pares ordenados", "função afim", "funcao afim",
        "função quadrática", "funcao quadratica", "reta", "parábola", "parabola",
        "mru", "mruv", "velocidade", "posição", "posicao", "aceleração", "aceleracao",
        "liga os pontos", "ligue os pontos", "não liga", "nao liga",
    ]
    return any(k in text for k in keywords)


def _extract_function(text: str):
    text = (text or "").lower().replace("^", "**")

    match = re.search(r"f\s*\(\s*x\s*\)\s*=\s*([^\n\r]+)", text)
    if match:
        return match.group(1).strip()

    match = re.search(r"y\s*=\s*([^\n\r]+)", text)
    if match:
        return match.group(1).strip()

    return None


def _extract_points_pairs(text: str):
    pairs = re.findall(r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", text)
    if not pairs:
        return None
    points = [(float(x), float(y)) for x, y in pairs]
    return points if len(points) >= 2 else None


def _extract_points_xy_lists(text: str):
    text = text.lower()

    mx = re.search(r"x\s*:\s*([\d,\.\-\s]+)", text)
    my = re.search(r"y\s*:\s*([\d,\.\-\s]+)", text)
    if not (mx and my):
        return None

    xs = [float(v.strip()) for v in mx.group(1).split(",") if v.strip()]
    ys = [float(v.strip()) for v in my.group(1).split(",") if v.strip()]

    if len(xs) >= 2 and len(xs) == len(ys):
        return list(zip(xs, ys))
    return None


def _infer_default_function(text: str):
    text = (text or "").lower()

    if "quadrática" in text or "quadratica" in text or "parábola" in text or "parabola" in text:
        return "x**2"
    if "afim" in text or "reta" in text or "linear" in text:
        return "x + 1"
    return "x"


def _plot_function(func_str: str):
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
    return _save_plot(fig)


def _plot_points(points, linked=False, title="Plano cartesiano"):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(xs, ys, s=45)

    if linked:
        ax.plot(xs, ys, linewidth=1.8)

    for x, y in points:
        ax.annotate(f"({x:g}, {y:g})", (x, y), textcoords="offset points", xytext=(6, 6), fontsize=8)

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return _save_plot(fig)


def _plot_mru():
    t = np.linspace(0, 10, 300)
    s = 2 + 3 * t

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, s, linewidth=2)
    ax.set_title("Gráfico do MRU")
    ax.set_xlabel("t")
    ax.set_ylabel("s(t)")
    ax.grid(True, alpha=0.3)
    return _save_plot(fig)


def _plot_mruv():
    t = np.linspace(0, 10, 300)
    s = 1 + 2 * t + 0.5 * 1.5 * (t ** 2)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, s, linewidth=2)
    ax.set_title("Gráfico do MRUV")
    ax.set_xlabel("t")
    ax.set_ylabel("s(t)")
    ax.grid(True, alpha=0.3)
    return _save_plot(fig)


def maybe_generate_graph(user_input: str, mentor: str, last_context=None):
    text = (user_input or "").lower()
    last_context = last_context or {}

    if mentor not in ["Matemática", "Física", "Metodologia Científica"]:
        return None, {}

    if not _detect_graph_request(text):
        points = _extract_points_pairs(user_input) or _extract_points_xy_lists(user_input)
        if not points:
            return None, {}

    if mentor == "Física":
        if "mruv" in text and _detect_graph_request(text):
            path = _plot_mruv()
            return path, {
                "mode": "physics_curve",
                "function": None,
                "points": None,
                "linked": True,
                "message": "Aqui está um gráfico de exemplo do MRUV.",
            }
        if "mru" in text and _detect_graph_request(text):
            path = _plot_mru()
            return path, {
                "mode": "physics_curve",
                "function": None,
                "points": None,
                "linked": True,
                "message": "Aqui está um gráfico de exemplo do MRU.",
            }

    points = _extract_points_pairs(user_input) or _extract_points_xy_lists(user_input)
    if points:
        linked = any(k in text for k in ["liga os pontos", "ligue os pontos", "conecte", "una os pontos"])
        if any(k in text for k in ["não liga", "nao liga", "sem ligar", "só os pontos", "so os pontos"]):
            linked = False

        path = _plot_points(points, linked=linked, title="Plano cartesiano com pontos")
        return path, {
            "mode": "points",
            "function": None,
            "points": points,
            "linked": linked,
            "message": "Aqui está o plano cartesiano com os pontos informados.",
        }

    if last_context.get("mode") == "points" and last_context.get("points"):
        if any(k in text for k in ["liga os pontos", "ligue os pontos", "conecte", "una os pontos"]):
            path = _plot_points(last_context["points"], linked=True, title="Plano cartesiano com pontos ligados")
            return path, {
                "mode": "points",
                "function": None,
                "points": last_context["points"],
                "linked": True,
                "message": "Agora liguei os pontos no plano cartesiano.",
            }
        if any(k in text for k in ["não liga", "nao liga", "sem ligar", "só os pontos", "so os pontos"]):
            path = _plot_points(last_context["points"], linked=False, title="Plano cartesiano com pontos")
            return path, {
                "mode": "points",
                "function": None,
                "points": last_context["points"],
                "linked": False,
                "message": "Agora deixei apenas os pontos no plano cartesiano.",
            }

    func = _extract_function(user_input)
    if func:
        path = _plot_function(func)
        if path:
            return path, {
                "mode": "function",
                "function": func,
                "points": None,
                "linked": False,
                "message": "Aqui está o gráfico da função informada.",
            }

    if _detect_graph_request(text):
        if any(k in text for k in ["quadrática", "quadratica", "parábola", "parabola"]):
            func = "x**2"
        elif any(k in text for k in ["afim", "reta", "linear"]):
            func = "x + 1"
        elif any(k in text for k in ["gere um", "gera um", "faça um", "faz um", "plote um"]) and last_context.get("function"):
            func = last_context["function"]
        else:
            func = _infer_default_function(text)

        path = _plot_function(func)
        if path:
            return path, {
                "mode": "function",
                "function": func,
                "points": None,
                "linked": False,
                "message": f"Aqui está um gráfico de exemplo para {func}.",
            }

    return None, {}
