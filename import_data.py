from app import db
from sqlalchemy import text

def import_sql():
    with open("backup.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";\n")  # separa por cada sentencia
        with db.engine.connect() as conn:
            for command in sql_commands:
                cmd = command.strip()
                if cmd:  # evita líneas vacías
                    conn.execute(text(cmd))

if __name__ == "__main__":
    import_sql()
    print("Datos importados correctamente 🚀")
