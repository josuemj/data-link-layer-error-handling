import * as fs from 'fs';
import * as path from 'path';

/**
 * Escribe un mensaje en un archivo, sobrescribiendo el contenido existente.
 * Si el directorio no existe, lo crea.
 * 
 * @param filePath - Ruta completa del archivo donde se escribirá el mensaje
 * @param message - Contenido de texto que se escribirá en el archivo
 * 
 * @throws {Error} - Lanza error si no se puede crear el directorio o escribir el archivo
 * 
 * @example
 * ```typescript
 * // Escribir en un archivo existente
 * setMessage('./output/result.txt', 'Contenido del mensaje');
 * 
 * // Crear directorio y archivo si no existen
 * setMessage('./nueva_carpeta/archivo.txt', 'Mensaje en nuevo archivo');
 * ```
 * 
 * @remarks
 * - Sobrescribe completamente el contenido del archivo si ya existe
 * - Crea automáticamente los directorios padre necesarios
 * - Utiliza codificación UTF-8 para la escritura
 * - Muestra confirmación en consola cuando la operación es exitosa
 */
export default function setMessage(filePath: string, message: string): void {
    try {
        // Crear directorio si no existe
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        
        // Escribir el mensaje al archivo (sobrescribe contenido existente)
        fs.writeFileSync(filePath, message, 'utf8');
        console.log(`Mensaje escrito exitosamente en: ${filePath}`);
    } catch (error) {
        console.error(`Error al escribir archivo: ${error}`);
        throw error;
    }
}