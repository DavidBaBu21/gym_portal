from app import db
from sqlalchemy import text

def import_sql():
    tables_count = {}
    with open("backup_postgres.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";\n")
        with db.engine.begin() as conn:  # begin() maneja transacciones
            for command in sql_commands:
                cmd = command.strip()
                if cmd:
                    try:
                        conn.execute(text(cmd))
                        # Detecta si es un INSERT y cuenta por tabla
                        if cmd.upper().startswith("INSERT INTO"):
                            table_name = cmd.split()[2]
                            tables_count[table_name] = tables_count.get(table_name, 0) + 1
                    except Exception as e:
                        print(f"Error en: {cmd[:50]}... -> {e}")

    # Log final
    print("✅ Importación completada 🚀")
    for table, count in tables_count.items():
        print(f"Tabla {table}: {count} registros insertados")

if __name__ == "__main__":
    import_sql()
