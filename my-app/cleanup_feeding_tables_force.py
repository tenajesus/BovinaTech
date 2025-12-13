import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def cleanup_tables_force():
    print("Cleaning up Feeding Module tables (Force)...")
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Disable FK checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                
                # Drop tables requested by user
                tables_to_drop = ['formula_alimento', 'ingrediente_formula']
                for table in tables_to_drop:
                    sql = f"DROP TABLE IF EXISTS {table}"
                    cursor.execute(sql)
                    print(f"Table '{table}' dropped.")
                
                # Re-enable FK checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                
                conexion.commit()
                print("Cleanup complete.")
                
    except Exception as e:
        print(f"Error cleaning up tables: {e}")

if __name__ == "__main__":
    cleanup_tables_force()
