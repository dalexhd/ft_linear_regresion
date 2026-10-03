from src.regression import estimate_price, load_dataset, save_thetas


# 0.1 y 1000 van bien con km en 0-1. crudos se va a la mierda
LR = 0.1
EPOCHS = 1000


def scale_km(mileages):
    # 240000 * error revienta tmp1. de 0 a 1 ya no
    # el que menos km tiene queda en 0, el que mas en 1
    lo = min(mileages)
    hi = max(mileages)
    span = hi - lo
    return [(x - lo) / span for x in mileages], lo, span


def to_raw_thetas(theta0, theta1, lo, span):
    # el descent vio km 0-1. predict recibe km de verdad
    # si no deshago esto, 150000 entra como si fuera 150000 veces 1
    return theta0 - theta1 * lo / span, theta1 / span


def train(mileages, prices):
    # empiezo en 0 y 0, como si no hubiera visto ningun coche
    xs, lo, span = scale_km(mileages)
    theta0 = 0.0
    theta1 = 0.0
    m = len(prices)

    for _ in range(EPOCHS):
        # los dos tmp con los theta de ahora, luego se restan a la vez
        # si actualizo uno ya, el otro se calcula con otra recta
        sum0 = 0.0
        sum1 = 0.0
        for i in range(m):
            # predicho - real. negativo = me quede corto, hay que subir
            err = estimate_price(xs[i], theta0, theta1) - prices[i]
            sum0 += err
            # el de muchos km tira mas de la pendiente
            sum1 += err * xs[i]
        tmp0 = LR * sum0 / m
        tmp1 = LR * sum1 / m
        theta0 -= tmp0
        theta1 -= tmp1

    return to_raw_thetas(theta0, theta1, lo, span)


def main():
    # csv -> aprende -> json
    km, prices = load_dataset()
    theta0, theta1 = train(km, prices)
    save_thetas(theta0, theta1)
    print("theta0:", theta0)
    print("theta1:", theta1)


if __name__ == "__main__":
    main()
