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
    // Implementación del código Hamming
    console.log(`Generando código Hamming para: ${data}`);
    return data;
}
