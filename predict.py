from src.regression import estimate_price, load_thetas


def ask_mileage():
    # input siempre es texto, hay que pasarlo a numero
    raw = input("km: ")
    return float(raw)


def main():
    # no abre el csv. solo los 2 numeros que dejo train
    theta0, theta1 = load_thetas()
    print("theta0:", theta0)
    print("theta1:", theta1)
    mileage = ask_mileage()
    price = estimate_price(mileage, theta0, theta1)
    print("precio:", price)


if __name__ == "__main__":
    main()
