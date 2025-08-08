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

def hamming(data: str) -> str:
    """
    Procesa una cadena de bits codificada con el código de Hamming y determina 
    el estado del mensaje recibido según las reglas.

    Parámetros:
    -----------
    data : str
        Cadena de bits recibida desde el emisor (datos + bits de paridad Hamming).
        Ejemplo: "1011010"

    Ejemplo de uso:
    ---------------
    >>> recibido = "1011010"
    >>> mensaje = hamming(recibido)
    # Posible salida en consola:
    # "No se detectaron errores. Mensaje original: 1011"
    # o
    # "Se detectó y corrigió un error en la posición 3. Mensaje corregido: 1001"
    # o
    # "Se detectaron errores no corregibles. Mensaje descartado."

    Notas:
    ------
    - El algoritmo asume que el mensaje fue codificado con Hamming por el emisor.
    - Aplicar Hamming sobre un mensaje que no fue codificado con este método 
      generará resultados inválidos.
    """
    print(f"Procesando mensaje Hamming (receptor): {data}")
    bits = [int(ch) for ch in data]
    n = len(bits)
    parity_positions = get_parity_positions(n)
    print('posiciones de los bits de paridad:', parity_positions)
    return data
