import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def inspect_to_file():
    try:
        with connectionBD() as conexion:
            with conexion.cursor(dictionary=True) as cursor:
                cursor.execute("DESCRIBE item")
                columns = cursor.fetchall()
                with open('db_info.txt', 'w') as f:
                    f.write(f"{'Field':<25} {'Type':<20} {'Null':<5} {'Default'}\n")
                    f.write("-" * 60 + "\n")
                    for col in columns:
                        f.write(f"{col['Field']:<25} {col['Type']:<20} {col['Null']:<5} {col['Default']}\n")
        print("Done")
    except Exception as e:
        with open('db_info.txt', 'w') as f:
            f.write(str(e))

if __name__ == "__main__":
    inspect_to_file()
