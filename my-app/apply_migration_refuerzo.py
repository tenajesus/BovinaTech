import sys
import os

# Agregar directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conexion.conexionBD import connectionBD

def aplicar_migracion():
    try:
        print("Iniciando migración...")
        with connectionBD() as conexion:
            with conexion.cursor() as cursor:
                # Leer archivo SQL
                with open('context/migration_add_refuerzo_columns.sql', 'r') as f:
                    sql_content = f.read()
                
                # Ejecutar cada sentencia
                statements = sql_content.split(';')
                for statement in statements:
                    if statement.strip():
                        print(f"Ejecutando: {statement.strip()}")
                        try:
                            cursor.execute(statement)
                        except Exception as e:
                            # Ignorar error de columna duplicada si ya existe
                            if "Duplicate column name" in str(e):
                                print("La columna ya existe, continuando...")
                            else:
                                raise e
                
                conexion.commit()
        print("Migración completada exitosamente.")
        return True
    except Exception as e:
        print(f"Error durante la migración: {e}")
        return False

if __name__ == "__main__":
    aplicar_migracion()
