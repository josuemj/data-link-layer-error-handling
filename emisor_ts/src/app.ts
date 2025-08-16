import WebSocket from "ws";
import { createInterface } from "readline/promises";
import { stdin as input, stdout as output } from "node:process";
import hammingCode from "./hamming/hamming";
import fletcher16_emit from "./fletcher16/fletcher16";

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

/* =========================
 * Ruido (voltear K bits)
 * ========================= */

function flipAt(s: string, i: number): string {
  const arr = s.split("");
  arr[i] = arr[i] === "0" ? "1" : "0";
  return arr.join("");
}

/** Devuelve { noised, positions } con K índices únicos aleatorios [0..len-1] */
function addNoiseKFlips(bits: string, k: number): { noised: string; positions: number[] } {
  const n = bits.length;
  if (k <= 0) return { noised: bits, positions: [] };
  if (k > n) throw new Error(`k=${k} excede longitud (${n})`);

  const positions: number[] = [];
  const picked = new Set<number>();
  while (positions.length < k) {
    const idx = Math.floor(Math.random() * n);
    if (!picked.has(idx)) {
      picked.add(idx);
      positions.push(idx);
    }
  }
  positions.sort((a, b) => a - b);

  let out = bits;
  for (const p of positions) out = flipAt(out, p);
  return { noised: out, positions };
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
      encoded = hammingCode(payloadBits);
    } else {
      
      encoded = fletcher16_emit(payloadBits);
    }

    // ¿Agregar ruido?
    const noiseAns = (await rl.question("¿Agregar ruido? (s/n) [n]: ")).trim().toLowerCase();
    let finalBits = encoded;
    let noiseMeta: { enabled: boolean; flips: number; positions: number[] } = {
      enabled: false,
      flips: 0,
      positions: [],
    };

    if (noiseAns === "s" || noiseAns === "si" || noiseAns === "sí") {
      const max = encoded.length;
      let kStr = await rl.question(`¿Cuántos bits voltear? (1..${max}): `);
      let k = parseInt(kStr, 10);
      if (!Number.isFinite(k) || k < 1 || k > max) {
        console.error(`Valor inválido: ${kStr}. Debe estar entre 1 y ${max}. Saliendo.`);
        process.exit(1);
      }

      const { noised, positions } = addNoiseKFlips(encoded, k);
      finalBits = noised;
      noiseMeta = { enabled: true, flips: k, positions };
      console.log(`\nRuido aplicado: ${k} bit(s) volteado(s) en posiciones (0-based): ${positions.join(", ")}`);
    }

    // Payload solicitado
    const payload = {
      algorithm,
      message: finalBits,
      meta: {
        original_len: encoded.length,
        noise: noiseMeta,
      },
    };

    console.log("\nPayload a enviar:");
    console.log(JSON.stringify(payload, null, 2));

    // Enviar por WebSocket
    const WS_URL = process.env.WS_URL || "ws://0.0.0.0:8765";
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
