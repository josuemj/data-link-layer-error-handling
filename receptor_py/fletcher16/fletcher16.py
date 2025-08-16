# Entrada: cadena binaria = datos + 16 bits de checksum
# Salida: imprime según enunciado y devuelve el mensaje "limpio" (sin checksum) si procede

def _bin_to_bytes(bits: str):
    pad = (8 - (len(bits) % 8)) % 8
    padded = bits + ("0" * pad)
    return [int(padded[i:i+8], 2) for i in range(0, len(padded), 8)]

def bin_to_bytes(bits: str) -> list[int]:
    """Convierte cadena binaria a lista de bytes"""
    # Pad a múltiplos de 8
    pad = (8 - (len(bits) % 8)) % 8
    padded = bits + "0" * pad
    bytes_list = []
    for i in range(0, len(padded), 8):
        bytes_list.append(int(padded[i:i+8], 2))
    return bytes_list

def _fletcher16_compute(data_bits: str) -> int:
    bytes_ = _bin_to_bytes(data_bits)
    sum1 = 0
    sum2 = 0
    for b in bytes_:
        sum1 = (sum1 + b) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1  # 16-bit checksum

def fletcher16_receive(frame: str) -> str:
    """
    Verifica y decodifica una trama Fletcher-16.
    
    Args:
        frame: Cadena binaria con datos + checksum de 16 bits
        
    Returns:
        str: Datos originales si la verificación es correcta
        
    Raises:
        ValueError: Si hay error en el checksum
    """
    if len(frame) < 16:
        raise ValueError("Trama muy corta para Fletcher-16")
    
    # Separar datos y checksum
    data_bits = frame[:-16]
    received_checksum = int(frame[-16:], 2)
    
    print(f"Datos recibidos: {data_bits}")
    print(f"Checksum recibido: {received_checksum:016b} ({received_checksum})")
    
    # Calcular checksum de los datos recibidos
    bytes_data = bin_to_bytes(data_bits)
    sum1 = 0
    sum2 = 0
    
    for b in bytes_data:
        sum1 = (sum1 + b) % 255
        sum2 = (sum2 + sum1) % 255
    
    calculated_checksum = (sum2 << 8) | sum1
    
    print(f"Checksum calculado: {calculated_checksum:016b} ({calculated_checksum})")
    
    # Verificar integridad
    if received_checksum == calculated_checksum:
        print("✓ Verificación Fletcher-16 exitosa - No hay errores detectados")
        return data_bits
    else:
        error_msg = f"✗ Error Fletcher-16 detectado - Checksum no coincide"
        print(error_msg)
        raise ValueError(error_msg)