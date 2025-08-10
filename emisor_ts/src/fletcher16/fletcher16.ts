// emisor_ts/fletcher.ts
// Entrada: cadena binaria "110101..." (cualquier longitud)
// Salida: trama = datos + checksum de 16 bits (como binario)

function binToBytes(bits: string): number[] {
  // pad a múltiplos de 8
  const pad = (8 - (bits.length % 8)) % 8;
  const padded = bits + "0".repeat(pad);
  const bytes: number[] = [];
  for (let i = 0; i < padded.length; i += 8) {
    bytes.push(parseInt(padded.slice(i, i + 8), 2));
  }
  return bytes;
}

export default function fletcher16_emit(dataBits: string): string {
  const bytes = binToBytes(dataBits);
  let sum1 = 0;
  let sum2 = 0;
  for (const b of bytes) {
    sum1 = (sum1 + b) % 255;
    sum2 = (sum2 + sum1) % 255;
  }
  const checksum = (sum2 << 8) | sum1; // 16 bits
  const checksumBits = checksum.toString(2).padStart(16, "0");
  return dataBits + checksumBits; // concatenado como pide el enunciado
}

// Ejemplo de uso (npx ts-node):
// const trama = fletcher16_emit("1001");
// console.log(trama); // datos + 16 bits de checksum
