# Entrada: cadena binaria = datos + 16 bits de checksum
# Salida: imprime según enunciado y devuelve el mensaje "limpio" (sin checksum) si procede

def _bin_to_bytes(bits: str):
    pad = (8 - (len(bits) % 8)) % 8
    padded = bits + ("0" * pad)
    return [int(padded[i:i+8], 2) for i in range(0, len(padded), 8)]

def _fletcher16_compute(data_bits: str) -> int:
    bytes_ = _bin_to_bytes(data_bits)
    sum1 = 0
    sum2 = 0
    for b in bytes_:
        sum1 = (sum1 + b) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1  # 16-bit checksum

def fletcher16_receive(frame_bits: str) -> str | None:
    if len(frame_bits) < 16:
        print("Se detectaron errores: trama demasiado corta. Mensaje descartado.")
        return None

    data_bits = frame_bits[:-16]
    recv_ck_bits = frame_bits[-16:]
    recv_ck = int(recv_ck_bits, 2)

    calc_ck = _fletcher16_compute(data_bits)

    if calc_ck == recv_ck:
        # Sin errores: mostrar mensaje original (sin checksum)
        print(f"No se detectaron errores. Mensaje original: {data_bits}")
        return data_bits
    else:
        # Fletcher-16 SOLO detecta, no corrige
        print("Se detectaron errores: checksum no coincide. Mensaje descartado.")
        return None
