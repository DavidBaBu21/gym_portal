from app import db
from sqlalchemy import text

def import_sql():
    with open("backup.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";\n")
        with db.engine.begin() as conn:  # begin() maneja transacciones
            for command in sql_commands:
                cmd = command.strip()
                if cmd:
                    try:
                        conn.execute(text(cmd))
                    except Exception as e:
                        print(f"Error en: {cmd[:50]}... -> {e}")
