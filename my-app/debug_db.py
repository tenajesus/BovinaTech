import sys
import os

# Agregar directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conexion.conexionBD import connectionBD

def inspect_table():
    try:
        print("Inspeccionando tabla 'item'...")
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute("DESCRIBE item")
                columns = cursor.fetchall()
                print(f"{'Field':<25} {'Type':<20} {'Null':<5} {'Default'}")
                print("-" * 60)
                for col in columns:
                    print(f"{col['Field']:<25} {col['Type']:<20} {col['Null']:<5} {col['Default']}")
                    
    except Exception as e:
        print(f"Error inspeccionando: {e}")

if __name__ == "__main__":
    inspect_table()
