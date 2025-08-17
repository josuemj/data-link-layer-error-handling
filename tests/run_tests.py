import asyncio
import subprocess
import time
import os
import sys

async def main():
    print(" INICIANDO PRUEBAS AUTOMATIZADAS")
    print("=" * 40)
    
    # Verificar estructura
    if not os.path.exists("config/test_config.yaml"):
        print("❌ Error: Falta archivo de configuración")
        return
    
    # Instalar dependencias
    print(" Instalando dependencias...")
    
    # Crear directorios
    os.makedirs("results/raw_data", exist_ok=True)
    os.makedirs("results/graphs", exist_ok=True)
    os.makedirs("results/reports", exist_ok=True)
    
    # Iniciar receptor
    print(" Iniciando receptor...")
    receptor_process = subprocess.Popen([
        sys.executable, "../receptor_py/app.py"
    ])
    
    # Esperar que inicie
    print(" Esperando receptor...")
    time.sleep(5)
    
    try:
        # Ejecutar pruebas
        print(" Ejecutando pruebas...")
        subprocess.run([sys.executable, "automation/test_runner.py"])
        
        # Generar análisis
        print(" Generando análisis...")
        subprocess.run([sys.executable, "automation/statistics_analyzer.py"])
        
        print("\n✅ PRUEBAS COMPLETADAS")
        print(" Resultados en tests/results/")
        
    finally:
        # Terminar receptor
        print(" Cerrando receptor...")
        receptor_process.terminate()

if __name__ == "__main__":
    asyncio.run(main())