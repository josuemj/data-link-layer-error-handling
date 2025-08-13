import os
import json
import asyncio
import websockets
from hamming.hamming import hamming



# -------- utilidades ----------
def bits_to_text(bits: str) -> str:
    if not bits:
        return ""
    if any(c not in "01" for c in bits):
        raise ValueError("Bits inválidos")
    usable = (len(bits) // 8) * 8
    bits = bits[:usable]
    return "".join(chr(int(bits[i:i+8], 2)) for i in range(0, usable, 8))

# =========================
# WebSocket Server
# =========================

async def handler(ws):
    async for message in ws:
        try:
            frame = json.loads(message)
            if not isinstance(frame, dict):
                await ws.send(json.dumps({"status": "error", "reason": "Payload inválido (no es JSON de objeto)"}))
                continue

            algorithm = (frame.get("algorithm") or "").strip().lower()
            bitstream = frame.get("message") or ""

            if not algorithm or not bitstream:
                await ws.send(json.dumps({
                    "status": "error",
                    "reason": "Faltan campos: 'algorithm' y/o 'message'"
                }))
                continue

            print("\n--- Mensaje recibido ---")
            print(f"Algoritmo: {algorithm}")
            print(f"Bits (len={len(bitstream)}): {bitstream[:80]}{'...' if len(bitstream)>80 else ''}")

            if algorithm == "hamming":
                # Tu función hamming() retorna un string con los bits de datos decodificados
                data_bits = hamming(bitstream)
                try:
                    decoded_text = bits_to_text(data_bits)
                except Exception as e:
                    await ws.send(json.dumps({
                        "status": "error",
                        "algorithm": algorithm,
                        "reason": f"Error al convertir a ASCII: {e}"
                    }))
                    continue

                print("Texto decodificado:")
                print(decoded_text if decoded_text else "(vacío)")

                await ws.send(json.dumps({
                    "status": "ok",
                    "algorithm": algorithm,
                    "decoded_text": decoded_text,
                    "details": {
                        "decoded_bits": data_bits,
                        "input_len": len(bitstream),
                        "output_len": len(data_bits)
                    }
                }))

            elif algorithm == "fletcher16":
                # TODO: implementar verificación/decodificación Fletcher-16
                await ws.send(json.dumps({
                    "status": "error",
                    "algorithm": algorithm,
                    "reason": "Fletcher-16: TODO (no implementado)"
                }))

            else:
                await ws.send(json.dumps({
                    "status": "error",
                    "reason": f"Algoritmo no soportado: {algorithm}"
                }))

        except Exception as e:
            await ws.send(json.dumps({
                "status": "error",
                "reason": f"Excepción en servidor: {str(e)}"
            }))

async def main():
    host = os.getenv("WS_HOST", "0.0.0.0")
    port = int(os.getenv("WS_PORT", "8765"))
    async with websockets.serve(handler, host, port):
        print(f"Receptor WS listo en ws://{host}:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
