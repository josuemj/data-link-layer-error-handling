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
    Recalcula cada bit de paridad y construye el error.
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

def correct_error(bits: List[int], error: int) -> None:
    """
    Invierte el bit en la posicion indicada por el error
    Retorna una tupla (bit_original, bit_corregido)
    """
    id = error - 1
    original = bits[id]
    bits[id] ^= 1
    corrected = bits[id]
    return original, corrected

def extract_data(bits: List[int], parity_positions: List[int]) -> List[int]:
    """
    Extrae solo los bits de datos (omitiendo las posiciones de paridad)
    """
    return [bits[i] for i in range(len(bits)) if (i + 1) not in parity_positions]

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
        print(f"Se detecto un error en la posicion {error}.")
        original, corrected = correct_error(bits, error)
        print(f"El bit en la posicion {error} cambio de {original} a {corrected}.")
        corrected_msg = ''.join(str(b) for b in bits)
        print(f"Mensaje corregido completo: {corrected_msg}")

    data_bits = extract_data(bits, parity_positions)
    data = ''.join(str(b) for b in data_bits)
    print('Mensaje original: ', data)
    return data
