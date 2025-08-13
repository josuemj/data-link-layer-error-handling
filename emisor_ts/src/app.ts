import WebSocket from "ws";
import { createInterface } from "readline/promises";
import { stdin as input, stdout as output } from "node:process";
import hammingCode from './hamming/hamming'

/* =========================
 * Utilidades de presentación
 * ========================= */

// Convierte texto a binario ASCII (8 bits por caracter)
function textToAsciiBits(text: string): string {
  let bits = "";
  for (const ch of text) {
    const code = ch.charCodeAt(0); // ASCII
    bits += code.toString(2).padStart(8, "0").slice(-8);
  }
  return bits;
}

// Convierte string de bits a arreglo de bytes (números 0..255)
// Asume longitud múltiplo de 8; si no, hace padding a la derecha con ceros.
function bitsToBytes(bits: string): number[] {
  const pad = (8 - (bits.length % 8)) % 8;
  const padded = bits + "0".repeat(pad);
  const out: number[] = [];
  for (let i = 0; i < padded.length; i += 8) {
    out.push(parseInt(padded.slice(i, i + 8), 2));
  }
  return out;
}

// Convierte número a binario fijo de n bits
function toBits(n: number, width: number): string {
  return (n >>> 0).toString(2).padStart(width, "0").slice(-width);
}

/* =========================
 * Algoritmos de Enlace
 * ========================= */

type Algo = "hamming" | "fletcher16";

function normalizeAlgo(a: string): Algo {
  const x = (a || "").trim().toLowerCase();
  if (x === "hamming" || x === "fletcher16") return x;
  return "hamming";
}
/* =========================
 * Main (CLI + WebSocket)
 * ========================= */

async function main() {
  const rl = createInterface({ input, output });

  try {
    console.log("=== Emisor (WS) - Capa de Enlace ===");
    console.log("Bienvenido. Este emisor toma tu mensaje, lo codifica y lo envía por WebSocket.\n");

    // Algoritmo
    const algoAns = await rl.question("¿Algoritmo? (hamming | fletcher16) [hamming]: ");
    const algorithm: Algo = normalizeAlgo(algoAns);
    console.log(`Algoritmo seleccionado: ${algorithm}`);

    // Mensaje
    const userText = await rl.question("Escribe el mensaje (texto libre): ");
    if (!userText.trim()) {
      console.error("Mensaje vacío. Saliendo.");
      process.exit(1);
    }

    // Texto -> bits ASCII
    const payloadBits = textToAsciiBits(userText);
    console.log(`\nASCII (bits):\n${payloadBits}\n`);

    // Aplicar algoritmo
    let encoded: string;
    if (algorithm === "hamming") {
      //TODO
      encoded = hammingCode(payloadBits);
    } else {
      //TODO
      encoded = '000';
    }

    // Payload solicitado
    const payload = {
      algorithm,
      message: encoded,
    };

    console.log("\nPayload a enviar:");
    console.log(JSON.stringify(payload, null, 2));

    // Enviar por WebSocket
    const WS_URL = process.env.WS_URL || "ws://localhost:8765";
    console.log(`\nConectando a ${WS_URL} ...`);
    const ws = new WebSocket(WS_URL);

    ws.on("open", () => {
      console.log("Conexión establecida. Enviando payload...");
      ws.send(JSON.stringify(payload));
    });

    ws.on("message", (data: any) => {
      try {
        const resp = JSON.parse(data.toString());
        console.log("\nRespuesta del receptor:");
        console.log(JSON.stringify(resp, null, 2));
      } catch {
        console.log("\nRespuesta del receptor (texto):");
        console.log(data.toString());
      } finally {
        ws.close();
      }
    });

    ws.on("error", (err: any) => {
      console.error("WS error:", err);
    });

    ws.on("close", () => {
      console.log("Conexión cerrada.");
      rl.close();
    });
  } catch (e) {
    console.error("Error:", e);
    process.exit(1);
  }
}

main();
