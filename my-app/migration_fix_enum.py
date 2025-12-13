import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def fix_enum_constraint():
    print("Modifying unidad_medida column to VARCHAR(50)...")
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Change column to VARCHAR to allow new units like 'kg', 'litros'
                sql = "ALTER TABLE item MODIFY COLUMN unidad_medida VARCHAR(50) DEFAULT 'unidad'"
                cursor.execute(sql)
                print("Column modified successfully!")
                conexion.commit()
                
    except Exception as e:
        print(f"Error modifying column: {e}")

if __name__ == "__main__":
    fix_enum_constraint()
