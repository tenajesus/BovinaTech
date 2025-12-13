import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def check_lote():
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("DESCRIBE lote")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"{col[0]}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_lote()
