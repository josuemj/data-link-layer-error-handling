from hamming.hamming import hamming
from fletcher16.fletcher16 import fletcher16_receive
from pathlib import Path

def main():
    print("=== RECEPTOR ===\n")
    
    # Mostrar opciones de algoritmos
    print("=== Seleccione el algoritmo de recepción ===")
    print("1. Hamming")
    print("2. Fletcher-16")
    
    # Validar selección del algoritmo
    algorithm = 0
    while True:
        try:
            algorithm = int(input("Ingrese su opción (1 o 2): "))
            if algorithm in [1, 2]:
                break
            else:
                print("Error: Ingrese 1 o 2. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un número válido (1 o 2). Intente nuevamente.")
    
    base_dir = Path(__file__).resolve().parent
    message_path = base_dir.parent / "tests" / "mensaje.txt"

    message = read_message(message_path)
    print(f"Mensaje recibido: {message}")

    # Procesar según el algoritmo seleccionado
    if algorithm == 1:
        print("\n=== Algoritmo Hamming seleccionado ===")
        hamming(message)
    elif algorithm == 2:
        print("\n=== Algoritmo Fletcher-16 seleccionado ===")
        fletcher16_receive(message)


def read_message(file_path: Path) -> str:
    """
    Lee un mensaje en binario desde un archivo de texto.
    `file_path` debe ser un objeto Path con la ruta completa.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        return file.read().strip()


main()