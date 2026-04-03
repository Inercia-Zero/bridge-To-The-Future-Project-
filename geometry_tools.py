import os
import uuid
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

GEOM_DIR = "generated_geometry"
os.makedirs(GEOM_DIR, exist_ok=True)


def _save(fig):
    path = os.path.join(GEOM_DIR, f"geom_{uuid.uuid4().hex}.png")
    fig.savefig(path, bbox_inches="tight", dpi=180)
    plt.close(fig)
    return path


def _is_geometry_request(text: str) -> bool:
    text = (text or "").lower()
    keys = [
        "pitágoras",
        "pitagoras",
        "triângulo",
        "triangulo",
        "área do triângulo",
        "area do triangulo",
        "metade de um quadrado",
        "metade de um retângulo",
        "metade de um retangulo",
        "demonstre",
        "demonstração",
        "demonstracao",
        "origem da fórmula",
        "origem da formula",
        "prove visualmente",
        "mostre visualmente",
        "explique por geometria",
        "visualize",
        "desmonte",
    ]
    return any(k in text for k in keys)


def _triangle_half_rectangle():
    fig, ax = plt.subplots(figsize=(6, 5))

    # retângulo base x altura
    rect = Rectangle((0, 0), 6, 4, fill=False, linewidth=2)
    ax.add_patch(rect)

    # triângulo dentro do retângulo
    tri = Polygon([(0, 0), (6, 0), (0, 4)], closed=True, alpha=0.35)
    ax.add_patch(tri)

    # diagonal do retângulo
    ax.plot([0, 6], [4, 0], linestyle="--", linewidth=1.5)

    ax.text(3, -0.35, "base", ha="center", fontsize=10)
    ax.text(-0.45, 2, "altura", va="center", rotation=90, fontsize=10)
    ax.text(2.1, 1.1, "triângulo", ha="center", fontsize=10)
    ax.text(3.4, 2.7, "retângulo", ha="center", fontsize=10)

    ax.set_title("Área do triângulo = metade do retângulo")
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 5)
    ax.set_aspect("equal")
    ax.axis("off")

    return _save(fig), (
        "Aqui está a ideia visual: o triângulo ocupa metade do retângulo "
        "de mesma base e altura. Por isso, a área do triângulo é "
        "base × altura ÷ 2."
    )


def _right_triangle_labeled():
    fig, ax = plt.subplots(figsize=(6, 5))

    tri = Polygon([(0, 0), (4, 0), (0, 3)], closed=True, fill=False, linewidth=2)
    ax.add_patch(tri)

    ax.text(2, -0.35, "base", ha="center", fontsize=10)
    ax.text(-0.45, 1.5, "altura", va="center", rotation=90, fontsize=10)
    ax.text(1.8, 1.7, "hipotenusa", rotation=36, fontsize=10)

    # marca do ângulo reto
    ax.plot([0.35, 0.35, 0], [0, 0.35, 0.35], linewidth=1.5)

    ax.set_title("Triângulo retângulo")
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 4.5)
    ax.set_aspect("equal")
    ax.axis("off")

    return _save(fig), (
        "Aqui está um triângulo retângulo com base, altura e hipotenusa identificadas."
    )


def _pythagoras_visual():
    fig, ax = plt.subplots(figsize=(7, 6))

    # triângulo retângulo 3-4-5
    tri = Polygon([(0, 0), (4, 0), (0, 3)], closed=True, fill=False, linewidth=2)
    ax.add_patch(tri)

    # quadrado sobre lado horizontal (a)
    sq_a = Rectangle((0, -4), 4, 4, fill=False, linewidth=2)
    ax.add_patch(sq_a)
    ax.text(2, -2, "a²", ha="center", va="center", fontsize=12)

    # quadrado sobre lado vertical (b)
    sq_b = Rectangle((-3, 0), 3, 3, fill=False, linewidth=2)
    ax.add_patch(sq_b)
    ax.text(-1.5, 1.5, "b²", ha="center", va="center", fontsize=12)

    # quadrado sobre hipotenusa (representação visual simplificada)
    hyp_square = Polygon(
        [(4, 0), (5.8, 2.4), (3.4, 4.2), (1.6, 1.8)],
        closed=True,
        fill=False,
        linewidth=2,
    )
    ax.add_patch(hyp_square)
    ax.text(3.7, 2.1, "c²", ha="center", va="center", fontsize=12)

    ax.text(2, -4.45, "lado a", ha="center", fontsize=10)
    ax.text(-3.4, 1.5, "lado b", rotation=90, va="center", fontsize=10)
    ax.text(2.0, 1.25, "triângulo", ha="center", fontsize=10)

    # marca do ângulo reto
    ax.plot([0.35, 0.35, 0], [0, 0.35, 0.35], linewidth=1.5)

    ax.set_title("Visualização do Teorema de Pitágoras")
    ax.set_xlim(-4.5, 7)
    ax.set_ylim(-5.2, 6)
    ax.set_aspect("equal")
    ax.axis("off")

    return _save(fig), (
        "Aqui está uma visualização do Teorema de Pitágoras: as áreas "
        "a² e b² se relacionam com a área c²."
    )


def maybe_generate_geometry_visual(user_input: str, mentor: str):
    if mentor not in ["Matemática", "Física"]:
        return None, None

    text = (user_input or "").lower()

    if not _is_geometry_request(text):
        return None, None

    # Pitágoras
    if "pitágoras" in text or "pitagoras" in text:
        return _pythagoras_visual()

    # Área do triângulo / metade do retângulo
    if (
        "área do triângulo" in text
        or "area do triangulo" in text
        or "metade de um quadrado" in text
        or "metade de um retângulo" in text
        or "metade de um retangulo" in text
    ):
        return _triangle_half_rectangle()

    # Triângulo genérico / triângulo retângulo
    if "triângulo" in text or "triangulo" in text:
        return _right_triangle_labeled()

    return None, None
