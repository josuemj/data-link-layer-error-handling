from hamming.hamming import hamming

def main():
    print("=== RECEPTOR ===\n")
    
    # Mostrar opciones de algoritmos
    print("=== Seleccione el algoritmo de recepción ===")
    print("1. Hamming")
    print("2. TODO (Por implementar)")
    
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
    
    # Procesar según el algoritmo seleccionado
    if algorithm == 1:
        print("\n=== Algoritmo Hamming seleccionado ===")
        hamming("sd")
    elif algorithm == 2:
        print("\n=== Algoritmo TODO seleccionado ===")
