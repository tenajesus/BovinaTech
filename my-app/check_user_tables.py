import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def check_specific_tables():
    tables_to_check = ['formula', 'detalle_formula', 'registro_alimento', 'formula_alimento', 'ingrediente_formula']
    print("Checking specific tables...")
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                for table in tables_to_check:
                    cursor.execute(f"SHOW TABLES LIKE '{table}'")
                    result = cursor.fetchone()
                    if result:
                        print(f"Table '{table}' EXISTS.")
                        cursor.execute(f"DESCRIBE {table}")
                        columns = cursor.fetchall()
                        for col in columns:
                            print(f"  {col[0]} ({col[1]})")
                    else:
                        print(f"Table '{table}' does NOT exist.")
                
    except Exception as e:
        print(f"Error checking tables: {e}")

if __name__ == "__main__":
    check_specific_tables()
