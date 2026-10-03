import csv
import json
from pathlib import Path

# este fichero esta en src/, el csv y el json estan un piso arriba
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data.csv"
THETAS = ROOT / "thetas.json"


def load_dataset():
    # solo train lee el csv. predict no tiene que ver esto
    # dos listas, misma posicion = mismo coche
    km = []
    prices = []
    with open(DATA) as f:
        for row in csv.DictReader(f):
            km.append(float(row["km"]))
            prices.append(float(row["price"]))
    return km, prices


def estimate_price(mileage, theta0, theta1):
    # theta0 = precio a 0 km. theta1 = lo que cambia por cada km
    # t1 ya es negativo, por eso se suma y no se resta
    return theta0 + theta1 * mileage


def load_thetas():
    # sin json = no hay train, volvemos a 0 y 0
    # ahi estimate_price da siempre 0, da igual los km
    if not THETAS.exists():
        return 0.0, 0.0
    with open(THETAS) as f:
        data = json.load(f)
    return data["theta0"], data["theta1"]


def save_thetas(theta0, theta1):
    # train termina y deja los 2 numeros para predict
    # a partir de aqui el csv ya no hace falta
    with open(THETAS, "w") as f:
        json.dump({"theta0": theta0, "theta1": theta1}, f)
