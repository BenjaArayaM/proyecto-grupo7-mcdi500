def detectar_atipicos_bucle(serie, limite_inferior, limite_superior):
    """
    Recorre los valores uno a uno y guarda aquellos
    que están fuera de los límites definidos por IQR.
    """
    atipicos = []

    for valor in serie:
        if valor < limite_inferior or valor > limite_superior:
            atipicos.append(valor)

    return atipicos


def detectar_atipicos_vectorizado(serie, limite_inferior, limite_superior):
    """
    Detecta valores atípicos mediante operaciones vectorizadas de pandas.
    """
    mascara = (serie < limite_inferior) | (serie > limite_superior)
    return serie[mascara].tolist()