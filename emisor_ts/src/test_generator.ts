import fs from 'fs';
import path from 'path';
import hammingCode from "./hamming/hamming";
import fletcher16_emit from "./fletcher16/fletcher16";

/* =========================
 * Configuración de Pruebas
 * ========================= */

interface TestConfig {
  algorithms: string[];
  dataSizes: number[];
  errorProbabilities: number[];
  iterations: number;
  outputFile: string;
}

const TEST_CONFIG: TestConfig = {
  algorithms: ["hamming", "fletcher16"],
  dataSizes: [32, 64, 128, 256, 512],
  errorProbabilities: [0.0, 0.01, 0.02, 0.05, 0.1],
  iterations: 100, // 100 pruebas por configuración
  outputFile: "../tests/results/emisor_data.csv"
};

/* =========================
 * Utilidades
 * ========================= */

function generateRandomText(length: number): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function textToAsciiBits(text: string): string {
  let bits = "";
  for (const ch of text) {
    const code = ch.charCodeAt(0);
    bits += code.toString(2).padStart(8, "0").slice(-8);
  }
  return bits;
}

function addNoise(bits: string, errorProbability: number): { noisyBits: string; errorsIntroduced: number; positions: number[] } {
  const positions: number[] = [];
  let noisyBits = bits;
  let errorsIntroduced = 0;

  for (let i = 0; i < bits.length; i++) {
    if (Math.random() < errorProbability) {
      const bitArray = noisyBits.split('');
      bitArray[i] = bitArray[i] === '0' ? '1' : '0';
      noisyBits = bitArray.join('');
      errorsIntroduced++;
      positions.push(i);
    }
  }

  return { noisyBits, errorsIntroduced, positions };
}

function calculateOverhead(algorithm: string, dataSize: number): number {
  if (algorithm === "hamming") {
    let r = 0;
    while (Math.pow(2, r) < dataSize + r + 1) {
      r++;
    }
    return r / dataSize;
  } else if (algorithm === "fletcher16") {
    return 16 / dataSize;
  }
  return 0;
}

/* =========================
 * Datos del Emisor
 * ========================= */

interface EmisorData {
  testId: number;
  algorithm: string;
  dataSize: number;
  errorProbability: number;
  originalText: string;
  originalBits: string;
  encodedBits: string;
  encodedLength: number;
  noisyBits: string;
  errorsIntroduced: number;
  errorPositions: string;
  overhead: number;
  timestamp: number;
}

/* =========================
 * Generador de Datos
 * ========================= */

class DataGenerator {
  private data: EmisorData[] = [];
  private testCounter = 0;

  generateSingleTest(
    algorithm: string,
    dataSize: number,
    errorProbability: number
  ): EmisorData {
    this.testCounter++;

    // Generar texto aleatorio
    const charCount = Math.ceil(dataSize / 8);
    const originalText = generateRandomText(charCount);
    const originalBits = textToAsciiBits(originalText).slice(0, dataSize);
    
    // Aplicar algoritmo de codificación
    let encodedBits: string;
    if (algorithm === "hamming") {
      encodedBits = hammingCode(originalBits);
    } else {
      encodedBits = fletcher16_emit(originalBits);
    }

    // Aplicar ruido
    const { noisyBits, errorsIntroduced, positions } = addNoise(encodedBits, errorProbability);

    return {
      testId: this.testCounter,
      algorithm,
      dataSize,
      errorProbability,
      originalText,
      originalBits,
      encodedBits,
      encodedLength: encodedBits.length,
      noisyBits,
      errorsIntroduced,
      errorPositions: positions.join(';'),
      overhead: calculateOverhead(algorithm, dataSize),
      timestamp: Date.now()
    };
  }

  generateAllTests(): void {
    console.log(" Generando datos de prueba del emisor");

    const totalConfigurations = 
      TEST_CONFIG.algorithms.length *
      TEST_CONFIG.dataSizes.length *
      TEST_CONFIG.errorProbabilities.length;

    console.log(`📊 Configuraciones: ${totalConfigurations}`);
    console.log(`🔢 Pruebas por configuración: ${TEST_CONFIG.iterations}`);
    console.log(`📈 Total de pruebas: ${totalConfigurations * TEST_CONFIG.iterations}`);

    let configCounter = 0;

    for (const algorithm of TEST_CONFIG.algorithms) {
      for (const dataSize of TEST_CONFIG.dataSizes) {
        for (const errorProb of TEST_CONFIG.errorProbabilities) {
          configCounter++;
          
          console.log(`\n📦 Configuración ${configCounter}/${totalConfigurations}`);
          console.log(`   ${algorithm} | ${dataSize}b | ${(errorProb * 100).toFixed(1)}%`);

          for (let i = 0; i < TEST_CONFIG.iterations; i++) {
            const testData = this.generateSingleTest(algorithm, dataSize, errorProb);
            this.data.push(testData);

            if ((i + 1) % 25 === 0) {
              console.log(`   ✓ ${i + 1}/${TEST_CONFIG.iterations}`);
            }
          }
        }
      }
    }

    this.saveToCSV();
  }

  private saveToCSV(): void {
    // Crear directorio si no existe
    const outputPath = path.resolve(TEST_CONFIG.outputFile);
    const outputDir = path.dirname(outputPath);
    
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Headers del CSV
    const headers = [
      'testId',
      'algorithm', 
      'dataSize',
      'errorProbability',
      'originalText',
      'originalBits',
      'encodedBits',
      'encodedLength',
      'noisyBits',
      'errorsIntroduced',
      'errorPositions',
      'overhead',
      'timestamp'
    ];

    let csvContent = headers.join(',') + '\n';

    // Agregar datos
    for (const row of this.data) {
      const csvRow = [
        row.testId,
        row.algorithm,
        row.dataSize,
        row.errorProbability,
        `"${row.originalText.replace(/"/g, '""')}"`,
        `"${row.originalBits}"`,
        `"${row.encodedBits}"`,
        row.encodedLength,
        `"${row.noisyBits}"`,
        row.errorsIntroduced,
        `"${row.errorPositions}"`,
        row.overhead.toFixed(6),
        row.timestamp
      ];
      csvContent += csvRow.join(',') + '\n';
    }

    // Guardar archivo
    fs.writeFileSync(outputPath, csvContent);

    console.log(`\n✅ Datos guardados en: ${outputPath}`);
    console.log(`📊 Total de registros: ${this.data.length}`);
    
    this.printSummary();
  }

  private printSummary(): void {
    console.log('\n RESUMEN DE DATOS GENERADOS:');
    
    for (const algorithm of TEST_CONFIG.algorithms) {
      const algorithmData = this.data.filter(d => d.algorithm === algorithm);
      const avgOverhead = algorithmData.reduce((sum, d) => sum + d.overhead, 0) / algorithmData.length;
      const totalErrors = algorithmData.reduce((sum, d) => sum + d.errorsIntroduced, 0);
      
      console.log(`\n${algorithm.toUpperCase()}:`);
      console.log(`  Registros: ${algorithmData.length}`);
      console.log(`  Overhead promedio: ${(avgOverhead * 100).toFixed(2)}%`);
      console.log(`  Total errores introducidos: ${totalErrors}`);
    }

  }
}

function main() {
  try {
    console.log("Iniciando generador de datos de prueba");
    
    const generator = new DataGenerator();
    generator.generateAllTests();
    
    console.log("\n Generación de datos completada!");
    console.log("📁 Archivo CSV listo para procesamiento con Python");

  } catch (error) {
    console.error(" Error:", error);
    process.exit(1);
  }
}

main();