from app import db
from sqlalchemy import text

def import_sql():
    with open("backup.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read()
        with db.engine.connect() as conn:
            conn.execute(text(sql_commands))

if __name__ == "__main__":
    import_sql()
    print("Datos importados correctamente 🚀")
