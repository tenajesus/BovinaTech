import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from conexion.conexionBD import connectionBD

def create_feeding_tables():
    print("Creating tables for Feeding Module...")
    try:
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Table: formula
                sql_formula = """
                CREATE TABLE IF NOT EXISTS formula (
                    id_formula INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT,
                    costo_estimado DECIMAL(10, 2) DEFAULT 0.00,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_formula)
                print("Table 'formula' created/verified.")

                # Table: ingrediente_formula
                sql_ingrediente = """
                CREATE TABLE IF NOT EXISTS ingrediente_formula (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_formula INT NOT NULL,
                    id_item INT NOT NULL,
                    porcentaje DECIMAL(5, 2) NOT NULL,
                    FOREIGN KEY (id_formula) REFERENCES formula(id_formula) ON DELETE CASCADE,
                    FOREIGN KEY (id_item) REFERENCES item(id_item)
                )
                """
                cursor.execute(sql_ingrediente)
                print("Table 'ingrediente_formula' created/verified.")

                # Table: registro_alimento
                # Assuming 'animal' table exists and has 'id_animal'. 
                # If not, I might need to check, but based on context it likely exists.
                # 'tipo_alimento' in the user request likely maps to 'id_formula'.
                sql_registro = """
                CREATE TABLE IF NOT EXISTS registro_alimento (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATE NOT NULL,
                    id_animal INT NOT NULL,
                    id_formula INT NOT NULL,
                    racion_asignada DECIMAL(8, 2) NOT NULL,
                    racion_consumida DECIMAL(8, 2) NOT NULL,
                    observaciones TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_formula) REFERENCES formula(id_formula),
                    FOREIGN KEY (id_animal) REFERENCES animal(id_animal)
                )
                """
                cursor.execute(sql_registro)
                print("Table 'registro_alimento' created/verified.")

                conexion.commit()
                print("All tables created successfully!")
                
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_feeding_tables()
