import numpy as np

def filtro_edo(rate, data, a):
    dt = 1 / rate
    y = np.zeros(len(data))

    # hacer más fuerte el efecto del slider
    alpha = a * 5  # multiplica el impacto

    for i in range(1, len(data)):
        y[i] = y[i-1] + dt * (data[i] - alpha * y[i-1])

    return y

def filtro_euler_mejorado(rate, data, a=1):
    """
    Filtro usando Euler mejorado (Heun)
    
    rate: frecuencia de muestreo
    data: señal de entrada (audio)
    a: nivel de filtro
    """

    y = np.zeros(len(data))
    alpha = a / (a + 1)

    for i in range(1, len(data)):
        # pendiente inicial
        f1 = data[i-1] - y[i-1]

        # predicción
        y_pred = y[i-1] + f1

        # pendiente corregida
        f2 = data[i] - y_pred

        # corrección (más estable)
        y[i] = y[i-1] + (alpha * 0.5) * (f1 + f2)

    return y