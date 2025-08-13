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
 * Convierte un array de bits en una cadena de caracteres
 */
function bitsArrayToString(bits: number[]): string {
    return bits
        .map(b => {
            if (b !== 0 && b !== 1) {
                throw new Error(`Valor inválido en array de bits: ${b}`);
            }
            return b.toString();
        })
        .join('');
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

function appendGlobalParity(encoded: number[]): string {
    // g = XOR de todos los bits actuales (paridad de todo el bloque)
    const g = encoded.reduce((acc, b) => acc ^ b, 0);
    encoded.push(g); // bit global al final
    return bitsArrayToString(encoded);
}

/**
 * Recorre cada posicion de paridad y calcula su valor haciendo paridad modulo 2 de los bloques que le corresponden
 */
function calculateParityBits(encoded: number[]): string {
    const n = encoded.length;

    // Encuentra todas las posiciones de paridad
    for (let pos = 1; pos <= n; pos <<= 1) {
        let parity = 0;

        // Empieza en pos-1, avanza en saltos de pos*2 y suma pos bits cada vez
        for (let i = pos - 1; i < n; i += pos * 2) {
            for (let j = i; j < i + pos && j < n; j++) {
                parity ^= encoded[j];
            }
        }

        // Escribe la paridad calculada
        encoded[pos - 1] = parity;
    }

    return bitsArrayToString(encoded);
}


/**
 * Genera el código Hamming para detección y corrección de errores de un bit.
 * 
 * @param data - Cadena binaria de entrada (solo caracteres '0' y '1')
 * @returns Cadena binaria con bits de paridad de Hamming añadidos
 * 
 */
export default function hammingCode(data: string): string {
    const output = bitsStringToArray(data);
    const withPlaceholders = insertParityPlaceholders(output);
    console.log('Posiciones con bits de paridad (en 0): ' + withPlaceholders)

    const newMessage = calculateParityBits(withPlaceholders)
    console.log('Nuevo mensaje: ' + newMessage)
    return appendGlobalParity(bitsStringToArray(newMessage));
}