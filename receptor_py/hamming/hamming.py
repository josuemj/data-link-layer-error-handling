from typing import List

def get_parity_positions(n: int) -> List[int]:
    """
    Devuelve las posiciones (1-indexadas) de los bits de paridad
    para un bloque de longitud n: 1, 2, 4, 8, …
    """
    positions = []
    p = 1
    while p <= n:
        positions.append(p)
        p <<= 1
    return positions

def compute_erros(bits: List[int], parity_positions: List[int]) -> int:
    """
    Recalcula cada bit de paridad y construye el sindrome.
    El error es la suma de las posiciones de paridad que dieron paridad = 1.
    """
    n = len(bits)
    error = 0

    for p in parity_positions:
        parity = 0
        for i in range(p - 1, n, 2 * p):
            parity ^= sum(bits[i : i + p]) % 2
        if parity != 0:
            error += p

    return error

def hamming(data: str) -> str:
    """
    Procesa una cadena de bits codificada con el código de Hamming y determina 
    el estado del mensaje recibido según las reglas.

    Parámetros:
    -----------
    data : str
        Cadena de bits recibida desde el emisor (datos + bits de paridad Hamming).
        Ejemplo: "1011010"
    """
    print(f"Procesando mensaje Hamming (receptor): {data}")
    bits = [int(ch) for ch in data]
    n = len(bits)
    parity_positions = get_parity_positions(n)
    print('posiciones de los bits de paridad:', parity_positions)

    error = compute_erros(bits, parity_positions)

    if error == 0:
        print("No se detectaron errores.")
    else:
        print(f"Se detectó un error en la posición {error}.")

    return data
