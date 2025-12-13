import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def list_tables_and_columns():
    print("Inspecting database schema...")
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    print(f"\nTable: {table_name}")
                    cursor.execute(f"DESCRIBE {table_name}")
                    columns = cursor.fetchall()
                    for col in columns:
                        print(f"  {col[0]} ({col[1]})")
                
    except Exception as e:
        print(f"Error inspecting DB: {e}")

if __name__ == "__main__":
    list_tables_and_columns()
