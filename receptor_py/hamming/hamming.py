from typing import List, Tuple

USE_SECDED = True

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
    Recalcula cada bit de paridad y construye el error (síndrome).
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

def _failing_parities(bits: List[int], parity_positions: List[int]) -> List[int]:
    """Lista de posiciones de paridad que fallan (para reportar)."""
    n = len(bits)
    fails = []
    for p in parity_positions:
        parity = 0
        for i in range(p - 1, n, 2 * p):
            parity ^= sum(bits[i : i + p]) % 2
        if parity != 0:
            fails.append(p)
    return fails

def correct_error(bits: List[int], error: int) -> Tuple[int, int]:
    """
    Invierte el bit en la posicion indicada por el error
    Retorna (bit_original, bit_corregido)
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

def _overall_parity(bits: List[int]) -> int:
    """XOR de todos los bits (0=par, 1=impar)."""
    return sum(bits) & 1

def _candidate_pairs_for_double_error(syndrome: int, n_code: int) -> List[Tuple[int, int]]:
    """
    Todas las parejas (i,j) con i<j y i ^ j == síndrome, 1 ≤ i,j ≤ n_code.
    Estas son las posibles posiciones si asumimos EXACTAMENTE 2 errores en code_bits.
    """
    pairs = []
    for i in range(1, n_code + 1):
        j = i ^ syndrome
        if 1 <= j <= n_code and i < j:
            pairs.append((i, j))
    return pairs

def hamming(data: str) -> str:
    print(f"Procesando mensaje Hamming (receptor): {data}")
    bits_all = [int(ch) for ch in data]
    n_all = len(bits_all)

    if USE_SECDED:
        code_bits = bits_all[:-1]
        global_pos = n_all
        parity_positions = get_parity_positions(len(code_bits))
        print('posiciones de los bits de paridad:', parity_positions, '(con paridad global al final)')

        syndrome = compute_erros(code_bits, parity_positions)
        gpar = _overall_parity(bits_all)

        errores = []

        if syndrome == 0 and gpar == 0:
            print("No se detectaron errores.")
        elif syndrome == 0 and gpar == 1:
            errores.append((bits_all[-1], global_pos))
        elif syndrome != 0 and gpar == 1:
            original, _ = correct_error(code_bits, syndrome)
            errores.append((original, syndrome))
        else:  # múltiples errores
            pairs = _candidate_pairs_for_double_error(syndrome, len(code_bits))
            for i, j in pairs:
                errores.append((code_bits[i-1], i))
                errores.append((code_bits[j-1], j))
            if 1 <= syndrome <= len(code_bits):
                errores.append((code_bits[syndrome-1], syndrome))
                errores.append((bits_all[-1], global_pos))

        if errores:
            print(f"errores: {len(errores)}")
            for bit, pos in errores:
                print(f"{bit},{pos}")

        data_bits = extract_data(code_bits, parity_positions)
        print('Mensaje original: ', ''.join(str(b) for b in data_bits))
        return ''.join(str(b) for b in data_bits)

    else:
        parity_positions = get_parity_positions(n_all)
        print('posiciones de los bits de paridad:', parity_positions, '(sin paridad global)')

        fails = _failing_parities(bits_all, parity_positions)
        syndrome = sum(fails)
        errores = []

        if syndrome == 0:
            print("No se detectaron errores.")
        else:
            if len(fails) >= 2:
                pairs = _candidate_pairs_for_double_error(syndrome, n_all)
                for i, j in pairs:
                    errores.append((bits_all[i-1], i))
                    errores.append((bits_all[j-1], j))
            else:
                original, _ = correct_error(bits_all, syndrome)
                errores.append((original, syndrome))

        if errores:
            print(f"errores: {len(errores)}")
            for bit, pos in errores:
                print(f"{bit},{pos}")

        data_bits = extract_data(bits_all, parity_positions)
        print('Mensaje original: ', ''.join(str(b) for b in data_bits))
        return ''.join(str(b) for b in data_bits)
