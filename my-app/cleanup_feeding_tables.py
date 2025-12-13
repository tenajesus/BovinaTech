import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def cleanup_tables():
    print("Cleaning up Feeding Module tables...")
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Drop tables requested by user
                tables_to_drop = ['formula_alimento', 'ingrediente_formula']
                for table in tables_to_drop:
                    sql = f"DROP TABLE IF EXISTS {table}"
                    cursor.execute(sql)
                    print(f"Table '{table}' dropped.")
                
                conexion.commit()
                print("Cleanup complete.")
                
    except Exception as e:
        print(f"Error cleaning up tables: {e}")

if __name__ == "__main__":
    cleanup_tables()
