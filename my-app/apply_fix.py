import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def aplicar_fix():
    try:
        print("Aplicando corrección de estructura...")
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                with open('context/fix_structure_item.sql', 'r') as f:
                    sql = f.read()
                
                # Ejecutar como un solo bloque si no tiene ; múltiples o separar
                # MySQL connector often allows executing multiple if separated?
                # safer to execute statement by statement
                statements = sql.split(';')
                for stmt in statements:
                    if stmt.strip():
                        print(f"Ejecutando: {stmt.strip()}")
                        cursor.execute(stmt)
                        
                conexion.commit()
        print("Corrección aplicada Exitosamente.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    aplicar_fix()
