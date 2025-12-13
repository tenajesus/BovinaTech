import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def check_specific_tables():
    tables_to_check = ['formula', 'detalle_formula', 'registro_alimento', 'formula_alimento', 'ingrediente_formula']
    output_file = "user_tables_schema_utf8.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Checking specific tables...\n")
        try:
            with connectionBD() as conexion:
                with conexion.cursor() as cursor:
                    for table in tables_to_check:
                        cursor.execute(f"SHOW TABLES LIKE '{table}'")
                        result = cursor.fetchone()
                        if result:
                            f.write(f"Table '{table}' EXISTS.\n")
                            cursor.execute(f"DESCRIBE {table}")
                            columns = cursor.fetchall()
                            for col in columns:
                                f.write(f"  {col[0]} ({col[1]})\n")
                        else:
                            f.write(f"Table '{table}' does NOT exist.\n")
                    
        except Exception as e:
            f.write(f"Error checking tables: {e}\n")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    check_specific_tables()
