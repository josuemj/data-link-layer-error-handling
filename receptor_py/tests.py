import pandas as pd
import os
import sys
import time
from typing import Tuple, Optional

# Agregar la ruta del receptor para importar los módulos

try:
    from hamming.hamming import hamming
    from fletcher16.fletcher16 import fletcher16_receive
except ImportError as e:
    print(f" Error importando módulos del receptor: {e}")
    print("   Asegúrate de que los módulos estén en ../receptor_py/")
    sys.exit(1)

class ReceptorProcessor:
    def __init__(self, input_csv: str, output_csv: str):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.results = []
        
    def load_emisor_data(self) -> pd.DataFrame:
        """Carga los datos generados por el emisor"""
        try:
            df = pd.read_csv(self.input_csv)
            print(f" Datos del emisor cargados: {len(df)} registros")
            return df
        except FileNotFoundError:
            print(f"❌ No se encontró el archivo: {self.input_csv}")
            print("   Primero ejecuta: tsx test_generator.ts")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error cargando CSV: {e}")
            sys.exit(1)
    
    def process_hamming(self, noisy_bits: str) -> Tuple[bool, bool, str, str]:
        """
        Procesa con algoritmo Hamming
        Returns: (detected, corrected, status, message)
        """
        try:
            # Intentar decodificar con Hamming
            decoded_bits = hamming(noisy_bits)
            
            # Si llega aquí, Hamming pudo corregir o no había errores
            return False, True, "ok", "Hamming: Decodificación exitosa"
            
        except Exception as e:
            # Hamming detectó un error que no puede corregir
            error_msg = str(e)
            return True, False, "error", f"Hamming: {error_msg}"
    
    def process_fletcher16(self, noisy_bits: str) -> Tuple[bool, bool, str, str]:
        """
        Procesa con algoritmo Fletcher-16
        Returns: (detected, corrected, status, message)
        """
        try:
            # Intentar verificar con Fletcher-16
            decoded_bits = fletcher16_receive(noisy_bits)
            
            # Si llega aquí, Fletcher-16 no detectó errores
            return False, False, "ok", "Fletcher-16: Verificación exitosa"
            
        except Exception as e:
            # Fletcher-16 detectó un error
            error_msg = str(e)
            return True, False, "error", f"Fletcher-16: {error_msg}"
    
    def process_single_test(self, row: pd.Series) -> dict:
        """Procesa una sola prueba con el receptor correspondiente"""
        
        test_id = row['testId']
        algorithm = row['algorithm']
        noisy_bits = row['noisyBits']
        errors_introduced = row['errorsIntroduced']
        
        start_time = time.time()
        
        # Procesar según el algoritmo
        if algorithm == 'hamming':
            detected, corrected, status, message = self.process_hamming(noisy_bits)
        elif algorithm == 'fletcher16':
            detected, corrected, status, message = self.process_fletcher16(noisy_bits)
        else:
            detected, corrected, status, message = False, False, "error", f"Algoritmo desconocido: {algorithm}"
        
        processing_time = (time.time() - start_time) * 1000  # En milisegundos
        
        # Determinar si la detección fue correcta
        if errors_introduced > 0:
            # Había errores: debería haber sido detectado
            correct_detection = detected
        else:
            # No había errores: no debería haber sido detectado
            correct_detection = not detected
        
        # Determinar si la corrección fue correcta (solo para Hamming)
        if algorithm == 'hamming' and errors_introduced > 0:
            # Si había errores y Hamming dice que corrigió, verificamos
            correct_correction = corrected
        else:
            correct_correction = False  # Fletcher no corrige
        
        return {
            'testId': test_id,
            'algorithm': algorithm,
            'dataSize': row['dataSize'],
            'errorProbability': row['errorProbability'],
            'originalText': row['originalText'],
            'originalBits': row['originalBits'],
            'encodedBits': row['encodedBits'],
            'noisyBits': noisy_bits,
            'errorsIntroduced': errors_introduced,
            'errorPositions': row['errorPositions'],
            'overhead': row['overhead'],
            # Resultados del receptor
            'detected': detected,
            'corrected': corrected,
            'correctDetection': correct_detection,
            'correctCorrection': correct_correction,
            'processingTime': round(processing_time, 3),
            'status': status,
            'message': message,
            'timestamp': int(time.time())
        }
    
    def process_all_tests(self):
        """Procesa todas las pruebas del CSV del emisor"""
        
        print("🔄 Iniciando procesamiento con algoritmos del receptor")
        print("=" * 60)
        
        # Cargar datos del emisor
        df = self.load_emisor_data()
        
        total_tests = len(df)
        processed = 0
        errors = 0
        
        print(f"📈 Total de pruebas a procesar: {total_tests}")
        print()
        
        # Procesar cada prueba
        for index, row in df.iterrows():
            try:
                result = self.process_single_test(row)
                self.results.append(result)
                processed += 1
                
                # Mostrar progreso cada 100 pruebas
                if processed % 100 == 0:
                    print(f"   ✅ Procesadas: {processed}/{total_tests} ({(processed/total_tests)*100:.1f}%)")
                
            except Exception as e:
                errors += 1
                print(f"   ❌ Error en prueba {row['testId']}: {e}")
        
        print(f"\n📊 Procesamiento completado:")
        print(f"   ✅ Exitosas: {processed}")
        print(f"   ❌ Errores: {errors}")
        
        # Guardar resultados
        self.save_results()
    
    def save_results(self):
        """Guarda los resultados en CSV"""
        
        if not self.results:
            print("❌ No hay resultados para guardar")
            return
        
        # Crear directorio si no existe
        output_dir = os.path.dirname(self.output_csv)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Convertir a DataFrame y guardar
        results_df = pd.DataFrame(self.results)
        results_df.to_csv(self.output_csv, index=False)
        
        print(f"\n💾 Resultados guardados en: {self.output_csv}")
        print(f"📊 Total de registros: {len(self.results)}")
        
        # Generar resumen
        self.generate_summary(results_df)
    
    def generate_summary(self, df: pd.DataFrame):
        """Genera resumen estadístico de los resultados"""
        
        print("\n📈 RESUMEN DE RESULTADOS DEL RECEPTOR:")
        print("=" * 50)
        
        for algorithm in df['algorithm'].unique():
            algo_data = df[df['algorithm'] == algorithm]
            
            # Estadísticas de detección
            total_tests = len(algo_data)
            correct_detections = algo_data['correctDetection'].sum()
            detection_rate = (correct_detections / total_tests) * 100
            
            # Estadísticas de corrección (solo para Hamming)
            if algorithm == 'hamming':
                corrections = algo_data['corrected'].sum()
                correction_rate = (corrections / total_tests) * 100
            else:
                correction_rate = 0
            
            # Tiempo promedio
            avg_time = algo_data['processingTime'].mean()
            
            # Errores por probabilidad
            error_stats = algo_data.groupby('errorProbability').agg({
                'correctDetection': 'mean',
                'errorsIntroduced': 'sum'
            }).round(3)
            
            print(f"\n🔍 {algorithm.upper()}:")
            print(f"   Total de pruebas: {total_tests}")
            print(f"   Detección correcta: {detection_rate:.1f}% ({correct_detections}/{total_tests})")
            print(f"   Tasa de corrección: {correction_rate:.1f}%")
            print(f"   Tiempo promedio: {avg_time:.2f} ms")
            print(f"   Overhead promedio: {algo_data['overhead'].mean()*100:.2f}%")
            
            print(f"\n   📊 Por probabilidad de error:")
            for error_prob, stats in error_stats.iterrows():
                print(f"      {error_prob*100:4.1f}%: {stats['correctDetection']*100:5.1f}% detección correcta")
        
        # Comparación general
        print(f"\n🏆 COMPARACIÓN GENERAL:")
        comparison = df.groupby('algorithm').agg({
            'correctDetection': 'mean',
            'corrected': 'mean',
            'processingTime': 'mean',
            'overhead': 'mean'
        }).round(4)
        
        print(comparison)
        
        # Mejores algoritmos
        best_detection = comparison['correctDetection'].idxmax()
        fastest = comparison['processingTime'].idxmin()
        lowest_overhead = comparison['overhead'].idxmin()
        
        print(f"\n🥇 Mejor detección: {best_detection}")
        print(f"⚡ Más rápido: {fastest}")
        print(f"📦 Menor overhead: {lowest_overhead}")

def main():
    """Función principal"""
    
    # Rutas de archivos
    input_file = "tests/emisor_data.csv"
    output_file = "results/receptor_results.csv"
    
    try:
        # Crear procesador y ejecutar
        processor = ReceptorProcessor(input_file, output_file)
        processor.process_all_tests()
        
        print("\n🎉 ¡Procesamiento del receptor completado exitosamente!")
        print(f"📁 Resultados disponibles en: {output_file}")
        print("\n🔬 Ahora puedes analizar los datos con:")
        print("   - pandas para análisis estadístico")
        print("   - matplotlib/seaborn para gráficas")
        print("   - Excel para visualización manual")
        
    except KeyboardInterrupt:
        print("\n❌ Procesamiento interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el procesamiento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()