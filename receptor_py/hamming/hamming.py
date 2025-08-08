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
    return data
