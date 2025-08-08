/**
 * Calcula cuantos bits de paridad se necesitan para k bits de datos 2^r ≥ k + r + 1
 */
function calculateParityBitsCount(k: number): number {
    let r = 0;
    while (Math.pow(2, r) < k + r + 1) {
        r++;
    }
    return r;
}

/**
 * Convierte una cadena de bits en un array de numeros
 */
function bitsStringToArray(str: string): number[] {
    return Array.from(str).map(ch => {
        if (ch !== '0' && ch !== '1') {
            throw new Error(`Carácter inválido para bit: "${ch}"`);
        }
        return ch === '1' ? 1 : 0;
    });
}

/**
 * Inserta marcadores en las posiciones de paridad y colocar los bits de datos en el resto de posiciones
 */
function insertParityPlaceholders(dataBits: number[]): number[] {
    const k = dataBits.length;
    const r = calculateParityBitsCount(k);
    console.log('Bits de paridad: ' + r)
    const totalLength = k + r;
    const encoded: number[] = [];
    let dataIndex = 0;

    for (let i = 1; i <= totalLength; i++) {
        if ((i & (i - 1)) === 0) {
            encoded.push(0);
        } else {
            encoded.push(dataBits[dataIndex++]);
        }
    }

    return encoded;
}


/**
 * Genera el código Hamming para detección y corrección de errores de un bit.
 * 
 * @param data - Cadena binaria de entrada (solo caracteres '0' y '1')
 * @returns Cadena binaria con bits de paridad de Hamming añadidos
 * 
 * @example
 * ```typescript
 * const original = "1011";
 * const encoded = hammingCode(original);
 * console.log(encoded); // Cadena con bits de paridad insertados
 * ```
 */
export default function hammingCode(data: string): string {
    const output = bitsStringToArray(data);
    console.log(insertParityPlaceholders(output))

    
    return data;
}