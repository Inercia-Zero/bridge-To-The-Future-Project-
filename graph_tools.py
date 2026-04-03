import re
import numpy as np
import matplotlib.pyplot as plt
import uuid
import os


def extract_function(text):
    match = re.search(r"y\s*=\s*([0-9x+\-*/\s\.]+)", text.lower())
    if match:
        return match.group(1)
    return None


def maybe_generate_graph(user_input, mentor):
    if mentor not in ["Matemática", "Física"]:
        return None

    func = extract_function(user_input)

    if not func:
        return None

    try:
        x = np.linspace(-10, 10, 200)
        y = eval(func)

        plt.figure()
        plt.plot(x, y)
        plt.axhline(0)
        plt.axvline(0)
        plt.grid()

        filename = f"graph_{uuid.uuid4().hex}.png"
        path = os.path.join("uploads", filename)

        os.makedirs("uploads", exist_ok=True)
        plt.savefig(path)
        plt.close()

        return path

    except Exception:
        return None
