import * as readlineSync from 'readline-sync';
import hammingCode from './src/hamming/hamming';
import todo from './src/todo/todo';
import setMessage from './src/utils/utils';

function main(): void {
    console.log('=== EMISOR ===\n');
    
    // Pedir cadena binaria
    let binaryString: string = '';
    while (true) {
        binaryString = readlineSync.question('Ingrese la cadena de binario: ');
        
        // Validar que solo contenga 0s y 1s
        if (/^[01]+$/.test(binaryString)) {
            break;
        } else {
            console.log('Error: La cadena debe contener solo 0s y 1s. Intente nuevamente.');
        }
    }
    
    console.log(`\nCadena binaria ingresada: ${binaryString}`);
    
    //  opciones de algoritmos
    console.log('\n=== Seleccione el algoritmo ===');
    console.log('1. Hamming');
    console.log('2. (Por implementar)');
    
    let algorithm: number = 0;
    while (true) {
        const input = readlineSync.question('Ingrese su opción (1 o 2): ');
        algorithm = parseInt(input);
        
        if (algorithm === 1 || algorithm === 2) {
            break;
        } else {
            console.log('Error: Ingrese 1 o 2. Intente nuevamente.');
        }
    }
    
    // Procesar según el algoritmo seleccionado
    switch (algorithm) {
        case 1:
            console.log('\n=== Algoritmo Hamming seleccionado ===');
            const hammingResult = hammingCode(binaryString);
            setMessage('../tests/mensaje.txt', hammingResult);
            break;
        case 2:
            console.log('\n=== Algoritmo TODO seleccionado ===');
            const todoResult = todo(binaryString);
            setMessage('../tests/mensaje.txt', todoResult);
            break;
    }
}

main();
